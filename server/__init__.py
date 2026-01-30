from flask import Flask
from .extensions import db

def create_app():
    app=Flask(__name__)
    # initialize the app with the extension
    db.init_app(app)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Flask app is working !'
    return app