"""Flask app for Cupcakes API"""
from flask import Flask, request, jsonify, render_template,  redirect, flash, session
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


    @app.route('/api/cupcakes')
    def list_cupcakes():
        """Returns JSON payload w/ all cupcakes"""
        all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=all_cupcakes)


    @app.route('/api/cupcakes/<int:id>')
    def get_cupcake(id):
        """Returns JSON payload for one cupcake"""
        cupcake = Cupcake.query.get_or_404(id)
        return jsonify(cupcake=cupcake.serialize())


    @app.route('/api/cupcakes', methods=["POST"])
    def create_cupcake():
        """Creates a new cupcake and returns JSON payload of that created cupcake"""

        # determine whether request includes image_url
        if request.json.get('image_url'):
            new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], image_url=request.json["image_url"], rating=request.json["rating"])
        else:
            new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"])
        
        db.session.add(new_cupcake)
        db.session.commit()
        response_json = jsonify(cupcake=new_cupcake.serialize())

        # Return with a status code of 201 (Created) 
        return (response_json, 201)

    return app

if __name__ == '__main__':
    app = create_app('cupcakes', developing=True)
    app.app_context().push() # remove when done testing
    connect_db(app)
    app.run(debug=True)      # show when done testing