#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import jsonify, request, session
from flask_bcrypt import Bcrypt
import openai


# Local imports
from config import app, db, api
from models import User, StoryInput, ChatGptResponse, DallEResponse
import apikeys

# Set API key
openai.api_key = apikeys.openai_apikey


bcrypt = Bcrypt(app)

# Can comment out these since importing from config and models
# migrate = Migrate(app, db)

# db.init_app(app)

# CHECK THIS: May not need this
URL_PREFIX = '/api/v1'



# Helps methods to condense code
def current_user():
    return User.query.filter(User.id == session.get('user_id')).first()


def authorize():
    if not current_user():
        return {'Message': "No logged in user. You must log in"}, 401



@app.route('/')
def index():
    return '<h1>The server is working</h1>'


@app.route(URL_PREFIX + '/users')
def get_users():
    authorize()
    return jsonify( [user.to_dict() for user in current_user()] ), 200



@app.route(URL_PREFIX + '/users')
def get_storyinputs():
    authorize()
    return jsonify( [story_input.to_dict() for story_input in current_user().story_input] ), 200



@app.post(URL_PREFIX + '/users')
def create_user():
    try:
        data = request.json
        password_hash = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        new_user = User(
            email=data['email'], 
            password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return new_user.to_dict(), 201
    except Exception as e:
        return { 'error': str(e) }, 406





# # Sign up route
# @app.post('/users')
# def create_user():
#     print("Create users triggered; before try")
#     try:
#         print("After the try")
#         json = request.json
#         print("got the JSON data from front end")
#         pw_hash = bcrypt.generate_password_hash(json['password']).decode('utf-8')
#         print("got to the password encryption")
#         new_user = User(
#             email=json['email'],
#             password = pw_hash,
#             # For now, commenting out other user info
#             # first_name = json['first_name'],
#             # last_name = json['last_name'],
#             # phone_number = json['phone_number'],
#             # street_line1 = json['street_line1'],
#             # street_line2 = json['street_line2'],
#             # zip_code = json['zip_code'],
#             # city = json['city'],
#             # state = json['state']
#             )
#         print("made the new user; not yet added to the database")
#         db.session.add(new_user)
#         db.session.commit()
#         print("New user added to the database")

#         # Add the cookie here
#         session["user_id"] = new_user.id
#         print("cookie was successful")
#         return new_user.to_dict(), 201
#     except Exception as e:
#         print("error triggered as exception")
#         return {'Error': str(e)}, 406


# Login route
@app.post(URL_PREFIX + '/login')
def login():
    json_data = request.json
    user = User.query.filter(User.email == json_data['email']).first()

    if user and bcrypt.check_password_hash( user.password_hash, json_data['password'] ):
        # Set cookie for login that stores teh user_id
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 202
    else:
        return jsonify( {"Message" : "Invalid email address or password"}), 401
    

# Route to check user using session
# @app.get(URL_PREFIX + '/check_session')
# def check_session():
#     user = current_user()

#     if user:
#         return jsonify(user.to_dict()), 200
#     else:
#         return {}, 400
    

#Change this for if Users are not currently logged in
@app.get(URL_PREFIX + '/check_session')
def check_session():
    user = current_user()
    print(current_user)

    if user is not None:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"message": "No authenticated user"}), 401



# Delete method for cookies
@app.delete(URL_PREFIX + "/logout")
def logout():
    session.pop("user_id")
    return {}, 204


# Write routes for creating and viewing the stories.
# need to modify this with the code to send it to OpenAI on post
# and return 

@app.post(URL_PREFIX + "/createstory")
def create_story():
    try:
        data = request.json
        new_story = StoryInput(**data)
        new_story.email = current_user()
        db.session.add(new_story)
        db.session.commit()
        return jsonify( new_story.to_dict() ), 201
    except Exception as e:
        return jsonify( {'error' : str(e)} ), 406
    

# @app.post(URL_PREFIX + "/createstory")
# def create_story():
#     try:
#         data = request.json
#         new_story = StoryInput(**data)
#         new_story.email = current_user()
#         db.session.add(new_story)
#         db.session.commit()

#         # Now try to submit it to OPENAI

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#         )

#         return jsonify( new_story.to_dict() ), 201
#     except Exception as e:
#         return jsonify( {'error' : str(e)} ), 406

    

# def submit_openai():
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "Who won the world series in 2020?"},
#             {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#             {"role": "user", "content": "Where was it played?"}
#         ]
#     )



if __name__ == '__main__':
    app.run(port=5555, debug=True)

    

