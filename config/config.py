from pathlib import Path
import os

# =========================
# Базовая директория проекта
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Storage
# =========================

STORAGE_DIR = (
    BASE_DIR /
    "storage"
)


# =========================
# Исходный XML
# =========================

SOURCE_XML = (
    STORAGE_DIR /
    "source" /
    "2gis.xml"
)


SOURCE_BACKUP_DIR = (
    STORAGE_DIR /
    "source" /
    "backups"
)


# =========================
# Фиды
# =========================

FEEDS_DIR = (
    STORAGE_DIR /
    "feeds"
)


# =========================
# Логи
# =========================

LOG_FILE = (
    STORAGE_DIR /
    "logs" /
    "last_run.json"
)


LOG_HISTORY_DIR = (
    STORAGE_DIR /
    "logs" /
    "history"
)


MAX_LOG_HISTORY = 10


# =========================
# Настройки наценок
# =========================

SETTINGS_FILE = (
    BASE_DIR /
    "config" /
    "settings.json"
)


# =========================
# Резервные копии XML
# =========================

MAX_XML_BACKUPS = 5



# =========================
# Источник данных
# =========================

SOURCE_URL = (
    "https://my.advantshop.net/"
    "435975-urqg/export/2gis.xml"
)



# =========================
# Магазин
# =========================

SHOP_NAME = (
    "Большой папа"
)


SHOP_URL = (
    "https://bpapa.ru"
)


SECRET_KEY = os.environ.get(
    "FEED_MANAGER_SECRET_KEY",
    "8f4c2d9a7e6b1f5c3a9d0e7b4f6c8a2e"
)

APP_VERSION = "1.0.0"

DEBUG = False

# =========================
# Создание директорий
# =========================

DIRECTORIES = [

    STORAGE_DIR,

    STORAGE_DIR / "source",

    SOURCE_BACKUP_DIR,

    FEEDS_DIR,

    STORAGE_DIR / "logs",

    LOG_HISTORY_DIR,

]


for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )
