#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, jsonify, request, session
from flask_restful import Resource
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Local imports
from config import app, db, api
from models import User, StoryInput, ChatGptResponse, DallEResponse


bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)

# CHECK THIS: May not need this
URL_PREFIX = '/api/v1'



# Helps methods to condense code
def current_user():
    return User.query.filter(User.id == session.get('user_id')).first

# Could add an admin here if wanted


@app.route('/')
def index():
    return '<h1>Project Server Test</h1>'



# Sign up route
@app.post('/users')
def create_user():
    try:
        json = request.json
        pw_hash = bcrypt.generate_password_hash(json['password']).decode('utf-8')
        new_user = User(
            email=json['email'],
            password = pw_hash,
            first_name = json['first_name'],
            last_name = json['last_name'],
            phone_number = json['phone_number'],
            street_line1 = json['street_line1'],
            street_line2 = json['street_line2'],
            zip_code = json['zip_code'],
            city = json['city'],
            state = json['state '])
        db.session.add(new_user)
        db.session.commit()

        # Add the cookie here
        session["user_id"] = new_user.id
        return new_user.to_dict(), 201
    except Exception as e:
        return {'Error': str(e)}, 406


# Login route
@app.post(URL_PREFIX + 'login')
def login():
    json_data = request.json
    user = User.query.filter(User.email_address == json_data['email_address']).first()

    if user and bcrypt.check_password_hash( user.password_hash, json_data['password'] ):
        # Set cookie for login that stores teh user_id
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 202
    else:
        return jsonify( {"Message" : "Invalid email address or password"}), 401
    

# Route to check user using session
@app.get(URL_PREFIX + '/check_session')
def check_session():
    user = current_user()

    if user:
        return jsonify( user.to_dict() ), 200
    else:
        return {}, 400
    

# Delete method for cookies
@app.delete(URL_PREFIX + "/logout")
def logout():
    session.pop("user_id")
    return {}, 204


# Write routes for creating and viewing the stories.
@app.post(URL_PREFIX + "/creatstory")
def create_story():
    try:
        data = request.json
        new_story = StoryInput(**data)
        new_story.email = current_user()
        db.session.add(new_story)
        db.session.commmit()
        return jsonify( new_story.to_dict() ), 201
    except Exception as e:
        return jsonify( {'error' : str(e)} ), 406
    








if __name__ == '__main__':
    app.run(port=5555, debug=True)

