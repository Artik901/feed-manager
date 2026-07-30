import json
from pathlib import Path
from datetime import datetime

from app.system_info import get_system_info

from config.config import (
    LOG_FILE,
    LOG_HISTORY_DIR,
    MAX_LOG_HISTORY
)


def save_run_log(
        status,
        source_offers,
        categories_count,
        generated_feeds,
        generated_offers,
        feeds,
        errors=None,
        duration=None
):

    now = datetime.now()

    data = {

        "date": now.strftime(
            "%Y-%m-%d %H:%M"
        ),

        "status": status,

        "system": get_system_info(),

        "duration": duration,


        "source": {

            "offers": source_offers,

            "categories": categories_count
        },


        "result": {

            "feeds": generated_feeds,

            "offers": generated_offers
        },


        "check": {

            "success": (
                source_offers == generated_offers
            ),

            "lost": (
                source_offers - generated_offers
            )
        },


        "feeds": feeds,


        "errors": errors or []

    }


    # =========================
    # последний запуск
    # =========================

    log_file = Path(
        LOG_FILE
    )

    log_file.parent.mkdir(
        exist_ok=True
    )


    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


    # =========================
    # история запусков
    # =========================

    history_dir = Path(
        LOG_HISTORY_DIR
    )

    history_dir.mkdir(
        exist_ok=True
    )


    history_file = (
        history_dir /
        (
            "run_"
            +
            now.strftime(
                "%Y%m%d_%H%M%S"
            )
            +
            ".json"
        )
    )


    with open(
        history_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


    # =========================
    # очистка старых логов
    # =========================

    logs = sorted(
        history_dir.glob("run_*.json"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )


    for old_log in logs[MAX_LOG_HISTORY:]:

        old_log.unlink()


    return log_file