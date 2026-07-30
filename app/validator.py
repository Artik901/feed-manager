import json
from pathlib import Path

from config.config import SETTINGS_FILE


def validate_settings(categories):

    print("Проверка settings.json...")

    path = Path(SETTINGS_FILE)

    if not path.exists():
        raise Exception("Файл settings.json не найден")

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    markup = data.get("markup")

    if markup is None:
        raise Exception("В settings.json отсутствует раздел markup")

    if not isinstance(markup, list):
        raise Exception("markup должен быть списком")

    for item in markup:

        if "category_id" not in item:
            raise Exception("Не указан category_id")

        if "percent" not in item:
            raise Exception(
                f'Для категории {item["category_id"]} отсутствует percent'
            )

        category_id = str(item["category_id"])

        if category_id not in categories:
            raise Exception(
                f"Категория {category_id} отсутствует в XML"
            )

        percent = item["percent"]

        if not isinstance(percent, (int, float)):
            raise Exception(
                f"percent для категории {category_id} должен быть числом"
            )

    print("settings.json корректен")