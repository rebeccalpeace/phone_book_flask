from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 

# Users should have a one to many relationship with the Address (each user can be related to many addresses,
#  but each address can only have one user)

# users should only be able to add addresses if they are logged in

# users should be able to view all of the addresses that they created, but only theirs, not other users. 

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in ('name', 'phone_number', 'address'):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    addresses = db.relationship('Address', backref='book_user', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)