from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
from datetime import datetime


# User Class for ORM
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), index=True, unique=True)
    first_name = db.Column(db.String(250), index=True)
    dob = db.Column(db.DateTime, index=True)
    deriv_date = db.Column(db.DateTime, index=True)
    password_hash = db.Column(db.String(128))
    superuser = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return

        return User.query.get(id)

    def __repr__(self):
        return '<User: {} {} ({})>'.format(self.first_name,
                                           self.dob.strftime('%m/%d/%Y'), self.email)


# Set the user id to track the user currently online
@login.user_loader
def load_user(id):
	return User.query.get(int(id))


# Articles
class Article(db.Model):
    __tablename__='articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    subtitle = db.Column(db.String(500))
    body = db.Column(db.String(20000))
    author = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Post {}>".format(self.title)
