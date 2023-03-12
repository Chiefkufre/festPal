import os
from flask_sqlalchemy import SQLAlchemy
from core.config import settings

db = SQLAlchemy()
DB_NAME = settings.DB_NAME


# create database based on the model defined.
def create_db(app):
    # Check if the database file exists
    if not os.path.exists("core" + DB_NAME):
        # Set the application for the SQLAlchemy object
        db.app = app
        # Initialize the SQLAlchemy object with the applicatio
        db.init_app(app)
        # Create the database tables based on the defined models
        db.create_all()
