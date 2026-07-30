import json
from pathlib import Path

from config.config import SETTINGS_FILE



def load_markup_rules():

    if not Path(SETTINGS_FILE).exists():

        return []


    with open(
        SETTINGS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)


    return data.get(
        "markup",
        []
    )



def get_markup_rules():

    return load_markup_rules()



def find_markup(
        category_id,
        categories
):

    current = str(category_id)

    visited = set()


    rules = get_markup_rules()



    while current:


        if current in visited:
            break


        visited.add(current)



        for rule in rules:


            rule_id = str(
                rule["category_id"]
            )


            if rule_id == current:


                percent = rule.get(
                    "percent",
                    0
                )


                return (
                    1 +
                    percent / 100
                )



        category = categories.get(
            current
        )


        if not category:
            break



        current = category.get(
            "parent"
        )



    return 1.0




def apply_markup(
        offer,
        categories
):


    coefficient = find_markup(
        offer.get("category_id"),
        categories
    )


    offer["markup"] = coefficient



    if coefficient == 1.0:

        return offer



    price = offer.get(
        "price"
    )


    if not price:

        return offer



    try:


        old_price = float(
            price
        )


        offer["price"] = str(
            round(
                old_price * coefficient
            )
        )


    except Exception:

        pass



    return offer