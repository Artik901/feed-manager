from pathlib import Path
from lxml import etree
from datetime import datetime

from app.utils import translit
from app.parser import create_offer_xml

from config.config import (
    SHOP_NAME,
    SHOP_URL,
    FEEDS_DIR
)


def create_feed(
        offers,
        categories
):

    root = etree.Element(
        "yml_catalog",
        date=datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    )


    shop = etree.SubElement(
        root,
        "shop"
    )


    etree.SubElement(
        shop,
        "name"
    ).text = SHOP_NAME


    etree.SubElement(
        shop,
        "company"
    ).text = SHOP_NAME


    etree.SubElement(
        shop,
        "url"
    ).text = SHOP_URL


    currencies = etree.SubElement(
        shop,
        "currencies"
    )


    etree.SubElement(
        currencies,
        "currency",
        id="RUB",
        rate="1"
    )


    feed_categories = get_feed_categories(
        offers,
        categories
    )


    add_categories(
        shop,
        feed_categories
    )


    add_offers(
        shop,
        offers
    )


    return etree.ElementTree(root)



def get_feed_categories(
        offers,
        categories
):

    result = {}


    for offer in offers:

        current = str(
            offer.get("category_id")
        )


        while current:


            if current in result:
                break


            category = categories.get(
                current
            )


            if not category:
                break


            result[current] = category


            parent = category.get(
                "parent"
            )


            if parent:

                current = str(parent)

            else:

                break


    return result



def add_categories(
        shop,
        categories
):

    node = etree.SubElement(
        shop,
        "categories"
    )


    def category_depth(cat_id):

        depth = 0

        parent = categories[cat_id].get(
            "parent"
        )


        while parent:

            depth += 1

            parent_cat = categories.get(
                str(parent)
            )


            if not parent_cat:
                break


            parent = parent_cat.get(
                "parent"
            )


        return depth



    for cat_id in sorted(
        categories.keys(),
        key=category_depth
    ):

        cat = categories[cat_id]


        category = etree.SubElement(
            node,
            "category",
            id=str(cat_id)
        )


        if cat.get("parent"):

            category.set(
                "parentId",
                str(cat["parent"])
            )


        category.text = cat["name"]



def add_offers(
        shop,
        offers
):

    node = etree.SubElement(
        shop,
        "offers"
    )


    for item in offers:

        xml = create_offer_xml(
            item
        )


        node.append(
            xml
        )



def save_feed(
        tree,
        category
):

    folder = Path(
        FEEDS_DIR
    )


    folder.mkdir(
        exist_ok=True
    )


    filename = (
        translit(category)
        +
        ".xml"
    )


    final = folder / filename


    temp = folder / (
        filename +
        ".tmp"
    )


    tree.write(
        temp,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
    )


    parsed = etree.parse(
        temp
    )


    offers = parsed.xpath(
        ".//offer"
    )


    if not offers:

        raise Exception(
            "Создан пустой feed"
        )


    temp.replace(
        final
    )


    return final