import os
import tempfile

from dotenv import load_dotenv

load_dotenv(verbose=True)

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
# API_BASE_URL = "http://localhost:8000/api/v1"
API_BASE_URL = "https://aivle-api.leotan.cn/api/v1"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CELERY_BROKER_URI = os.getenv("BROKER_URI")
CELERY_RESULT_BACKEND = "rpc"
