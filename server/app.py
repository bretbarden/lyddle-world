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

            prompt = f"Please write a 10-page children's book about a child named {new_story.child_name} who is {new_story.child_age} years old, lives in {new_story.child_location}, and is interested in {new_story.child_interests}. The book's setting should be {new_story.story_setting}. {new_story.child_name} should overcome some kind of obstacle in the story. Please include page numbers in your response. After the story, please include Dall-E prompts for each of the pages, with each description beginning with 'Image 1' for instance, corresponding to a page. In each Dall-E prompt, include 1) a description of {new_story.child_name}: a child aged {new_story.child_age}, wearing {new_story.child_clothing}, are {new_story.child_race}, with {new_story.child_hairstyle} hair, 2) explicitly state that {new_story.child_name} should take up only a small amount of the image, around one-eight of the image size, 3) explicitly state that the style should be a digital art illustration, 4) all people should be faceless, and 5) be as consistent across the page illustrations as possible. An example of the type of Dall-E image prompts to inspire you is 'Digital art illustration of a Florida beach scene with bright sunshine and sparkling sea. On one side, occupying about an eighth of the image, is Jenna, a 13-year-old girl with a determined demeanor. In the background, there's a sailboat with white sails billowing against the blue horizon. The sand is golden, and there are seashells scattered around. The essence of the image should capture Jenna's love for sailing and her ambition to be the best sailor.'"

            chatgpt_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=3000
            )
            generated_text = chatgpt_response.choices[0].text.strip()
            print(f'This is a print of generated_text: {generated_text}')

            # Parse the returned results into pages
            # Refactor this with loops later - change prompt to have numbering be "01" style
            # Commenting out the regular expressions to see if it will work without them since they appear to be messing with the way that pages are parsed
            # sentences = re.split(r'(?<=[.!?])\s+', generated_text)


            page01_index = generated_text.index("Page 1")
            print(f'This is a print of page01_index: {page01_index}')
            page02_index = generated_text.index("Page 2")
            page03_index = generated_text.index("Page 3")
            page04_index = generated_text.index("Page 4")
            page05_index = generated_text.index("Page 5")
            page06_index = generated_text.index("Page 6")
            page07_index = generated_text.index("Page 7")
            page08_index = generated_text.index("Page 8")
            page09_index = generated_text.index("Page 9")
            # page10_index = generated_text.index("Page 10") if "Page 10" in generated_text else len(generated_text)
            page10_index = generated_text.index("Page 10")
            print(f'This is a print of page10_index: {page10_index}')


            page01_text = generated_text[page01_index + 8:page02_index]
            print(f'This is a print of page01_text: {page01_text}')
            page02_text = generated_text[page02_index + 8:page03_index]
            page03_text = generated_text[page03_index + 8:page04_index]
            page04_text = generated_text[page04_index + 8:page05_index]
            page05_text = generated_text[page05_index + 8:page06_index]
            page06_text = generated_text[page06_index + 8:page07_index]
            page07_text = generated_text[page07_index + 8:page08_index]
            page08_text = generated_text[page08_index + 8:page09_index]
            page09_text = generated_text[page09_index + 8:page10_index]
            page10_text = generated_text[page10_index + 9:]
            print(f'This is a print of page10_text: {page10_text}')


            returned_story = ChatGptResponse(
                full_response=generated_text,
                storyinput_id=new_story.id,
                page01_text=page01_text,
                page02_text=page02_text,
                page03_text=page03_text,
                page04_text=page04_text,
                page05_text=page05_text,
                page06_text=page06_text,
                page07_text=page07_text,
                page08_text=page08_text,
                page09_text=page09_text,
                page10_text=page10_text
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





@app.route("/storyinputs/<int:id>")
def get_story_by_id(id):
    story_input = StoryInput.query.filter_by(id=id).first()
    if story_input:
        return story_input.to_dict()
    else:
        return "No Story Input response found with that id"



# Route to check Chat GPT responses
@app.route("/chatgptresponses/<int:id>")
def chatgpt_responses_by_id(id):
    chatgpt_response = ChatGptResponse.query.filter_by(id=id).first()
    if chatgpt_response:
        return chatgpt_response.to_dict()
    else:
        return "No ChatGPT story response found with that id"

















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

    

