from datetime import datetime

from sqlalchemy.types import Boolean

from core.database import db



# User model that represents a user data
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.String(50), unique=False)
    profile_picture = db.Column(db.String(255))
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(Boolean, default=True)
    event = db.relationship("Event", backref="user", lazy=True)
    

    


# Event model that represents events state
class Event(db.Model):

    __tablename__ = 'events'

    id  = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    host = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

