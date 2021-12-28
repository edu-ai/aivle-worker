import logging

from client import Submission, run_submission
from settings import CELERY_QUEUE, CELERY_CONCURRENCY
from tasks import app

logging.basicConfig(level=logging.DEBUG)


def start_sandbox():
    s = Submission(sid=233,
                   task_url="file:///home/leo/Documents/fyp/aivle-worker/examples/aivle-single/grader.zip",
                   agent_url="file:///home/leo/Documents/fyp/aivle-worker/examples/aivle-single/agent.zip")
    run_submission(s, force=True)


def start_worker():
    argv = [
        'worker',
        '--loglevel=INFO',
        '-Q',
        CELERY_QUEUE,
        f'--concurrency={CELERY_CONCURRENCY}'
    ]
    app.worker_main(argv)


start_worker()
# start_sandbox()
