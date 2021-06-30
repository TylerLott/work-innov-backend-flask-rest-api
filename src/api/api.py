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

import os
from pathlib import Path
from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    # g,
    # abort,
)
from flask_httpauth import HTTPBasicAuth

# from passlib.apps import custom_app_context as cac
# from itsdangerous import (
#     TimedJSONWebSignatureSerializer as Serializer,
#     BadSignature,
#     SignatureExpired,
# )
# from src.user.user import User
# from src.db_user.db_user import DBUser
from src.ocr.ocr import OCR


app = Flask(__name__)

auth = HTTPBasicAuth()


# @auth.verify_password
# def verify_password(user_or_tok, password):
#     user = User.verify_tok(user_or_tok)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username=user_or_tok).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True


# @app.route("/api/users", methods=["POST"])
# def new_user():
#     pass


@app.route("/api/example_image", methods=["GET"])
def example_image():
    """Return the test image stored on the server"""
    sys_path = os.getcwd()
    info_path = "/data/test_img.png"
    path = Path(sys_path + info_path)
    return send_file(path, mimetype="image/png")


@app.route("/api/image_upload", methods=["POST"])
def upload_file():
    """
    Handle the uploading of files

    These could be pdfs or images
    """
    file = request.files["file"]
    sys_path = os.getcwd()
    info_path = "/data/test_img.png"
    path = Path(sys_path + info_path)
    file.save(path)

    ocr = OCR(str(path))
    return jsonify(ocr.extract_table())


# @app.route("/api/users/<int:id>", methods=["GET"])
# def get_user(user_id):
#     user = User.query.get(id)
#     if not user:
#         abort(400)
#     return jsonify({"username": user.username})


# @app.route("/api/token")
# @auth.login_required
# def get_tok():
#     token = g.user.generate_tok(1000)
#     return jsonify({"token": token.decode("ascii"), "duration": 600})


# @app.route("/api/drawing/<int:id>", methods=["GET"])
# @auth.login_required
# def get_image():
#     pass


# @app.route("/api/projects", methods=["GET"])
# @auth.login_required
# def get_projects():
#     pass


# @app.route("/api/project/<int:id>", methods=["GET"])
# @auth.login_required
# def get_project(project_id):
#     pass


# @app.route("/api/part/<int:id>", methods=["GET"])
# @auth.login_required
# def get_part(part_id):
#     pass


# @app.route("/api/project", methods=["POST"])
# @auth.login_required
# def create_project():
#     pass


# @app.route("/api/part", methods=["POST"])
# @auth.login_required
# def create_part():
#     pass


# @app.route("/api/drawing", methods=["POST"])
# @auth.login_required
# def upload_drawing():
#     pass