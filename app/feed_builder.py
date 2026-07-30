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


    add_categories(
        shop,
        categories
    )


    add_offers(
        shop,
        offers
    )


    return etree.ElementTree(root)





def add_categories(
        shop,
        categories
):

    node = etree.SubElement(
        shop,
        "categories"
    )


    for cat_id, cat in categories.items():

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
        xml = create_offer_xml(item)
        node.append(
            xml
        )


def save_feed(
        tree,
        category
):

    folder = Path(FEEDS_DIR)

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


    parsed = etree.parse(temp)

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