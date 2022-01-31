import logging

import zmq

from client import Submission, run_submission
from settings import CELERY_QUEUE, CELERY_CONCURRENCY, ACCESS_TOKEN, API_BASE_URL, FULL_WORKER_NAME
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


def send_info_to_monitor():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:55545")
    socket.send_pyobj({
        "api_base_url": API_BASE_URL,
        "access_token": ACCESS_TOKEN,
        "full_worker_name": FULL_WORKER_NAME,
        "queue_name": CELERY_QUEUE,
    })
    _ = socket.recv()


send_info_to_monitor()
start_worker()
# start_sandbox()
