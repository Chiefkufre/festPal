from flask import Flask, redirect, render_template, Response, request, session, url_for

from core.config import settings
from core.database import create_db


# create application instance
def create_app_instance():
    # initialize application
    app = Flask(__name__)
    app.config.from_object(settings)

    with app.app_context():
        # initialize database
        create_db(app)



    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('show.html')

    

    @app.route('/register', methods=['GET', 'POST'])
    def register():

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            address = request.form.get('address')
            wsn = request.form.get('tel')
            password = request.form.get('password')
        
       
        if not all([name, email,address,wsn,password]):
            return render_template("register.html", msg="some field are missing")

        


        


        return render_template('register.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')
    


    @app.route('/login', methods=['GET'])
    def logout():
        return redirect(url_for("home"))


    @app.route('/create', methods=['GET','POST'])
    def create_event():
        return render_template('create.html')















    return app
