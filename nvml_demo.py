import logging

from py3nvml.py3nvml import *

logger = logging.getLogger()

nvmlInit()
device_count = nvmlDeviceGetCount()  # will raise an exception if nvidia driver is not installed properly
if device_count > 1:
    logger.error("more than one GPU is not supported")
    sys.exit(1)
elif device_count <= 0:
    logger.error("no supported GPU is found")
    sys.exit(1)

handle = nvmlDeviceGetHandleByIndex(0)
device_name = nvmlDeviceGetName(handle)
print(f"Device name: {device_name}")
utils = nvmlDeviceGetUtilizationRates(handle)
gpu_util = utils.gpu
mem_util = utils.memory
print(f"GPU util: {gpu_util}%")
mem_info = nvmlDeviceGetMemoryInfo(handle)
KB_TO_MiB_CONV = 1024 * 1024
print(f"Memory util: {mem_info.used // KB_TO_MiB_CONV}MiB ({mem_util}%) / {mem_info.total // KB_TO_MiB_CONV}MiB")
print(f"Free memory: {mem_info.free // KB_TO_MiB_CONV}MiB")

print("---Compute processes---")
for p in nvmlDeviceGetComputeRunningProcesses(handle):
    print(f"pid {p.pid} VRAM usage {p.usedGpuMemory // KB_TO_MiB_CONV}MiB")
print("---Graphics processes---")
for p in nvmlDeviceGetGraphicsRunningProcesses(handle):
    print(f"pid {p.pid} VRAM usage {p.usedGpuMemory // KB_TO_MiB_CONV}MiB")
