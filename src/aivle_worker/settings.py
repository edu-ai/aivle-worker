import os
import socket
import tempfile

from dotenv import load_dotenv

from .errors import DotEnvFileNotFound, MissingDotEnvField

DOTENV_PATH = "./.env"
if not os.path.exists(DOTENV_PATH):
    raise DotEnvFileNotFound()
load_dotenv(verbose=True, dotenv_path=DOTENV_PATH)

# Sandbox config
package_directory = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(package_directory, "profiles", "aivle-base.profile")  # "./profiles/aivle-base.profile"
CREATE_VENV_PATH = os.path.join(package_directory, "scripts", "create-venv.sh")  # "./scripts/create-venv.sh"
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
if os.getenv("API_BASE_URL") is None:
    raise MissingDotEnvField("API_BASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")
if os.getenv("ACCESS_TOKEN") is None:
    raise MissingDotEnvField("ACCESS_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if os.getenv("BROKER_URI") is None:
    raise MissingDotEnvField("BROKER_URI")
CELERY_BROKER_URI = os.getenv("BROKER_URI")
CELERY_RESULT_BACKEND = "rpc"
CELERY_QUEUE = os.getenv("TASK_QUEUE") if os.getenv("TASK_QUEUE") is not None else "default"
CELERY_CONCURRENCY = os.getenv("CELERY_CONCURRENCY") if os.getenv("CELERY_CONCURRENCY") is not None else "1"
WORKER_NAME = os.getenv("WORKER_NAME") if os.getenv("WORKER_NAME") is not None else "celery"
FULL_WORKER_NAME = f"{WORKER_NAME}@{socket.gethostname()}"

# Monitor config
ZMQ_PORT = os.getenv("ZMQ_PORT") if os.getenv("ZMQ_PORT") is not None else "15921"


def update_queue(val: str):
    global CELERY_QUEUE
    CELERY_QUEUE = val


def update_concurrency(val: int):
    global CELERY_CONCURRENCY
    CELERY_CONCURRENCY = str(val)
    print(CELERY_CONCURRENCY)


def update_worker_name(val: str):
    global WORKER_NAME, FULL_WORKER_NAME
    WORKER_NAME = val
    FULL_WORKER_NAME = f"{WORKER_NAME}@{socket.gethostname()}"


def update_zmq_port(val: int):
    global ZMQ_PORT
    ZMQ_PORT = str(val)
