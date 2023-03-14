import os
import uuid
from datetime import datetime

from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from core.config import settings
from core.database import create_db, db
from core.models import VirtualListeningParty, Room, User
from core.notifications import sendNotification, sendSMS, create_room, generate_token


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
            return redirect(url_for('reate_virtual_listening_party'))
    
        return render_template('register.html')

    # Route for creating a new virtual listening party
    @app.route('/create', methods=['GET', 'POST'])
    def create_virtual_listening_party():
        if request.method == 'POST':

            name = request.form['name']
            email = request.form['email']
            description = request.form['description']
            date = datetime.strptime(request.form['date'], '%Y-%m-%d %H:%M:%S')

            # Generate a unique identifier for the virtual listening party
            identifier = str(uuid.uuid4())


            if not all([name, email, description, date]):
                return render_template('create.html', msg="Some fields are missing")

            # create a unique event link
            event_link = f"/vlp/{identifier}"

            # Create the virtual listening party in the database
            new_vlp = VirtualListeningParty(name=name, email=email, description=description, date=date, link=event_link)
            db.session.add(new_vlp)
            db.session.commit() 
            
            # Create a room for the virtual listening party
            room_name = f"{name} Room"
            create_room(name=room_name)
           

            # Send a WhatsApp message to all registered users with a link to the virtual listening party

            users = User.query.all()
            for user in users:
                reciepent_no = user.phone_number

                msg = f"Join the virtual listening party {new_vlp.name} on {new_vlp.link}"
                sendNotification(user.phone_number, )

            #  Redirect the user to the virtual listening party page
            return redirect(url_for('virtual_listening_party', identifier=identifier))

        return render_template('create.html')

   
    
    @app.route('/vlp/<identifier>/join', methods=['POST'])
    def join_virtual_listening_party(identifier):

        if request.method == 'POST':
            name = request.form['name']
            phone_number = request.form['phone_number']

            # Find the virtual listening party by its identifier

            link = f"/vlp/{identifier}"
            
            vlp = VirtualListeningParty.query.filter_by(link=link).first()

            # Find the room for the virtual listening party
            room = Room.query.filter_by(vlp_id=vlp.id).first()

            # Create or update the user
            user = User.query.filter_by(phone_number=phone_number).first()
            if user:
                user.name = name
                user.vlp_id = vlp.id
                user.room_id = room.id
            else:
                user = User(name=name, phone_number=phone_number, vlp_id=vlp.id, room_id=room.id)
                db.session.add(user)
                db.session.commit()

            # Generate a Twilio access token for the user
            token = generate_token(room)

        # Render the join room template with the Access Token and room name
        return render_template('join_room.html', token=token.to_jwt().decode(), room_name=room.name)
            

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
            
            # send login notification
            msg = f"Ahoy!! A user login just happened on your account! Was this you?"
            sendNotification(user.phone, msg)
            return redirect(url_for('show'))



        session['user_id'] = user.id
        return render_template('login.html')
    


    @app.route('/logout', methods=['GET'])
    def logout():
        logout_user()
        return redirect(url_for("home"))


    



    return app
