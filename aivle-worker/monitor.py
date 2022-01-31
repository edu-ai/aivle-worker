import logging
import time

import psutil

from apis import QueueInfo, stop_consuming, resume_consuming

logger = logging.getLogger("root")


def start_monitor(queue_info: QueueInfo):
    resume_consuming(queue_info)  # restore the default state in case the previous run ended in paused state
    paused = False  # TODO: only pause when the constraint is violated for multiple checks
    while True:
        free_memory = psutil.virtual_memory().available / (1024 * 1024)  # free memory (MiB)
        free_cpu = 100 - psutil.cpu_percent()  # cpu utlization (%)
        # per_cpu = psutil.cpu_percent(percpu=True)
        if not paused:
            if free_memory < queue_info.ram or free_cpu < queue_info.cpu:
                paused = True
                logger.info("Paused due to high system load")
                stop_consuming(queue_info)
        else:
            if free_memory >= queue_info.ram and free_cpu >= queue_info.cpu:
                paused = False
                logger.info("Operation resumed")
                resume_consuming(queue_info)
        time.sleep(1)
