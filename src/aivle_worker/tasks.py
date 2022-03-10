from __future__ import absolute_import

import os

from celery import Celery
from celery.signals import celeryd_after_setup

from .apis import start_job, submit_job
from .client import run_submission
from .settings import CELERY_BROKER_URI, CELERY_RESULT_BACKEND

# set the default Django settings module for the 'celery' program.
app = Celery("worker", backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URI)


@app.task(bind=True, name="aiVLE.submit_eval_task")
def evaluate(self, job_id):
    celery_task_id = self.request.id
    submission = start_job(job_id, celery_task_id)
    result = run_submission(s=submission, job_id=job_id, celery_task_id=celery_task_id)
    submit_job(job_id, celery_task_id, result)
    return {
        "ok": result.ok,
        "raw_log": result.raw,
        "result": result.result,
        "error": result.error,
    }


@celeryd_after_setup.connect
def capture_worker_name(sender, instance, **kwargs):
    os.environ["WORKER_NAME"] = '{0}'.format(sender)
