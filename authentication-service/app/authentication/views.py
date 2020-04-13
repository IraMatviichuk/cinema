from datetime import datetime, timedelta
from functools import wraps

from flask import jsonify, request, make_response, current_app
import jwt

from . import authentication
from .. import db
from ..models import CinemaUser


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({
                "messane": "token is missing"
            })

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"])
            current_cinema_user = CinemaUser.query.filter_by(cinema_user_id=data.get("public_id")).first()
        except:
            return jsonify({
                "message": "token is invalid"
            })

        return f(*args, **kwargs)
    return decorator


@authentication.route("/register", methods=["POST"])
def register():
    auth_data = request.get_json()
    cinema_user = CinemaUser(
        username=auth_data.get("username"),
        password=auth_data.get("password"),
        firstname=auth_data.get("firstname"),
        lastname=auth_data.get("lastname"),
    )

    db.session.add(cinema_user)
    db.session.commit()

    return jsonify({
        "status": "OK",
        "message": "registered successfully",
    })


@authentication.route("/login", methods=["GET"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("could not verify", 401, {"WWW.Authentication": "login required"})
    
    cinema_user = CinemaUser.query.filter_by(username=auth.username).first()

    if cinema_user.verify_password(auth.password):
        token = jwt.encode({
            "public_id": cinema_user.cinema_user_id,
            "exp": datetime.utcnow() + timedelta(minutes=5),
        }, current_app.config["SECRET_KEY"])

        return jsonify({"token": token.decode("UTF-8")})

    return make_response("could not verify", 401, {"WWW.Authentication": "login required"})


@authentication.route("/test1/", methods=["GET"])
@token_required
def test1():
    return jsonify({"test": "successful"})


@authentication.route("/test2/<int:random_number>", methods=["GET"])
@token_required
def test2(random_number):
    return jsonify({"test": "successful", "random_number": random_number})