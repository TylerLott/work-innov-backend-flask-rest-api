"""
RESTful api for OCR application

ROUTES:
** requires auth
    /api/users                            POST   request to add a user to the database
    /api/users/<int: id>                  GET    username from id -- probably remove this
**  /api/token                            GET    auth token for user
**  /api/drawing/<int: id>                GET    image from image id
**  /api/projects/                        GET    user projects (determines user from auth token)
**  /api/project/<int: id>                GET    project structure
**  /api/part/<int: id>                   GET    part detail from id
**  /api/part                             POST   places part in db
**  /api/project                          POST   places project in db
**  /api/drawing                          POST   saves drawing file and places path in db



PACKAGES:
    flask
    flask_httpauth
    passlib.apps
    itsdangerous

MODULES:
    User
    DBUser
    OCR

"""

# TODO import mongoDB driver
# TODO import and create User class
# TODO import and create OCR class

import os
from cv2 import imread
from pathlib import Path
from flask import Flask, abort, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as cac
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)
from src.User.User import User
from src.DBUser.DBUser import DBUser
from src.OCR.OCR import OCR


app = Flask(__name__)

auth = HTTPBasicAuth()

# TODO set up the MongoDB


@auth.verify_password
def verify_password(user_or_tok, password):
    user = User.verify_tok(user_or_tok)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=user_or_tok).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/api/users", methods=["POST"])
def new_user():
    pass


@app.route("/api/example_image", methods=["GET"])
def example_image():
    sys_path = os.getcwd()
    info_path = "/data/test_img.png"
    path = Path(sys_path + info_path)
    return send_file(path, mimetype="image/png")


@app.route("/api/image_upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    sys_path = os.getcwd()
    info_path = "/data/test_img.png"
    path = Path(sys_path + info_path)
    file.save(path)

    img = imread(str(path), 0)
    ocr = OCR(img)
    ocr.get_rois()
    data = ocr.extract()
    return jsonify(data)


@app.route("/api/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({"username": user.username})


@app.route("/api/token")
@auth.login_required
def get_tok():
    tok = g.user.generate_tok(1000)
    return jsonify({"token": token.decode("ascii"), "duration": 600})


@app.route("/api/drawing/<int:id>", methods=["GET"])
@auth.login_required
def get_image():
    pass


@app.route("/api/projects", methods=["GET"])
@auth.login_required
def get_projects():
    pass


@app.route("/api/project/<int:id>", methods=["GET"])
@auth.login_required
def get_project(id):
    pass


@app.route("/api/part/<int:id>", methods=["GET"])
@auth.login_required
def get_part(id):
    pass


@app.route("/api/project", methods=["POST"])
@auth.login_required
def create_project():
    pass


@app.route("/api/part", methods=["POST"])
@auth.login_required
def create_part():
    pass


@app.route("/api/drawing", methods=["POST"])
@auth.login_required
def upload_drawing():
    pass
