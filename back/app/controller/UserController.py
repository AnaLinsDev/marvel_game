from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import Response, request
from models.User import *
from app import app
import json

auth = HTTPBasicAuth()
authToken = HTTPTokenAuth(scheme='Bearer')
users = {}

# Auth Methods

@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if check_password_hash(user.password, password):
        return email

@app.route("/login")
@auth.login_required
def login():
    return "Hello, %s!" % auth.current_user()

@authToken.verify_token
def verify_token(token):
    user = User.query.filter_by(token=token).first()
    if user != None:
        return user

# User Methods

@app.route("/users", methods=["GET"])
@authToken.login_required
def get_all_users():
    user_list = User.query.all()
    users_json = [user.to_json() for user in user_list]
    return generate_response(200, "users", users_json)


@app.route("/user/<id>", methods=["GET"])
@authToken.login_required
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    user_json = user.to_json()
    return generate_response(200, "user", user_json)


@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()
    try:
        password = generate_password_hash(body["password"])
        user = User(name=body["name"], email= body["email"], password= password)
        user.generate_key()
        db.session.add(user)
        db.session.commit()
        return generate_response(201, "user", user.to_json(), "Created !!")

    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "user", {}, "Error on create !!")


@app.route("/user/<id>", methods=["PUT"])
@authToken.login_required
def update_user(id):
    user = User.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('name' in body):
            user.name = body['name']
        if('email' in body):
            user.email = body['email']
        if('password' in body):
            user.password = body['password']
        
        db.session.add(user)
        db.session.commit()
        return generate_response(200, "user", user.to_json(), "Updated !!")

    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "user", {}, "Error on update !!")


@app.route("/user/<id>", methods=["DELETE"])
@authToken.login_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    try:
        db.session.delete(user)
        db.session.commit()
        return generate_response(200, "user", user.to_json(), "Deleted !!")

    except Exception as e:
        print('Error: ', e)
        return generate_response(400, "user", {}, "Error on delete !!")



def generate_response(status, type, conteudo, mensagem=False):
    body = {}
    body[type] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    # dumps irá mudar obj para string
    # mimetype está definindo o tipo de retorno
    return Response(json.dumps(body), status=status, mimetype="application/json")
