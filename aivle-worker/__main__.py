import settings
import virtualenv
import sandbox

print(settings.TEMP_VENV_FOLDER)
env_name = virtualenv.create_venv("/home/leo/aivle-runner-v2/aivle-worker/requirements/base.txt")
print(env_name)
sandbox.run_with_venv(env_name, ["bash", "./bootstrap.sh"], "/tmp/aivle-worker/grading/test")
