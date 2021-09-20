import json
import os

import requests

from client import Submission
from settings import API_BASE_URL, ACCESS_TOKEN


def get_task_url(task_id: int):
    return API_BASE_URL + f"/tasks/{task_id}/download_grader/"


def get_agent_url(submission_id: int):
    return API_BASE_URL + f"/submissions/{submission_id}/download/"


def start_job(job_id, task_id) -> Submission:
    worker_name = "unknown_worker"
    if os.getenv("WORKER_NAME") is not None:
        worker_name = os.getenv("WORKER_NAME")
    resp = requests.get(API_BASE_URL + f"/jobs/{job_id}/start_job/",
                        headers={"Authorization": f"Token {ACCESS_TOKEN}"},
                        data={
                            "worker_name": worker_name,
                            "task_id": task_id
                        })
    if resp.status_code != 200:
        raise Exception(resp.content)
    obj = json.loads(resp.content)
    return Submission(sid=obj["submission"], task_url=get_task_url(obj["task"]),
                      agent_url=get_agent_url(obj["submission"]))


def submit_job(job_id, task_id, result):
    resp = requests.get(API_BASE_URL + f"/jobs/{job_id}/submit_job/",
                        headers={"Authorization": f"Token {ACCESS_TOKEN}"},
                        data={
                            "result": result,
                            "task_id": task_id
                        })
    return resp
