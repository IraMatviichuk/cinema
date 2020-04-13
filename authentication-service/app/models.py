from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

from app import db


class CinemaUser(db.Model):
    __tablename__ = "cinema_user"

    cinema_user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password, firstname, lastname):
        self.username = username
        self.password = generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return (
            f"<CinemaUser: (cinema_user_id={self.cinema_user_id}, username={self.username}, "
            f"password={self.password}, firstname={self.firstname}, lastname={self.lastname})>"
        )
    
    def to_dict(self):
        return {
            "cinema_user_id": self.cinema_user_id,
            "username": self.username,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
        }

    # @validates("username")
    # @validates("password")
    # @validates("firstname")
    # @validates("lastname")

    def verify_password(self, password_to_check):
        return check_password_hash(self.password, password_to_check)