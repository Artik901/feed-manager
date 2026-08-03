from lxml import etree
from copy import deepcopy

def load_xml(filename):
    """
    Загружает XML файл
    """

    tree = etree.parse(filename)
    root = tree.getroot()

    return root


def parse_categories(root):
    """
    Создает словарь категорий
    """

    categories = {}

    for category in root.xpath(".//category"):

        category_id = category.get("id")

        if not category_id:
            continue

        categories[category_id] = {
            "name": category.text.strip(),
            "parent": category.get("parentId")
        }

    return categories


def count_offers(root):
    """
    Количество товаров
    """

    offers = root.xpath(".//offer")

    return len(offers)


def get_root_categories(categories):
    """
    Получаем верхние категории
    """

    result = []

    for cat_id, cat in categories.items():

        if not cat["parent"]:
            result.append(cat["name"])

    return result

def get_category_path(category_id, categories):

    path = []

    current_id = category_id

    visited = set()


    while current_id:


        if current_id in visited:
            break


        visited.add(current_id)


        category = categories.get(
            str(current_id)
        )

        if not category:
            break


        path.append(
            category["name"]
        )


        current_id = category["parent"]


    return path

def get_category_id_path(category_id, categories):

    path = []

    current_id = category_id

    visited = set()


    while current_id:


        if current_id in visited:
            break


        visited.add(current_id)


        category = categories.get(
            str(current_id)
        )


        if not category:
            break


        path.append(
            str(current_id)
        )


        current_id = category["parent"]


    return path

def show_first_offer(root):
    """
    Показывает первый товар из XML
    """

    offers = root.xpath(".//offer")

    if not offers:
        print("Товары не найдены")
        return


    offer = offers[0]


    print()
    print("ПЕРВЫЙ ТОВАР")
    print("================")


    for child in offer:

        print(
            child.tag,
            "=",
            child.text
        )

def parse_offers(root, categories):

    result = []

    for offer in root.xpath(".//offer"):

        data = {
            "xml": deepcopy(offer),
            "id": offer.get("id"),
            "available": offer.get("available")
        }


        for child in offer:

            if len(child):
                continue

            data[child.tag] = child.text


        category_id = data.get("categoryId")

        if category_id:

            path = get_category_path(
                category_id,
                categories
            )
            id_path = get_category_id_path(
                category_id,
                categories
        )

            data["category_id"] = category_id

            data["category_path"] = path

            data["category_path_ids"] = id_path
            print(
                "CATEGORY IDS:",
                id_path
            )

            if path:
                data["root_category"] = path[-1]


        result.append(data)


    return result

def group_by_root_category(offers):
    """
    Группировка товаров по верхней категории
    """

    groups = {}

    for offer in offers:

        root = offer.get("root_category")

        if not root:
            continue


        if root not in groups:
            groups[root] = []


        groups[root].append(offer)


    return groups

def create_offer_xml(data):
    """
    Создает XML offer из словаря товара
    """

    offer = etree.Element(
        "offer",
        id=str(data.get("id", "")),
        available=str(data.get("available", "false"))
    )


    for key, value in data.items():

        if key in (
            "xml",
            "id",
            "available",
            "category_path",
            "category_path_ids",
            "root_category",
            "category_id"
        ):
            continue


        if value is None:
            continue


        # если это уже XML элемент
        if isinstance(value, etree._Element):

            offer.append(
                deepcopy(value)
            )

        else:

            element = etree.SubElement(
                offer,
                key
            )

            element.text = str(value)


    return offer

def get_offer_category(data):
    
    return {
        "id": data.get("category_id"),
        "path": data.get("category_path", []),
        "root": data.get("root_category")
    }