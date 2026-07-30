from app.main import main
import traceback


if __name__ == "__main__":

    try:

        main()

        print("OK: обновление завершено")


    except Exception as e:

        print("ERROR:")
        print(e)

        traceback.print_exc()

        raise