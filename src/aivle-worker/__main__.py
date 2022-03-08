import logging
from multiprocessing import Process

from .apis import get_queue_info
from .client import Submission, run_submission
from .monitor import start_monitor, start_warden
from .settings import CELERY_QUEUE, CELERY_CONCURRENCY
from .tasks import app

logging.basicConfig(level=logging.INFO)


def start_sandbox():
    s = Submission(sid=233,
                   task_url="file:///home/leo/Documents/fyp/aivle-worker/examples/worker-ram-limit/grader.zip",
                   agent_url="file:///home/leo/Documents/fyp/aivle-worker/examples/worker-ram-limit/agent.zip",
                   task_id=-1)  # negative task ID will return dummy task information
    print(run_submission(s, force=True))


def start_worker():
    argv = [
        'worker',
        '--loglevel=INFO',
        '-Q',
        CELERY_QUEUE,
        f'--concurrency={CELERY_CONCURRENCY}'
    ]
    app.worker_main(argv)


if __name__ == "__main__":
    queue = get_queue_info(CELERY_QUEUE)
    monitor_process = Process(target=start_monitor, args=(queue,))
    worker_process = Process(target=start_worker)
    warden_process = Process(target=start_warden)
    monitor_process.start()
    warden_process.start()
    worker_process.start()
    monitor_process.join()
    warden_process.join()
    worker_process.join()

    # start_sandbox()
