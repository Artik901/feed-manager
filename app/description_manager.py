import json
from pathlib import Path

from config.config import SETTINGS_FILE



def load_description_settings():

    if not Path(SETTINGS_FILE).exists():

        return {
            "enabled": False,
            "rules": []
        }


    with open(
        SETTINGS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)



    return data.get(
        "description",
        {
            "enabled": False,
            "rules": []
        }
    )





def save_description_settings(settings):

    with open(
        SETTINGS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)



    data["description"] = settings



    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )





def get_description_rule(category_id):

    settings = load_description_settings()


    if not settings.get("enabled"):

        return None



    for rule in settings.get("rules", []):


        if (
            str(rule.get("category_id"))
            ==
            str(category_id)
        ):


            if rule.get(
                "enabled",
                True
            ):

                return rule



    return None





def get_first_available_description_rule(category_ids):

    """
    Ищет первое подходящее правило.

    Приоритет:
    1. конкретная категория
    2. родительская категория
    3. выше по дереву

    Пример:

    [
        415,
        4,
        3
    ]

    сначала ищем 415,
    потом 4,
    потом 3
    """



    settings = load_description_settings()


    if not settings.get("enabled"):

        return None



    rules = settings.get(
        "rules",
        []
    )



    for category_id in category_ids:


        for rule in rules:



            if (
                str(rule.get("category_id"))
                ==
                str(category_id)
            ):


                if rule.get(
                    "enabled",
                    True
                ):

                    return rule



    return None

def clear_all_descriptions():

    settings = load_description_settings()


    settings["enabled"] = False

    settings["rules"] = []


    save_description_settings(
        settings
    )