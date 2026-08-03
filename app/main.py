from datetime import datetime

from app.cleanup import cleanup_storage
from app.downloader import download_feed
from app.feed_builder import (
    create_feed,
    save_feed
)
from app.logger import save_run_log
from app.markup import apply_markup
from app.description import apply_description

from app.parser import (
    load_xml,
    parse_categories,
    parse_offers,
    group_by_root_category
)

from app.validator import validate_settings


def main():

    start_time = datetime.now()

    success = 0
    generated_total = 0
    generated_feeds = []
    errors = []
    offers = []
    categories = {}


    try:


        download_result = download_feed()

        xml_file = download_result["path"]


        cleanup_storage()


        root = load_xml(xml_file)


        print("Анализ категорий...")


        categories = parse_categories(root)


        validate_settings(categories)


        print(
            "Категорий найдено:",
            len(categories)
        )



        offers = parse_offers(
            root,
            categories
        )


        print(
            "Товаров найдено:",
            len(offers)
        )



        print(
            "Применение правил наценки и описаний..."
        )



        for offer in offers:



            apply_markup(
                offer,
                categories
            )



            category_chain = offer.get(
                "category_path_ids",
                []
            )



            apply_description(
                offer,
                category_chain
            )





        groups = group_by_root_category(
            offers
        )



        print()

        print(
            "Создание полноценных фидов"
        )

        print("================")




        for category, products in groups.items():


            try:



                tree = create_feed(
                    products,
                    categories
                )



                filename = save_feed(
                    tree,
                    category
                )



                generated_total += len(products)



                print(
                    filename,
                    "-",
                    len(products),
                    "товаров"
                )



                generated_feeds.append(
                    {
                        "name": category,
                        "slug": filename.stem,
                        "offers": len(products),
                        "file": str(filename)
                    }
                )



                success += 1




            except Exception as e:



                print(
                    "ОШИБКА:",
                    category,
                    e
                )


                errors.append(
                    {
                        "category": category,
                        "error": str(e)
                    }
                )





        print()



        if generated_total != len(offers):


            print(
                "ОШИБКА ПРОВЕРКИ!"
            )


            print(
                "Источник:",
                len(offers)
            )


            print(
                "Создано:",
                generated_total
            )


            errors.append(
                {
                    "category": "CHECK",
                    "error": "Количество товаров не совпадает"
                }
            )



        else:


            print(
                "Проверка товаров: OK"
            )





        print()

        print("================")

        print("Готово")

        print("================")



        print(
            "Создано фидов:",
            success
        )



        print(
            "Всего товаров:",
            len(offers)
        )



        status = (
            "success"
            if not errors
            else "error"
        )





    except Exception as e:



        status = "error"



        print()

        print(
            "КРИТИЧЕСКАЯ ОШИБКА"
        )


        print(e)



        errors.append(
            {
                "category": "SYSTEM",
                "error": str(e)
            }
        )





    finally:



        duration_seconds = (
            datetime.now() - start_time
        ).total_seconds()



        duration = (
            f"{duration_seconds:.2f} сек"
        )



        save_run_log(
            status=status,
            source_offers=len(offers),
            categories_count=len(categories),
            generated_feeds=success,
            generated_offers=generated_total,
            feeds=generated_feeds,
            errors=errors,
            duration=duration
        )





if __name__ == "__main__":

    main()