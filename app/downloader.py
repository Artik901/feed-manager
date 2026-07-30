import requests
from pathlib import Path
from datetime import datetime

from lxml import etree

from config.config import (
    SOURCE_URL,
    SOURCE_XML,
    SOURCE_BACKUP_DIR,
    MAX_XML_BACKUPS
)


def download_feed():

    print("Загрузка XML с сервера...")


    response = requests.get(
    SOURCE_URL,
    timeout=(10, 120)
    )


    response.raise_for_status()


    content = response.content


    # проверяем что это XML
    try:

        etree.fromstring(
            content
        )

    except Exception:

        raise Exception(
            "Скачанный файл не является XML"
        )


    path = Path(
        SOURCE_XML
    )


    path.parent.mkdir(
        exist_ok=True
    )


    # резервные копии XML
    if path.exists():

        backup_dir = Path(
            SOURCE_BACKUP_DIR
        )

        backup_dir.mkdir(
            exist_ok=True
        )


        backup_file = (
            backup_dir /
            (
                "2gis_"
                +
                datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
                +
                ".xml"
            )
        )


        backup_file.write_bytes(
            path.read_bytes()
        )


        backups = sorted(
            backup_dir.glob("*.xml"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )


        for old_backup in backups[MAX_XML_BACKUPS:]:

            old_backup.unlink()


    # временная запись
    temp = path.with_suffix(
        ".tmp"
    )


    temp.write_bytes(
        content
    )


    # атомарная замена
    temp.replace(
        path
    )


    print(
        "XML загружен:",
        len(content),
        "байт"
    )


    return {
    "path": path,
    "size": len(content),
    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "backup": path.exists()
}