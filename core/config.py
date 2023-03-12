from decouple import config



class Setting():
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    DB_NAME = config('DB_NAME')
    SESSION_TYPE = "filesystem"
    DATABASE_URI =  f'sqlite:///{DB_NAME}'
    CKEDITOR = 'standard'






settings = Setting()

