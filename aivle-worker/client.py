import json
import os
import shutil

import requests

import aivle_venv
import sandbox
import settings
import util


class Submission:
    def __init__(self, id: str, env: dict, grader: str, agent: str, bootstrap: str):
        self.id = id
        self.env = env
        self.grader = grader
        self.agent = agent
        self.bootstrap = bootstrap


def get_submission(path: str):
    with open(path, "r") as f:
        obj = json.loads(f.read())
        s = Submission(**obj)
        if settings.LOCAL_FILE:
            s.env["requirements"] = "file://" + os.path.abspath(s.env["requirements"])
            s.grader = "file://" + os.path.abspath(s.grader)
            s.agent = "file://" + os.path.abspath(s.agent)
            s.bootstrap = "file://" + os.path.abspath(s.bootstrap)
        return s


def download_submission(s: Submission) -> str:
    temp_grading_folder = os.path.join(settings.TEMP_GRADING_FOLDER, s.id)
    if not os.path.exists(temp_grading_folder):
        os.mkdir(temp_grading_folder)
    session = requests.Session()
    if settings.LOCAL_FILE:
        session.mount("file://", util.LocalFileAdapter())
    util.download_and_save(session, s.env["requirements"], os.path.join(temp_grading_folder, "requirements.txt"))
    util.download_and_save(session, s.grader, os.path.join(temp_grading_folder, "grader.py"))
    util.download_and_save(session, s.agent, os.path.join(temp_grading_folder, "agent.py"))
    util.download_and_save(session, s.bootstrap, os.path.join(temp_grading_folder, "bootstrap.sh"))
    return temp_grading_folder


def run_submission(s: Submission) -> str:
    temp_grading_folder = download_submission(s)
    env_name = aivle_venv.create_venv(os.path.join(temp_grading_folder, "requirements.txt"))
    sandbox.run_with_venv(env_name, ["bash", "./bootstrap.sh"], temp_grading_folder)
    with open(os.path.join(temp_grading_folder, "stdout.log"), "r") as f:
        stdout_log = f.read().split("\x07")[1]
        f.close()
    shutil.rmtree(temp_grading_folder)
    return stdout_log
