from flask import Flask, redirect, render_template, request, session, url_for




# create application instance
def create_app_instance():
    app = Flask(__name__)
    app.config["SECRET"] = "notSoSecureKey"




    





    return app


