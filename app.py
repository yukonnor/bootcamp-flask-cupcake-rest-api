"""Flask app for Cupcakes API"""
from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, Cupcake

def create_app(db_name, testing=False, developing=False):

    app = Flask(__name__)
    app.testing = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
    app.config['SECRET_KEY'] = "chickenzarecool21837"

    if developing: 
        app.config['SQLALCHEMY_ECHO'] =  True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    return app

if __name__ == '__main__':
    app = create_app('blogly', developing=True)
    app.app_context().push() # remove when done testing
    connect_db(app)
    app.run(debug=True)      # show when done testing