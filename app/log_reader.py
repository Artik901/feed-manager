import json
from pathlib import Path

from config.config import (
    LOG_HISTORY_DIR,
    LOG_FILE
)


def get_last_log():

    file = Path(
        LOG_FILE
    )

    if not file.exists():
        return None


    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def get_history():

    history_dir = Path(
        LOG_HISTORY_DIR
    )

    if not history_dir.exists():
        return []


    logs = sorted(
        history_dir.glob("run_*.json"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )


    result = []


    for log_file in logs:

        try:

            with open(
                log_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


            result.append(data)


        except Exception:

            pass


    return result