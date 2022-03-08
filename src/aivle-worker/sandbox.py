import hashlib
import logging
import os
import subprocess
from typing import List

import zmq

from .apis import ERROR_TIME_LIMIT_EXCEEDED, ERROR_RUNTIME_ERROR
from .settings import PROFILE_PATH, TEMP_VENV_FOLDER, CREATE_VENV_PATH, ZMQ_PORT

logger = logging.getLogger("root")


def create_venv(req_path: str, force: bool = False) -> str:
    """
    Create virtual environment (NOTE: this step happens outside of any security sandbox)

    :param req_path: path to the requirements.txt file
    :param force: if True, the cached environment will be overwritten
    :return: venv name
    """
    with open(req_path, "r") as f:
        req_str = f.read()
        f.close()
    env_name = hashlib.md5(req_str.encode("ascii")).hexdigest()
    dst_path = os.path.join(TEMP_VENV_FOLDER, env_name)
    if os.path.exists(dst_path) and not force:
        return env_name
    cmd = ["bash", CREATE_VENV_PATH, dst_path, req_path]
    # Reference: https://stackoverflow.com/a/4417735
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line, end="")
    for stderr_line in iter(popen.stderr.readline, ""):
        print(stderr_line, end="")
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    return env_name


def run_with_venv(env_name: str, command: List[str], task_id: int, job_id: int, celery_task_id: str, home: str = "",
                  rlimit: int = 0, vram_limit: int = 256, time_limit: int = 0) -> str:
    """
    Run `command` within venv named `env_name`

    :param env_name: venv name
    :param command:
    :param home: path to the home directory (check --private={HOME} in Firejail doc)
    :param rlimit: RAM limit in MiB (<=0 means no limit,
    :param task_id: aiVLE task ID (NOT evaluation job/task ID)
    :param vram_limit: VRAM limit in MiB
    :param time_limit:

    :return: error type (defined as constants in api)
    """
    full_cmd = ["firejail",
                f"--profile={PROFILE_PATH}",
                "--read-only=/tmp",
                f"--env=PATH={os.path.join(TEMP_VENV_FOLDER, env_name)}/bin:/usr/bin",
                # f"--output={os.path.join(home, 'stdout.log')}",
                f"--output-stderr={os.path.join(home, 'stdout.log')}", ]
    if rlimit > 0:
        full_cmd.append(f"--rlimit-as={rlimit * 1024 * 1024}")
    if home != "":
        full_cmd.append(f"--private={home}")
    else:
        full_cmd.append("--private")
    full_cmd.extend(command)
    logger.debug(f"[SANDBOX | run_with_venv] command: {' '.join(full_cmd)}")
    proc = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{ZMQ_PORT}")
    socket.send_pyobj({
        "message_type": "sandbox-start",
        "payload": {
            "job_id": job_id,
            "celery_task_id": celery_task_id,
            "pid": proc.pid,
            "vram_limit": vram_limit,
        },
    })
    _ = socket.recv()
    error_type = None
    if time_limit > 0:
        try:
            proc.wait(time_limit + 30)  # wait 30 more seconds
        except subprocess.TimeoutExpired:
            error_type = ERROR_TIME_LIMIT_EXCEEDED
    else:
        return_code = proc.wait()
        if return_code != 0:
            error_type = ERROR_RUNTIME_ERROR
    # result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # print(result.returncode, result.stderr, result.stdout)
    socket.send_pyobj({
        "message_type": "sandbox-finish",
        "payload": {
            "task_id": task_id,
            "pid": proc.pid,
            "vram_limit": vram_limit,
        },
    })
    _ = socket.recv()
    return error_type
