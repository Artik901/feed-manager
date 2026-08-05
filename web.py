from flask import (
    Flask,
    render_template,
    redirect,
    send_file,
    request,
    session,
    flash,
    url_for
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required
)

from app.auth import User, check_login
import subprocess
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
from app.description_manager import (
    load_description_settings,
    save_description_settings,
    clear_all_descriptions
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

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User(user_id)

def start_feed_update():

    try:
        subprocess.Popen(
            [
                "systemctl",
                "start",
                "feed-update.service"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception as e:
        print(
            "Ошибка запуска обновления:",
            e
        )
@app.context_processor
def inject_globals():

    return {
        "app_version": APP_VERSION,
        "shop_name": SHOP_NAME
    }

app.secret_key = SECRET_KEY

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )


        if check_login(
            username,
            password
        ):

            login_user(
                User(username)
            )

            session["user"] = username

            return redirect("/")


        return "Неверный логин или пароль", 401


    return render_template(
        "login.html"
    )



@app.route("/logout")
def logout():

    logout_user()

    session.clear()

    return redirect("/login")

# =========================
# Главная
# =========================

@app.route("/")
@login_required
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
@login_required
def run():

    main()

    return redirect("/")



# =========================
# Фиды
# =========================

@app.route("/feeds")
@login_required
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
@login_required
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
@login_required
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

    active_count = 0

    for category in categories.values():

        if category["percent"] > 0:
            active_count += 1


        for child in category["children"]:

            if child["percent"] > 0:
                active_count += 1

    return render_template(
    "settings.html",
    categories=categories,
    settings=current_settings,
    active_count=active_count
)
@app.route("/descriptions")
@login_required
def descriptions():

    current = load_description_settings()
    rules = {}


    for item in current.get("rules", []):

        rules[str(item["category_id"])] = item

    categories = {}

    xml = Path(
        SOURCE_XML
    )

    if xml.exists():

        root = load_xml(xml)

        all_categories = parse_categories(root)


        for cid, cat in all_categories.items():

            if not cat.get("parent"):

                categories[cid] = {

                    "id": cid,

                    "name": cat.get(
                        "name",
                        cid
                    ),

                    "before": rules.get(
                        str(cid),
                        {}
                    ).get(
                        "before",
                        ""
                    ),

                    "after": rules.get(
                        str(cid),
                        {}
                    ).get(
                        "after",
                        ""
                    ),

                    "children": []

                }



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

                    "before": rules.get(
                        str(cid),
                        {}
                    ).get(
                        "before",
                        ""
                    ),

                    "after": rules.get(
                        str(cid),
                        {}
                    ).get(
                        "after",
                        ""
                    )

                })



    return render_template(
        "descriptions.html",
        categories=categories,
        description_settings=current
    )

# =========================
# Сохранение настроек
# =========================

@app.route(
    "/settings/save",
    methods=["POST"]
)
@login_required
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


    current = load_settings()

    current["markup"] = rules

    save_settings(current)

    start_feed_update()

    return redirect(
        "/settings"
    )
@app.route("/settings/clear_markup", methods=["POST"])
@login_required
def clear_markup():

    current = load_settings()

    current["markup"] = []

    save_settings(current)

    start_feed_update()

    return redirect("/settings")

@app.route(
    "/descriptions/save",
    methods=["POST"]
)
@login_required
def save_descriptions_page():

    current = load_description_settings()


    rules = []


    # получаем все категории из формы
    for key in request.form:


        if key.startswith("before_"):

            category_id = key.replace(
                "before_",
                ""
            )


            before = request.form.get(
                key,
                ""
            ).strip()


            after = request.form.get(
                "after_" + category_id,
                ""
            ).strip()



            if before or after:


                rules.append(
                    {
                        "category_id": category_id,
                        "before": before,
                        "after": after,
                        "enabled": True
                    }
                )



    current["enabled"] = bool(rules)

    current["rules"] = rules


    save_description_settings(
        current
    )


    start_feed_update()


    return redirect(
        "/descriptions"
    )


@app.route("/descriptions/clear", methods=["POST"])
@login_required
def clear_descriptions():

    clear_all_descriptions()

    start_feed_update()

    flash(
        "Все описания очищены",
        "success"
    )

    return redirect(
        url_for("descriptions")
    )
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
