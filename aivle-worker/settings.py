import os
import socket
import tempfile

from dotenv import load_dotenv

load_dotenv(verbose=True)

# Sandbox config
PROFILE_PATH = "./profiles/aivle-base.profile"
CREATE_VENV_PATH = "./scripts/create-venv.sh"
TEMP_FOLDER_ROOT = os.path.join(tempfile.gettempdir(), "aivle-worker")
if not os.path.isdir(TEMP_FOLDER_ROOT):
    os.mkdir(TEMP_FOLDER_ROOT)
TEMP_VENV_FOLDER = os.path.join(TEMP_FOLDER_ROOT, "venvs")
if not os.path.isdir(TEMP_VENV_FOLDER):
    os.mkdir(TEMP_VENV_FOLDER)
TEMP_GRADING_FOLDER = os.path.join(TEMP_FOLDER_ROOT, "grading")
if not os.path.isdir(TEMP_GRADING_FOLDER):
    os.mkdir(TEMP_GRADING_FOLDER)
LOCAL_FILE = True

# API config
API_BASE_URL = "http://localhost:8000/api/v1"
# API_BASE_URL = "https://aivle-api.leotan.cn/api/v1"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CELERY_BROKER_URI = os.getenv("BROKER_URI")
CELERY_RESULT_BACKEND = "rpc"
CELERY_QUEUE = os.getenv("TASK_QUEUE") if os.getenv("TASK_QUEUE") is not None else "default"
CELERY_CONCURRENCY = os.getenv("CELERY_CONCURRENCY") if os.getenv("CELERY_CONCURRENCY") is not None else "1"
WORKER_NAME = os.getenv("WORKER_NAME") if os.getenv("WORKER_NAME") is not None else "celery"
FULL_WORKER_NAME = f"{WORKER_NAME}@{socket.gethostname()}"
