from __future__ import absolute_import

from celery import Celery

from apis import start_job, submit_job
from client import run_submission
from settings import CELERY_BROKER_URI, CELERY_RESULT_BACKEND

# set the default Django settings module for the 'celery' program.
app = Celery("worker", backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URI)


@app.task(bind=True, name="aiVLE.submit_eval_task")
def evaluate(self, job_id):
    task_id = self.request.id
    submission = start_job(job_id, task_id)
    result = run_submission(submission)
    submit_job(job_id, task_id, result)
    return result
