import json
from pathlib import Path

from config.config import SETTINGS_FILE


def load_settings():

    file = Path(
        SETTINGS_FILE
    )

    if not file.exists():
        return {
            "markup": []
        }


    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_settings(data):

    file = Path(
        SETTINGS_FILE
    )


    file.parent.mkdir(
        exist_ok=True
    )


    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )