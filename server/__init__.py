from flask import Flask
from server.models import db
from .config import Config 

def create_app():

    #Create flask app instance 
    app=Flask(__name__)

    #Load configurations 
    app.config.from_object(Config)

    # initialize extensions 
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Flask app is working !'
    return app