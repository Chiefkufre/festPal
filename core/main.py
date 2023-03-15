import os
import uuid
from datetime import datetime

from flask import (Flask, Response, flash, redirect, render_template, request,
                   session, url_for, jsonify)
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

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))



    @app.route('/register', methods=['GET'])
    def return_register_form():
        return render_template('register.html')

    @app.route('/register', methods=['POST'])
    def register():


        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            wsn = request.form.get('phone')
            password = request.form.get('password')

         # check if all required fields are present
        if not (name and email and wsn and password):
            return render_template("register.html", msg="Some fields are missing")

        emailObj = User.query.filter(User.email==email).first()

        if emailObj:
            flash("user already exist")
            return redirect(url_for("login"))
        # hash password to secure string

        hash_pass = generate_password_hash(password)

        # check if hashing was successful
        if hash_pass is not None:
            password = hash_pass
        else:
            return render_template("register.html", msg="Password hashing failed")

        # create new user
        new_user = User(name=name, email=email, password=password, phone_number=wsn)

        # store new user
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

 


    # Route for creating a new virtual listening party
    @app.route('/create', methods=['GET', 'POST'])
    def create_virtual_listening_party():
        if request.method == 'POST':

            name = request.form['name']
            description = request.form['description']
            date_string = request.form['date']

            # Generate a unique identifier for the virtual listening party
            identifier = str(uuid.uuid4())

            # create a unique event link
            event_link = f"/vlp/{identifier}"

            # Create the virtual listening party in the database
            date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M')
            new_vlp = VirtualListeningParty(name=name, description=description, date=date, link=event_link)
            db.session.add(new_vlp)
            db.session.commit() 
            
            # Create a room for the virtual listening party
            room_name = f"{name} Room"

            # This function calls twilio api to create room
            create_room(room_name)
           

            # Send a WhatsApp message to all registered users with a link to the virtual listening party

            users = User.query.all()
            for user in users:
                reciepent_no = user.phone_number

                msg = f"Join the virtual listening party {new_vlp.name} on {new_vlp.link}"
                sendNotification(user.phone_number, msg)

            #  Redirect the user to the virtual listening party page
            return redirect(url_for('show_virtual_parties'))

        return render_template('create.html')

   
    
    @app.route('/vlp/<identifier>/join', methods=['GET','POST'])
    def join_virtual_listening_party(identifier):
        # Find the virtual listening party by its identifier
        link = f"/vlp/{identifier}"

        vlp = VirtualListeningParty.query.filter_by(link=link).first()

        if vlp:
            # Find the room for the virtual listening party
            room = Room.query.filter_by(vlp_id=vlp.id).first()

            if room:
                # Generate a Twilio access token for the user
                token = generate_token(room.name, room.sid)

                # Render the join room template with the Access Token and room name
                return render_template('room.html', token=token, room_name=room.name)
            else:
                # Room not found
                return "Room not found"
        else:
            # VirtualListeningParty not found
            return "VirtualListeningParty not found"
        
        return render_template('room.html', room=room)

            

    # route to display virtual party 
    @app.route('/')
    def show_virtual_parties():

        now = datetime.utcnow()

        active_parties = VirtualListeningParty.query.filter(VirtualListeningParty.date <= now).all()

        upcoming_parties = VirtualListeningParty.query.filter(VirtualListeningParty.date > now).all()

        active_parties_list = []

        for party in active_parties:
            party_info = {
                'id': party.id,
                'name': party.name,
                'description': party.description,
                'date': party.date.isoformat(),
                'link': party.link,
            }
            active_parties_list.append(party_info)

        upcoming_parties_list = []
        for party in upcoming_parties:
            party_info = {
                'id': party.id,
                'name': party.name,
                'description': party.description,
                'date': party.date.isoformat(),
                'link': party.link,
            }
            upcoming_parties_list.append(party_info)
        

        # Send whatsapp messages of all upcoming parties to users
        users = User.query.all()
        for user in users:
            reciepent_no = user.phone_number

            msg = f"Ahoy!! Keep up with all upcoming parties. Visit our website to see more"
            sendNotification(user.phone_number, msg)

        return render_template('show.html', active_parties = active_parties_list, upcoming_parties = upcoming_parties_list)
        
      

    # Login routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():

        email = request.form.get('email')
        password = request.form.get('password')

        # query user from database
        user = User.query.filter(User.email == email).first()

        if user is None:
            flash("user not found")
            return render_template('login.html')
        
        # check if user password is correct
        check_pass = check_password_hash(user.password, password)

        if user and check_pass:

            login_user(user)
            
            # send login notification
            msg = f"Ahoy!! A user login just happened on your account! Was this you?"
            sendNotification(user.phone_number, msg)
            return redirect(url_for('show_virtual_parties'))

        return render_template('login.html')
    


    @app.route('/logout', methods=['GET'])
    def logout():
        logout_user()
        return redirect(url_for("login"))


    



    return app
