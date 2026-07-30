import json
from pathlib import Path
from datetime import datetime

from config.config import BASE_DIR


STATUS_FILE = (
    BASE_DIR /
    "storage" /
    "logs" /
    "status.json"
)


def save_status(
        status,
        step,
        details=None
):

    STATUS_FILE.parent.mkdir(
        exist_ok=True
    )


    data = {

        "status": status,

        "step": step,

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "details": details or {}

    }


    with open(
        STATUS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def get_status():

    if not STATUS_FILE.exists():

        return None


    with open(
        STATUS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)