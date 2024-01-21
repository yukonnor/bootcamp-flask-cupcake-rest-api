"""Models for Cupcake API."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

DEFAULT_IMG = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    flavor = db.Column(db.String(50),  # string with max len of 50 chars
                     nullable=False)
    
    size = db.Column(db.String(50),  # string with max len of 50 chars
                     nullable=False)
    
    rating = db.Column(db.Float,  
                     nullable=False)

    image_url = db.Column(db.String(200), 
                          nullable=False,
                          default=DEFAULT_IMG)

    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.now())

    @classmethod
    def get_default_image(cls):
        return DEFAULT_IMG

    def __repr__(self):
        s = self
        return f"<Cupcake id={s.id} flavor={s.flavor} size={s.size}>"
    
    def serialize(self):
        """Returns a dict representation of cupcake which we can turn into JSON"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image_url': self.image_url,
            'created_at': self.created_at
        }
