#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import jsonify, request, session
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import openai
from openai import OpenAI



# Local imports
from config import app, db, api
from models import User, StoryInput, ChatGptResponse, DallEResponse
# import apikeys

# Set API key
# openai.api_key = apikeys.openai_apikey

# Use the new client notation that OpenAI implemented
client = OpenAI()

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
    


@app.post(URL_PREFIX + "/createstory")
def create_story():
    # authorize()
    try:
        data = request.json
        print(data)
        # new_story = StoryInput(**data)
        new_story = StoryInput(
            child_name=data['childName'],
            child_age=data['childAge'],
            child_pronouns=data['childPronouns'],
            child_race=data['childRace'],
            child_hairstyle=data['childHairStyle'],
            # child_eyecolor=data['childEyeColor'],
            # child_other_features=data['childOtherFeatures'],
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

            prompt = f"Do not use any quotation marks of any kind in your response. Please write a 6-page (exactly 6 pages - no more or less) children's book about a child named {new_story.child_name} who is {new_story.child_age} years old, uses {new_story.child_pronouns} pronouns, is from {new_story.child_location}, and is interested in {new_story.child_interests}. The book's setting should be {new_story.story_setting}. {new_story.child_name} should overcome some kind of obstacle in the story. Include a title for the story at the beginning of your response after the phrase 'TITLE:'. Please include page numbers like 'Page 01' for instance, at the beginning of each page, followed by the text of the story page. After the text of each story page, please include Dall-E prompts for each page, with each description beginning explicitly with 'Dalle-E 01' for instance so that I can parse it later, where the '01' corresponds to the page number. Each Dall-E prompt MUST incorporate the following five points of guidance: (1) MUST INCLUDE a description of {new_story.child_name}: a child aged {new_story.child_age}, using {new_story.child_pronouns} pronouns, wearing {new_story.child_clothing}, are {new_story.child_race}, with {new_story.child_hairstyle} hair, (2)  MUST EXPLICTLY DESCRIBE the background (3) MUST EXPLICITLY STATE that any people depicted being around only one-eight the size of the total Dall-E image (4) MUST EXPLICITLY STATE that all people in the image should be faceless, (5) MUST EXPLICITLY STATE that the style should be a digital art illustration, and (6) be as consistent across the page illustrations as possible. An example of the type of Dall-E image prompts to inspire you is 'Digital art illustration of a Florida beach scene with bright sunshine and sparkling sea. On one side, occupying about an eighth of the image, is Lydia, a 13-year-old Asian girl with straight black hair down to her shoulders wearing a green dress. In the background, there's a sailboat with white sails billowing against the blue horizon. The sand is golden, and there are seashells scattered around. The essence of the image should capture Jenna's love for sailing and her ambition to be the best sailor.'"

            # chatgpt_response = client.Completion.create(
            #     engine="gpt-3.5-turbo-instruct",
            #     prompt=prompt,
            #     max_tokens=3500
            # )

            chatgpt_response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What’s in this image?"},
                            {
                                "type": "image_url",
                                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            generated_text = chatgpt_response.choices[0].text.strip()
            print(f'This is a print of generated_text: {generated_text}')

            # Parse the returned results into pages
            # Refactor this with loops later - change prompt to have numbering be "01" style
            # Commenting out the regular expressions to see if it will work without them since they appear to be messing with the way that pages are parsed
            # sentences = re.split(r'(?<=[.!?])\s+', generated_text)

            

            title_index = generated_text.index("TITLE:")

            page01_index = generated_text.index("Page 01")
            page02_index = generated_text.index("Page 02")
            page03_index = generated_text.index("Page 03")
            page04_index = generated_text.index("Page 04")
            page05_index = generated_text.index("Page 05")
            page06_index = generated_text.index("Page 06")

            dalle01_index = generated_text.index("Dall-E 01")
            dalle02_index = generated_text.index("Dall-E 02")
            dalle03_index = generated_text.index("Dall-E 03")
            dalle04_index = generated_text.index("Dall-E 04")
            dalle05_index = generated_text.index("Dall-E 05")
            dalle06_index = generated_text.index("Dall-E 06")

        
            print(f'This is a print of title_index: {title_index}')
            print(f'This is a print of page01_index: {page01_index}')
            print(f'This is a print of page06_index: {page06_index}')
            print(f'This is a print of dalle01_index: {dalle01_index}')
            print(f'This is a print of dalle06_index: {dalle06_index}')

            title_text = generated_text[title_index + 7:page01_index]

            page01_text = generated_text[page01_index + 8:dalle01_index]
            page02_text = generated_text[page02_index + 8:dalle02_index]
            page03_text = generated_text[page03_index + 8:dalle03_index]
            page04_text = generated_text[page04_index + 8:dalle04_index]
            page05_text = generated_text[page05_index + 8:dalle05_index]
            page06_text = generated_text[page06_index + 8:dalle06_index]


            page01_dalleprompt = generated_text[dalle01_index + 11:page02_index]
            page02_dalleprompt = generated_text[dalle02_index + 11:page03_index]
            page03_dalleprompt = generated_text[dalle03_index + 11:page04_index]
            page04_dalleprompt = generated_text[dalle04_index + 11:page05_index]
            page05_dalleprompt = generated_text[dalle05_index + 11:page06_index]
            page06_dalleprompt = generated_text[dalle06_index + 11:]

            print(f'This is a print of title_text: {title_text}')
            print(f'This is a print of page01_text: {page01_text}')
            print(f'This is a print of page06_text: {page06_text}')
            print(f'This is a print of page01_dalleprompt: {page01_dalleprompt}')
            print(f'This is a print of page06_dalleprompt: {page06_dalleprompt}')


            returned_story = ChatGptResponse(
                full_response=generated_text,
                storyinput_id=new_story.id,
                title_text=title_text,
                page01_text=page01_text,
                page02_text=page02_text,
                page03_text=page03_text,
                page04_text=page04_text,
                page05_text=page05_text,
                page06_text=page06_text,
                page01_dalleprompt=page01_dalleprompt,
                page02_dalleprompt=page02_dalleprompt,
                page03_dalleprompt=page03_dalleprompt,
                page04_dalleprompt=page04_dalleprompt,
                page05_dalleprompt=page05_dalleprompt,
                page06_dalleprompt=page06_dalleprompt
            )
            # Commenting this out to add the story before the illustrations
            # db.session.add(returned_story)
            # db.session.commit()

            db.session.add(returned_story)
            db.session.commit()

            # dalle_mainprompt = "All people should be faceless. Any people should be around one-eigth the size of the image."
            dalle_mainprompt = "Image in the style of Leonid Afremov. Any people should be around one-eigth the size of the image."
            
            # Things to try:
            # Claude Monet
            # Leonid Afremov
            # Caspar David Friedrich, Wanderer above the Sea of Fog
            # Georges Seurat, A Sunday Afternoon on the Island of La Grande Jatte
            # Gideon Rubin famous faceless painter but colors too bland

            # 2023.11.21 Model upgraded for Dall-E 3 and using OpenAI syntax
            response_dalle01 = client.images.generate(
                model="dall-e-3",
                prompt=f'{dalle_mainprompt}{page01_dalleprompt}',
                n=1,
                size="1024x1024",
                quality="standard"
                )
            page01_imageurl = response_dalle01['data'][0]['url']
            print(f'Page 01 dalle-E illustration successfully generated: {page01_imageurl}')

            response_dalle02 = client.images.generate(
                model="dall-e-3",
                prompt=f'{dalle_mainprompt}{page02_dalleprompt}',
                n=1,
                size="1024x1024",
                quality="standard"
                )
            page02_imageurl = response_dalle02['data'][0]['url']
            print(f'Page 02 dalle-E illustration successfully generated: {page02_imageurl}')

            response_dalle03 = client.images.generate(
                model="dall-e-3",
                prompt=f'{dalle_mainprompt}{page03_dalleprompt}',
                n=1,
                size="1024x1024",
                quality="standard"
                )
            page03_imageurl = response_dalle03['data'][0]['url']
            print(f'Page 03 dalle-E illustration successfully generated: {page03_imageurl}')


            response_dalle04 = client.images.generate(
                model="dall-e-3",
                prompt=f'{dalle_mainprompt}{page04_dalleprompt}',
                n=1,
                size="1024x1024",
                quality="standard"
                )
            page04_imageurl = response_dalle04['data'][0]['url']
            print(f'Page 04 dalle-E illustration successfully generated: {page04_imageurl}')

            response_dalle05 = client.images.generate(
                model="dall-e-3",
                prompt=f'{dalle_mainprompt}{page05_dalleprompt}',
                n=1,
                size="1024x1024",
                quality="standard",
                )
            page05_imageurl = response_dalle05['data'][0]['url']
            print(f'Page 05 dalle-E illustration successfully generated: {page05_imageurl}')

            response_dalle06 = client.images.generate(
                model="dall-e-3",
                prompt=f'{dalle_mainprompt}{page06_dalleprompt}',
                n=1,
                size="1024x1024",
                quality="standard"
                )
            page06_imageurl = response_dalle06['data'][0]['url']
            print(f'Page 06 dalle-E illustration successfully generated: {page06_imageurl}')


            returned_illustrations= DallEResponse(
                storyinput_id=new_story.id,
                page01_imageurl=page01_imageurl,
                page02_imageurl=page02_imageurl,
                page03_imageurl=page03_imageurl,
                page04_imageurl=page04_imageurl,
                page05_imageurl=page05_imageurl,
                page06_imageurl=page06_imageurl,
            )


            db.session.add(returned_illustrations)
            db.session.commit()


        return jsonify(new_story.to_dict()), 201
    except SQLAlchemyError as e:
        # Handle database-related errors
        db.session.rollback()  # Roll back the transaction on error
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': str(e)}), 400



# Route for developer to check story inputs 
@app.route(URL_PREFIX + "/storyinputs/<int:id>")
def get_story_by_id(id):
    story_input = StoryInput.query.filter_by(id=id).first()
    if story_input:
        return story_input.to_dict()
    else:
        return "No Story Input response found with that id"



# Route for developer to check Chat GPT responses
@app.route(URL_PREFIX + "/chatgptresponses/<int:id>")
def chatgpt_responses_by_id(id):
    chatgpt_response = ChatGptResponse.query.filter_by(id=id).first()
    if chatgpt_response:
        return chatgpt_response.to_dict()
    else:
        return "No ChatGPT story response found with that id"


# Route for developer to check Dall-E responses
@app.route(URL_PREFIX + "/dalleresponses/<int:id>")
def dalle_responses_by_id(id):
    dalle_response = DallEResponse.query.filter_by(id=id).first()
    if dalle_response:
        return dalle_response.to_dict()
    else:
        return "No Dall-E story response found with that id"
    

# Route to display all stories for the user, just among the successful stories.
# @app.route(URL_PREFIX + "/stories/")
# def get_stories():
#     user = current_user()
#     stories = ChatGptResponse.query.filter_by(user__id=user)





# @app.route(URL_PREFIX + '/getlaststory')
# def get_laststory():
#     session = Session()

#     laststoryid = session.query(StoryInput).order_by(StoryInput.id.desc()).first()

#     laststoryid = StoryInput.query.order_by(StoryInput.id.desc()).first()
    
#     print(f'This is the last story ID: {laststoryid}')
#     chatgpt_response = ChatGptResponse.query.filter_by(storyinput_id=laststoryid).first()
#     dalle_response = DallEResponse.query.filter_by(storyinput_id=laststoryid).first()

#     if not chatgpt_response or not dalle_response:
#         return jsonify({"error": "Data not found"}), 404

#     chatgpt_data = chatgpt_response.to_dict()
#     dalle_data = dalle_response.to_dict()

#     combined_data = {
#         "title_text": chatgpt_data.get("title_text"),
#         "pages": [
#             {"text": chatgpt_data.get(f"page{i+1}_text"), "imageurl": dalle_data.get(f"page{i+1}_imageurl")}
#             for i in range(6)
#         ]
#     }

#     return jsonify(combined_data)




@app.route(URL_PREFIX + '/getlaststory')
def get_laststory():
    laststoryid = StoryInput.query.order_by(StoryInput.id.desc()).first()
    
    if not laststoryid:
        return jsonify({"error": "No story found"}), 404

    chatgpt_response = ChatGptResponse.query.filter_by(storyinput_id=laststoryid.id).first()
    dalle_response = DallEResponse.query.filter_by(storyinput_id=laststoryid.id).first()

    if not chatgpt_response or not dalle_response:
        return jsonify({"error": "Data not found"}), 404

    chatgpt_data = chatgpt_response.to_dict()
    dalle_data = dalle_response.to_dict()

    combined_data = {
        "title_text": chatgpt_data.get("title_text"),
        "pages": [
            {"text": chatgpt_data.get(f"page0{i+1}_text"), "imageurl": dalle_data.get(f"page0{i+1}_imageurl")}
            for i in range(6)
        ]
    }

    return jsonify(combined_data)



if __name__ == '__main__':
    app.run(port=5555, debug=True)

    

