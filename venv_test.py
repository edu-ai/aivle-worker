import hashlib
import os
import shutil
import subprocess
import tempfile
from typing import List

TEMP_VENV_PATH = "./tmp_venv"
OS_TEMP_PATH = tempfile.gettempdir()

# RUNNER_ID = uuid.uuid4().hex
RUNNER_ID = "test"
RUNNER_TEMP_PATH = os.path.join(OS_TEMP_PATH, "aivle_runner", RUNNER_ID)


def main():
    env_name = create_venv("./venv-req.txt")
    copy_venv(env_name)
    run_firejail_with_venv(env_name,
                           ["python", os.path.join(RUNNER_TEMP_PATH, "venvs", "aivle_gym_single.py")])


def create_venv(req_path: str) -> str:
    with open(req_path, "r") as f:
        req_str = f.read()
        f.close()
    env_name = hashlib.md5(req_str.encode("ascii")).hexdigest()
    dst_path = os.path.join(TEMP_VENV_PATH, env_name)
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
        # return env_name
    cmd = ["bash", "./create-venv.sh", dst_path, req_path]
    # Reference: https://stackoverflow.com/a/4417735
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line)
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    return env_name


def copy_venv(env_name: str):
    src_path = os.path.join(TEMP_VENV_PATH, env_name)
    dst_path = os.path.join(RUNNER_TEMP_PATH, "venvs", env_name)
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
        # return
    shutil.copytree(src=src_path, dst=dst_path, symlinks=False)


def run_firejail_with_venv(env_name: str, command: List[str]):
    full_cmd = ["firejail", "--private", "--private-dev", "--read-only=/tmp",
                f"--env=PATH={os.path.join(RUNNER_TEMP_PATH, 'venvs', env_name)}/bin:/usr/bin"]
    full_cmd.extend(command)
    result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(result.returncode, result.stderr, result.stdout)


if __name__ == "__main__":
    copy_venv("venv2")
