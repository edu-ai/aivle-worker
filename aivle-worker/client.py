import json
import os
import shutil

import aivle_venv
import sandbox
import settings


class Submission:
    def __init__(self, id: str, env: dict, grader: str, agent: str, bootstrap: str):
        self.id = id
        self.env = env
        self.grader = grader
        self.agent = agent
        self.bootstrap = bootstrap


def get_submission():
    with open("/home/leo/aivle-runner-v2/submission.json", "r") as f:
        obj = json.loads(f.read())
        return Submission(**obj)


def run_submission(s: Submission):
    env_name = aivle_venv.create_venv(s.env["requirements"])
    temp_grading_folder = os.path.join(settings.TEMP_GRADING_FOLDER, s.id)
    if not os.path.exists(temp_grading_folder):
        os.mkdir(temp_grading_folder)
    shutil.copy(s.agent, temp_grading_folder)
    shutil.copy(s.grader, temp_grading_folder)
    shutil.copy(s.bootstrap, temp_grading_folder)
    sandbox.run_with_venv(env_name, ["bash", "./bootstrap.sh"], temp_grading_folder)
    shutil.rmtree(temp_grading_folder)
