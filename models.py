from flask_login import UserMixin
from . import conn

class User(UserMixin, conn.Model):
    __tablename__ = 'v_users'
    id = conn.Column(conn.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    user_email = conn.Column(conn.String(100), unique=True)
    user_pass = conn.Column(conn.String(100))
    display_name = conn.Column(conn.String(250))
