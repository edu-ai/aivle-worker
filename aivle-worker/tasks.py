from __future__ import absolute_import

from celery import Celery

from apis import start_job, submit_job
from client import run_submission

# set the default Django settings module for the 'celery' program.
app = Celery("worker", backend="rpc", broker="amqp://localhost")


@app.task(bind=True, name="aiVLE.submit_eval_task")
def evaluate(self, job_id):
    task_id = self.request.id
    submission = start_job(job_id, task_id)
    result = run_submission(submission)
    submit_job(job_id, task_id, result)
    return result
