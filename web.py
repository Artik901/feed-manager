from flask import Flask, render_template, redirect, send_file, request
from pathlib import Path
import json


from app.main import main

from app.log_reader import (
    get_history
)

from app.parser import (
    load_xml,
    parse_categories
)

from app.settings_manager import (
    load_settings,
    save_settings
)
from config.config import (
    DEBUG,
    LOG_FILE,
    SOURCE_XML,
    SECRET_KEY,
    APP_VERSION,
    SHOP_NAME
)



app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

@app.context_processor
def inject_globals():

    return {
        "app_version": APP_VERSION,
        "shop_name": SHOP_NAME
    }

app.secret_key = SECRET_KEY


# =========================
# Главная
# =========================

@app.route("/")
def index():

    log = None

    file = Path(LOG_FILE)

    if file.exists():

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            log = json.load(f)


    return render_template(
        "index.html",
        log=log
    )



# =========================
# Запуск обновления
# =========================

@app.route("/run")
def run():

    main()

    return redirect("/")



# =========================
# Фиды
# =========================

@app.route("/feeds")
def feeds():

    data = []

    file = Path(LOG_FILE)

    if file.exists():

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            log = json.load(f)

            data = log.get(
                "feeds",
                []
            )


    return render_template(
        "feeds.html",
        feeds=data
    )



@app.route("/feed/<slug>")
def open_feed(slug):

    file = Path(
        "storage/feeds"
    ) / (
        slug + ".xml"
    )


    if file.exists():

        return send_file(
            file,
            mimetype="application/xml"
        )


    return "Фид не найден", 404



# =========================
# История
# =========================

@app.route("/history")
def history():

    logs = get_history()

    return render_template(
        "history.html",
        logs=logs
    )



# =========================
# Настройки
# =========================

@app.route("/settings")
def settings():

    current_settings = load_settings()


    rules = {}


    for item in current_settings.get("markup", []):

        rules[str(item["category_id"])] = item



    categories = {}


    xml = Path(
        SOURCE_XML
    )


    if xml.exists():


        root = load_xml(xml)


        all_categories = parse_categories(
            root
        )



        # родители

        for cid, cat in all_categories.items():


            if not cat.get("parent"):


                categories[cid] = {

                    "id": cid,

                    "name": cat.get(
                        "name",
                        cid
                    ),

                    "percent": rules.get(
                        str(cid),
                        {}
                    ).get(
                        "percent",
                        0
                    ),

                    "children": []

                }



        # дети

        for cid, cat in all_categories.items():


            parent = str(
                cat.get("parent")
            )


            if parent in categories:


                categories[parent]["children"].append({

                    "id": cid,

                    "name": cat.get(
                        "name",
                        cid
                    ),

                    "percent": rules.get(
                        str(cid),
                        {}
                    ).get(
                        "percent",
                        0
                    )

                })




    # активные категории наверх

    def sort_key(item):

        data = item[1]


        child_active = any(
            c["percent"] > 0
            for c in data["children"]
        )


        return not (
            data["percent"] > 0
            or child_active
        )



    categories = dict(
        sorted(
            categories.items(),
            key=sort_key
        )
    )



    return render_template(
        "settings.html",
        categories=categories,
        settings=current_settings
    )

# =========================
# Сохранение настроек
# =========================

@app.route(
    "/settings/save",
    methods=["POST"]
)
def save_settings_page():


    category_ids = request.form.getlist(
        "category_id"
    )


    percents = request.form.getlist(
        "percent"
    )


    rules = []


    for i, category_id in enumerate(category_ids):


        value = percents[i].strip()


        if value == "":

            percent = 0

        else:

            percent = int(value)


        if percent > 0:


            rules.append(

                {
                    "category_id": category_id,

                    "percent": percent,

                    "enabled": True
                }

            )


    save_settings(

        {
            "markup": rules
        }

    )


    return redirect(
        "/settings"
    )
@app.route("/settings/clear_markup", methods=["POST"])
def clear_markup():

    save_settings(
        {
            "markup": []
        }
    )

    return redirect("/settings")

@app.route("/health")
def health():

    return {
        "status": "ok",
        "service": "feed-manager",
        "version": APP_VERSION,
        "shop": SHOP_NAME
    }

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=DEBUG
    )