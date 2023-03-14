from flask import (Flask, Response, redirect, render_template, request,
                   session, url_for, flash)
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from core.config import settings
from core.database import create_db, db
from core.models import Event, User


# create application instance
def create_app_instance():
    # initialize application
    app = Flask(__name__)
    app.config.from_object(settings)

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():
        # initialize database
        create_db(app)

    

    @app.route('/register', methods=['GET', 'POST'])
    def register():

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            address = request.form.get('address')
            wsn = request.form.get('tel')
            password = request.form.get('password')
            bio = request.form.get('bio')
            register_as = request.form.get('register_as').strip()
        
        # check if all fields are include
        if not all([name, email,address,wsn,password]):
            return render_template("register.html", msg="some field are missing")


        # hash password to secure strings
        hash_pass = generate_password_hash(password)

        if hash_pass:
            password = hash_pass


        # create new user
        new_user = User(name=name, email=email, password=password, address=address, bio=bio, phone=wsn)

        # store new user

        db.session.add(new_user)
        db.session.commit()

        # set user session
        session['user_id'] = new_user.id


        if register_as == 'attendee':
            return redirect(url_for("addImage"))
        else:
            return redirect(url_for('create_festival'))
    
        return render_template('register.html')
    

    @app.route('/create', methods=['GET','POST'])
    def create_festival():

    
        if request.method == 'POST':
            event_name = request.form.get("name")
            location = request.form.get("location")
            start_date = request.form.get("start")
            end_date = request.form.get("end")
        
        user = current_user

        user_type = user.register_as

        if user_type == "attendees":
            flash("You can create an event. Please register as an evnt host")
            return redirect(url_for("register"))


        if not all([start_date, end_date, location, event_name]):
            return render_template('create.html', msg="Some fields are missing")
        

        # create new festival
        new_festival = Event(event_name=event_name, location=location, start_date=start_date, end_date=end_date)


        # store into db
        db.session.add(new_festival)
        db.session.commit()


        # return to route to upload profile picture
        return redirect(url_for("addImage"))
    


    @app.route('/', methods=['GET', 'POST'])
    def show():

        festival = []

        events = Event.query.all()
        for event in events:
            event_name = event.event_name
            location = event.location
            start_date = event.start_date
            end_date = event.end_date
            image = None;

            if event.image_url != None:
                image = event.image_url
            
            data = {
                "eventName": event_name,
                "location": location,
                "start_date": start_date,
                "end_date": end_date,
                "image": image
            }
        
            festival.append(data)
        return render_template('show.html', _payload=festival)


    # Login routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():

        email = request.form.get('email')
        password = request.form.get('password')

        # query user from database
        user = User.query.filter(User.email == email).first()

        if user is None:
            return render_template('login.html', msg="user not found")
        
        # check if user password is correct
        check_pass = check_password_hash(user.password, password)

        if user and check_pass:

            login_user(user)

            return redirect(url_for('show'))



        session['user_id'] = user.id
        return render_template('login.html')
    


    @app.route('/logout', methods=['GET'])
    def logout():
        logout_user()
        return redirect(url_for("home"))


    



    return app
