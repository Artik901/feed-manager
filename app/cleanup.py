from pathlib import Path

from config.config import (
    SOURCE_BACKUP_DIR,
    MAX_XML_BACKUPS,
    LOG_HISTORY_DIR,
    MAX_LOG_HISTORY
)


def cleanup_storage():

    # очистка XML backup
    backup_dir = Path(
        SOURCE_BACKUP_DIR
    )

    if backup_dir.exists():

        backups = sorted(
            backup_dir.glob("*.xml"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )


        for old_file in backups[MAX_XML_BACKUPS:]:

            try:
                old_file.unlink()

            except Exception:
                pass


    # очистка истории логов
    history_dir = Path(
        LOG_HISTORY_DIR
    )

    if history_dir.exists():

        logs = sorted(
            history_dir.glob("*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )


        for old_log in logs[MAX_LOG_HISTORY:]:

            try:
                old_log.unlink()

            except Exception:
                pass