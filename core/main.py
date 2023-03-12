from flask import Flask, redirect, render_template, request, session, url_for




# create application instance
def create_app_instance():
    app = Flask(__name__)
    app.config["SECRET"] = "notSoSecureKey"app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://quhndgozyzmwjb:615fdb6698b586d74a24c659dd67396f7b06c4d47e41faa28e5a77400231242e@ec2-52-4-104-184.compute-1.amazonaws.com:5432/d86porjmrvj6ar'
    # db = SQLAlchemy(app)
    app.config['CKEDITOR_PKG_TYPE'] = 'standard'
    # db.init_app(app)
    # ckeditor.init_app(app)











    return app


