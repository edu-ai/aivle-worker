import logging

from tasks import app

logging.basicConfig(level=logging.DEBUG)

# print(settings.TEMP_VENV_FOLDER)
# env_name = aivle_venv.create_venv("/home/leo/aivle-runner-v2/aivle-worker/requirements/base.txt")
# print(env_name)
# sandbox.run_with_venv(env_name, ["bash", "./bootstrap.sh"], "/tmp/aivle-worker/grading/test")

argv = [
    'worker',
    '--loglevel=INFO',
]
app.worker_main(argv)
