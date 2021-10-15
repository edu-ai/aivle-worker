import os
import shutil
import zipfile

import requests

import settings
import util
from sandbox import create_venv, run_with_venv


class Submission:
    def __init__(self, sid: int, task_url: str, agent_url: str):
        self.sid = sid
        self.task_url = task_url
        self.agent_url = agent_url

    def __str__(self):
        return f"Submission-{self.sid}-<{self.task_url}>-<{self.agent_url}>"


def _download_submission(s: Submission) -> str:
    temp_grading_folder = os.path.join(settings.TEMP_GRADING_FOLDER, str(s.sid))
    if not os.path.exists(temp_grading_folder):
        os.mkdir(temp_grading_folder)
    session = requests.Session()
    if settings.LOCAL_FILE:
        session.mount("file://", util.LocalFileAdapter())
    task_zip_path = os.path.join(temp_grading_folder, "task.zip")
    util.download_and_save(session, s.task_url, task_zip_path)
    with zipfile.ZipFile(task_zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_grading_folder)
    agent_zip_path = os.path.join(temp_grading_folder, "agent.zip")
    util.download_and_save(session, s.agent_url, agent_zip_path)
    with zipfile.ZipFile(agent_zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_grading_folder)
    return temp_grading_folder


def run_submission(s: Submission, force: bool = False) -> str:
    temp_grading_folder = _download_submission(s)
    env_name = create_venv(os.path.join(temp_grading_folder, "requirements.txt"), force=force)
    run_with_venv(env_name, ["bash", "./bootstrap.sh"], temp_grading_folder)
    # TODO: output stderr
    with open(os.path.join(temp_grading_folder, "stdout.log"), "r") as f:
        stdout_log = f.read().split("\x07")[1].splitlines()[0]  # hack
        f.close()
    shutil.rmtree(temp_grading_folder)
    return stdout_log
