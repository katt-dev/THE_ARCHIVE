import os

VERSION = "3.17"
SAVE_VERSION = 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
