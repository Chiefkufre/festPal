from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from core.config import settings 




# create application instance
def create_app_instance():

    # initialize application
    app = Flask(__name__)

    # add app configuration

    app.config["SECRET"] = settings.SECRET_KEY
    app.config['SESSION_TYPE'] = settings.SESSION_TYPE
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
    app.config['CKEDITOR_PKG_TYPE'] = settings.CKEDITOR

    # initialize database
    db = SQLAlchemy(app)
   



    
    return app


