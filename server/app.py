#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import jsonify, request, session
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import SQLAlchemyError 
import openai
import re


# Local imports
from config import app, db, api
from models import User, StoryInput, ChatGptResponse, DallEResponse
import apikeys

# Set API key
openai.api_key = apikeys.openai_apikey

# Set up brcrypt for password hashing
bcrypt = Bcrypt(app)


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
        # return jsonify(new_story.to_dict()), 201
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



# # Saving an earlier version of this post in case it breaks
# @app.post(URL_PREFIX + "/stories")
# def create_story():
#     # authorize()
#     try:
#         data = request.json
#         print(data)
#         # new_story = StoryInput(**data)
#         new_story = StoryInput(
#             child_name=data['childName'],
#             child_age=data['childAge'],
#             child_race=data['childRace'],
#             child_hairstyle=data['childHairStyle'],
#             child_eyecolor=data['childEyeColor'],
#             child_other_features=data['childOtherFeatures'],
#             child_location=data['childLocation'],
#             child_clothing=data['childClothing'],
#             child_interests=data['childInterests'],
#             story_setting=data['storySetting']
#         )
#         new_story.user_id = current_user().id
#         print(new_story.to_dict)
#         db.session.add(new_story)
#         db.session.commit()
#         return jsonify( new_story.to_dict() ), 201
#     except Exception as e:
#         return jsonify( {'error' : str(e)} ), 406
    
    

@app.post(URL_PREFIX + "/stories")
def create_story():
    # authorize()
    try:
        data = request.json
        print(data)
        # new_story = StoryInput(**data)
        new_story = StoryInput(
            child_name=data['childName'],
            child_age=data['childAge'],
            child_race=data['childRace'],
            child_hairstyle=data['childHairStyle'],
            child_eyecolor=data['childEyeColor'],
            child_other_features=data['childOtherFeatures'],
            child_location=data['childLocation'],
            child_clothing=data['childClothing'],
            child_interests=data['childInterests'],
            story_setting=data['storySetting']
        )
        new_story.user_id = current_user().id

        with app.app_context():
            db.session.add(new_story)
            db.session.commit()

            # Original prompt was not generating the right names
            # prompt = f"Python dictionary: {new_story}. Please write a 10-page children's book about the child named in this dictionary, incorporating some of the parameters in the dictionary. Please make the story relevant to the child's interests and have the child overcome some kind of obstacle."

            prompt = f"Please write a 10-page children's book about a child named {new_story.child_name} who is {new_story.child_age} years old, lives in {new_story.child_location}, and is interested in {new_story.child_interests}. The book's setting should be {new_story.story_setting}. {new_story.child_name} should overcome some kind of obstacle in the story. Please include page numbers in your response"

            chatgpt_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=3500
            )
            generated_text = chatgpt_response.choices[0].text.strip()

            # Parse the returned results into pages
            # Refactor this with loops later - change prompt to have numbering be "01" style
            sentences = re.split(r'(?<=[.!?])\s+', generated_text)

            page01_index = sentences.index("Page 1")
            page02_index = sentences.index("Page 2")
            page03_index = sentences.index("Page 3")
            page04_index = sentences.index("Page 4")
            page05_index = sentences.index("Page 5")
            page06_index = sentences.index("Page 6")
            page07_index = sentences.index("Page 7")
            page08_index = sentences.index("Page 8")
            page09_index = sentences.index("Page 9")
            page10_index = sentences.index("Page 10")

            page01_sentences = sentences[page01_index + 1:page02_index]
            page02_sentences = sentences[page02_index + 1:page03_index]
            page03_sentences = sentences[page03_index + 1:page04_index]
            page04_sentences = sentences[page04_index + 1:page05_index]
            page05_sentences = sentences[page05_index + 1:page06_index]
            page06_sentences = sentences[page06_index + 1:page07_index]
            page07_sentences = sentences[page07_index + 1:page08_index]
            page08_sentences = sentences[page08_index + 1:page09_index]
            page09_sentences = sentences[page08_index + 1:page10_index]
            page10_sentences = sentences[page10_index:]

            page01_text = "".join(page01_sentences)
            page02_text = "".join(page02_sentences)
            page03_text = "".join(page03_sentences)
            page04_text = "".join(page04_sentences)
            page05_text = "".join(page05_sentences)
            page06_text = "".join(page06_sentences)
            page07_text = "".join(page07_sentences)
            page08_text = "".join(page08_sentences)
            page09_text = "".join(page09_sentences)
            page10_text = "".join(page10_sentences)






            returned_story = ChatGptResponse(
                full_response=generated_text,
                storyinput_id=new_story.id,
            )
            db.session.add(returned_story)
            db.session.commit()

        return jsonify(new_story.to_dict()), 201
    except SQLAlchemyError as e:
        # Handle database-related errors
        db.session.rollback()  # Roll back the transaction on error
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': str(e)}), 400








# Route to check responses
@app.route("/checkresponse")
def storycheck():
    storyresponse = ChatGptResponse.query.filter_by(id=2).first()
    if storyresponse:
        return "The story response ID from ChaptGPT is {} and the text is is {}".format(storyresponse.id, storyresponse.full_response)
    else:
        return "No story response found with that id"











    #     print(new_story.to_dict())
    #     db.session.add(new_story)
    #     db.session.commit()

    #     prompt = f"Python dictionary: {new_story}. Please write a 10-page children's book about the child named in this dictionary, incoporating some of the parameters in the dictionary. Please make the story relavent to the child's interests, and have the child overcome some kind of obstacle."

    #     print(prompt)
    #     chatgpt_response = openai.Completion.create(
    #         engine="davinci-003",
    #         prompt=prompt,
    #         max_tokens=8000
    #     )
    #     print(chatgpt_response)
    #     generated_text = chatgpt_response.choices[0].text.strip()
    #     print(generated_text)

    #     returned_story = ChatGptResponse(
    #         full_response = generated_text,
    #         storyinput_id = new_story.id
    #     )
    #     print(returned_story.to_dict())
    #     db.session.add(returned_story)
    #     db.session.commit()
        
    #     return jsonify( new_story.to_dict() ), 201
    # except Exception as e:
    #     return jsonify( {'error' : str(e)} ), 406
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)

    

