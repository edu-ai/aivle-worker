import logging
import time

import psutil
from py3nvml.py3nvml import NVMLError, nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetName, \
    nvmlDeviceGetMemoryInfo

from apis import QueueInfo, stop_consuming, resume_consuming

logger = logging.getLogger("root")

MONITOR_INTERVAL = 1


def start_monitor(queue_info: QueueInfo):
    resume_consuming(queue_info)  # restore the default state in case the previous run ended in paused state
    nvmlInit()
    monitor_gpu = True
    try:
        device_count = nvmlDeviceGetCount()
        if device_count > 1:
            logger.error("More than one GPU is not supported")
            monitor_gpu = False
        if device_count == 0:
            logger.error("No supported GPU is found")
            monitor_gpu = False
    except NVMLError:
        monitor_gpu = False
    if monitor_gpu:
        handle = nvmlDeviceGetHandleByIndex(0)
        device_name = nvmlDeviceGetName(handle)
        logger.info(f"Monitoring GPU: {device_name}")
    paused = False  # TODO: only pause when the constraint is violated for multiple checks
    while True:
        free_memory = psutil.virtual_memory().available / (1024 * 1024)  # free memory (MiB)
        free_cpu = 100 - psutil.cpu_percent()  # cpu utlization (%)
        # per_cpu = psutil.cpu_percent(percpu=True)
        if monitor_gpu:
            # free_gpu = 100 - nvmlDeviceGetUtilizationRates(handle).gpu
            mem_info = nvmlDeviceGetMemoryInfo(handle)
            free_vram = mem_info.free // (1024 * 1024)  # in MiB
        if not paused:
            if free_memory < queue_info.ram:
                paused = True
                logger.info(f"Paused due to insufficient memory: have {free_memory}MiB, need {queue_info.ram}MiB")
                stop_consuming(queue_info)
            elif free_cpu < queue_info.cpu:
                paused = True
                logger.info(f"Paused due to insufficient CPU: have {free_cpu}%, need {queue_info.cpu}%")
                stop_consuming(queue_info)
            elif monitor_gpu:
                if free_vram < queue_info.vram:
                    paused = True
                    logger.info(f"Paused due to insufficient VRAM: have {free_vram}MiB, need {queue_info.vram}MiB")
                    stop_consuming(queue_info)
        else:
            if free_memory >= queue_info.ram and free_cpu >= queue_info.cpu \
                    and (not monitor_gpu or (free_vram >= queue_info.vram)):
                paused = False
                logger.info("Operation resumed")
                resume_consuming(queue_info)
        time.sleep(MONITOR_INTERVAL)
