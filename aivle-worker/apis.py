import json
import logging
import os

import requests

from client import Submission
from errors import QueueInfoNotFound, StopConsumingError, ResumeConsumingError
from settings import API_BASE_URL, ACCESS_TOKEN, FULL_WORKER_NAME

logger = logging.getLogger("root")


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


class QueueInfo:
    """
    CPU: percentage (integer)
    RAM and VRAM: MiB (integer)
    """

    def __init__(self, pk: int, name: str, cpu: int, ram: int, vram: int):
        self.pk = pk
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.vram = vram

    def __str__(self):
        return f"Resource Constraint - CPU {self.cpu}%, RAM {self.ram}MiB, VRAM {self.vram}MiB"


def get_queue_info(queue_name: str) -> QueueInfo:
    resp = requests.get(API_BASE_URL + f"/queue/", params={"name": queue_name},
                        headers={"Authorization": f"Token {ACCESS_TOKEN}"})
    results = resp.json()["results"]
    if len(results) == 0:
        raise QueueInfoNotFound()
    result = results[0]
    return QueueInfo(pk=int(result["id"]), name=result["name"], cpu=result["cpu_required"], ram=result["ram_required"],
                     vram=result["vram_required"])


def stop_consuming(queue: QueueInfo):
    resp = requests.get(API_BASE_URL + f"/queue/{queue.pk}/stop_consuming/", params={"worker": FULL_WORKER_NAME},
                        headers={"Authorization": f"Token {ACCESS_TOKEN}"})
    if resp.status_code != 200:
        raise StopConsumingError(f"stop consuming failed [{resp.status_code}]: {resp.content}")


def resume_consuming(queue: QueueInfo):
    resp = requests.get(API_BASE_URL + f"/queue/{queue.pk}/resume_consuming/", params={"worker": FULL_WORKER_NAME},
                        headers={"Authorization": f"Token {ACCESS_TOKEN}"})
    if resp.status_code != 200:
        raise ResumeConsumingError(f"resume consuming failed [{resp.status_code}]: {resp.content}")
