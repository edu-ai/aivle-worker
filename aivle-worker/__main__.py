import settings
import aivle_venv
import sandbox
import client

# print(settings.TEMP_VENV_FOLDER)
# env_name = aivle_venv.create_venv("/home/leo/aivle-runner-v2/aivle-worker/requirements/base.txt")
# print(env_name)
# sandbox.run_with_venv(env_name, ["bash", "./bootstrap.sh"], "/tmp/aivle-worker/grading/test")

submission = client.get_submission()
client.run_submission(submission)
