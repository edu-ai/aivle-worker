import hashlib
import os
import subprocess
from typing import List

import settings


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
    dst_path = os.path.join(settings.TEMP_VENV_FOLDER, env_name)
    if os.path.exists(dst_path) and not force:
        return env_name
    cmd = ["bash", settings.CREATE_VENV_PATH, dst_path, req_path]
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


def run_with_venv(env_name: str, command: List[str], home: str = "", rlimit: int = 256):
    """
    Run `command` within venv named `env_name`

    :param env_name: venv name
    :param command:
    :param home: path to the home directory (check --private={HOME} in Firejail doc)
    :param rlimit: ram limit in MiB
    """
    full_cmd = ["firejail",
                f"--profile={settings.PROFILE_PATH}",
                "--read-only=/tmp",
                f"--env=PATH={os.path.join(settings.TEMP_VENV_FOLDER, env_name)}/bin:/usr/bin",
                # f"--output={os.path.join(home, 'stdout.log')}",
                f"--output-stderr={os.path.join(home, 'stdout.log')}",
                f"--rlimit-as={rlimit * 1024 * 1024}",
                ]
    if home != "":
        full_cmd.append(f"--private={home}")
    else:
        full_cmd.append("--private")
    full_cmd.extend(command)
    print(" ".join(full_cmd))
    result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # print(result.returncode, result.stderr, result.stdout)
