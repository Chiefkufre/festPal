from flask import Flask, redirect, render_template, Response, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from core.config import settings
from core.database import create_db, db
from core.models import User, Event


# create application instance
def create_app_instance():
    # initialize application
    app = Flask(__name__)
    app.config.from_object(settings)

    with app.app_context():
        # initialize database
        create_db(app)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            address = request.form.get("address")
            wsn = request.form.get("tel")
            password = request.form.get("password")
            bio = request.form.get("bio")
            register_as = request.form.get("register_as").strip()

        # check if all fields are include
        if not all([name, email, address, wsn, password]):
            return render_template("register.html", msg="some field are missing")

        # hash password to secure strings
        hash_pass = generate_password_hash(password)

        if hash_pass:
            password = hash_pass

        # create new user
        new_user = User(
            name=name,
            email=email,
            password=password,
            address=address,
            bio=bio,
            phone=wsn,
        )

        # store new user

        db.session.add(new_user)
        db.session.commit()

        # set user session
        session["user_id"] = new_user.id

        if register_as == "attendee":
            return rdirect(url_for("addImage"))
        else:
            return redirect(url_for("create_festival"))

        return render_template("register.html")

    @app.route("/create", methods=["GET", "POST"])
    def create_festival():
        user_id = session.get("user_id")

        if request.method == "POST":
            event_name = request.form.get("name")
            location = request.form.get("location")
            start_date = request.form.get("start")
            end_date = request.form.get("end")

        if not all([start_date, end_date, location, event_name]):
            return render_template("create.html", msg="Some fields are missing")

        # create new festival
        new_festival = Event(
            event_name=event_name,
            location=location,
            start_date=start_date,
            end_date=end_date,
        )

        # store into db
        db.session.add(new_festival)
        db.session.commit()

        # return to route to upload profile picture
        return redirect(url_for("addImage"))

    @app.route("/", methods=["GET", "POST"])
    def show():
        festival = []

        events = Event.query.all()
        for event in events:
            event_name = event.event_name
            location = event.location
            start_date = event.start_date
            end_date = event.end_date
            image = None

            if event.image_url != None:
                image = event.image_url

            data = {
                "eventName": event_name,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "image": image,
            }

            festival.append(data)
        return render_template("show.html", _payload=festival)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        session["user_id"] = user.id
        return render_template("login.html")

    @app.route("/login", methods=["GET"])
    def logout():
        return redirect(url_for("home"))

    @app.route("/create", methods=["GET", "POST"])
    def create_event():
        return render_template("create.html")

    return app
