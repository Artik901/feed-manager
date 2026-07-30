import platform
import sys


APP_NAME = "Feed Manager"

APP_VERSION = "1.0.0"


def get_system_info():

    return {

        "app": APP_NAME,

        "version": APP_VERSION,

        "python": sys.version.split()[0],

        "platform": platform.system(),

        "platform_version": platform.version()

    }