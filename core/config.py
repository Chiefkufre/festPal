from decouple import config
from pathlib import Path


# Use this to build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Setting:
    DEBUG = config("DEBUG", default=False, cast=bool)
    SECRET_KEY = config("SECRET_KEY")
    SESSION_TYPE = "filesystem"

    # database settings
    DB_NAME = config("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    CKEDITOR_PKG_TYPE = "standard"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # path to store images
    UPLOAD_FOLDER = "static/images"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # static fir directory
    STATIC_FOLDER: Path = BASE_DIR / "static"

    # templates directory
    TEMPLATES_FOLDER: Path = BASE_DIR / "templates"


settings = Setting()
