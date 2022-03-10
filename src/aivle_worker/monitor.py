import logging
import time

import psutil
import zmq
from py3nvml.py3nvml import NVMLError, nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetName, \
    nvmlDeviceGetMemoryInfo, nvmlDeviceGetComputeRunningProcesses

from .apis import QueueInfo, stop_consuming, resume_consuming, update_job_error, ERROR_VRAM_LIMIT_EXCEEDED
from .settings import ZMQ_PORT

logger = logging.getLogger("root")

MONITOR_INTERVAL = 1


def start_monitor(queue_info: QueueInfo):
    resume_consuming(queue_info)  # restore the default state in case the previous run ended in paused state
    nvmlInit()
    monitor_gpu = True
    try:
        device_count = nvmlDeviceGetCount()
        if device_count > 1:
            logger.error("[MONITOR] More than one GPU is not supported")
            monitor_gpu = False
        if device_count == 0:
            logger.error("[MONITOR] No supported GPU is found")
            monitor_gpu = False
    except NVMLError:
        monitor_gpu = False
    if monitor_gpu:
        handle = nvmlDeviceGetHandleByIndex(0)
        device_name = nvmlDeviceGetName(handle)
        logger.info(f"[MONITOR] Monitoring GPU: {device_name}")
    paused = False  # TODO: only pause when the constraint is violated for multiple checks
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{ZMQ_PORT}")
    while True:
        free_memory = psutil.virtual_memory().available / (1024 * 1024)  # free memory (MiB)
        free_cpu = 100 - psutil.cpu_percent()  # cpu utlization (%)
        # per_cpu = psutil.cpu_percent(percpu=True)
        if monitor_gpu:
            # free_gpu = 100 - nvmlDeviceGetUtilizationRates(handle).gpu
            mem_info = nvmlDeviceGetMemoryInfo(handle)
            free_vram = mem_info.free // (1024 * 1024)  # in MiB
            proc_info = nvmlDeviceGetComputeRunningProcesses(handle)
            encoded_proc_info = []
            for info in proc_info:
                encoded_proc_info.append({
                    "pid": info.pid,
                    "vram": info.usedGpuMemory,
                })
            socket.send_pyobj(
                {
                    "message_type": "monitor-update",
                    "payload": encoded_proc_info,
                }
            )
            _ = socket.recv()
        if not paused:
            if free_memory < queue_info.ram:
                paused = True
                logger.info(
                    f"[MONITOR] Paused due to insufficient memory: have {free_memory}MiB, need {queue_info.ram}MiB")
                stop_consuming(queue_info)
            elif free_cpu < queue_info.cpu:
                paused = True
                logger.info(f"[MONITOR] Paused due to insufficient CPU: have {free_cpu}%, need {queue_info.cpu}%")
                stop_consuming(queue_info)
            elif monitor_gpu:
                if free_vram < queue_info.vram:
                    paused = True
                    logger.info(
                        f"[MONITOR] Paused due to insufficient VRAM: have {free_vram}MiB, need {queue_info.vram}MiB")
                    stop_consuming(queue_info)
        else:
            if free_memory >= queue_info.ram and free_cpu >= queue_info.cpu \
                    and (not monitor_gpu or (free_vram >= queue_info.vram)):
                paused = False
                logger.info("[MONITOR] Operation resumed")
                resume_consuming(queue_info)
        time.sleep(MONITOR_INTERVAL)


def start_warden():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{ZMQ_PORT}")

    pid_to_task_info = {}

    while True:
        message = socket.recv_pyobj()
        socket.send(b"ok")
        message_type = message["message_type"]
        payload = message["payload"]
        if message_type == "sandbox-start":
            pid_to_task_info[payload["pid"]] = payload
        elif message_type == "sandbox-finish":
            pid_to_task_info.pop(payload["pid"], None)
        elif message_type == "monitor-update":
            pid_to_child_pids = {}
            for parent in pid_to_task_info:
                temp = [parent]
                for child in psutil.Process(parent).children(recursive=True):
                    temp.append(child.pid)
                pid_to_child_pids[parent] = temp
            pid_to_total_vram = {}
            for record in payload:
                for parent in pid_to_task_info:
                    for child in pid_to_child_pids[parent]:
                        if record["pid"] == child:
                            if parent in pid_to_total_vram:
                                pid_to_total_vram[parent] += record["vram"]
                            else:
                                pid_to_total_vram[parent] = record["vram"]
            for parent in pid_to_total_vram:
                task_info = pid_to_task_info[parent]
                if pid_to_total_vram[parent] > task_info["vram_limit"] * 1024 * 1024:
                    logger.info(f"[WARDEN] pid {parent} has a violation: "
                                f"used {pid_to_total_vram[parent] / 1024 / 1024}MiB limit "
                                f"{pid_to_task_info[parent]['vram_limit']}MiB")
                    proc = psutil.Process(parent)
                    for child in proc.children(recursive=True):
                        child.kill()
                    proc.kill()
                    update_job_error(job_id=task_info["job_id"], task_id=task_info["celery_task_id"],
                                     error=ERROR_VRAM_LIMIT_EXCEEDED)
        else:
            logger.warning(f"[WARDEN] Unknown message type: {message_type}")
