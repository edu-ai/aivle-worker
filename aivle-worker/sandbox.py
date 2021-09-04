import os
import subprocess
from typing import List

import settings


def run_with_venv(env_name: str, command: List[str], home: str = ""):
    full_cmd = ["firejail", f"--profile={settings.PROFILE_PATH}", "--read-only=/tmp",
                f"--env=PATH={os.path.join(settings.TEMP_VENV_FOLDER, env_name)}/bin:/usr/bin"]
    if home != "":
        full_cmd.append(f"--private={home}")
    else:
        full_cmd.append("--private")
    full_cmd.extend(command)
    print(" ".join(full_cmd))
    result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    print(result.returncode, result.stderr, result.stdout)
