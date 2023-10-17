from config import db
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    # Cut out the other fields for now
    # first_name = db.Column(db.String, nullable=True)
    # last_name = db.Column(db.String, nullable=True)
    # phone_number = db.Column(db.Integer, nullable=True)
    # street_line1 = db.Column(db.String, nullable=True)
    # street_line2 = db.Column(db.String, nullable=True)
    # zip_code = db.Column(db.Integer, nullable=True)
    # city = db.Column(db.String, nullable=True)
    # state = db.Column(db.String, nullable=True)

    # A user can have many StoryInputs
    storyinputs = db.relationship('StoryInput', back_populates='user')

    serialize_rules = ('-storyinputs','-password_hash')

    


class StoryInput (db.Model, SerializerMixin):
    __tablename__ = 'story_inputs'
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String, nullable=False)
    child_age = db.Column(db.String, nullable = False)
    child_race = db.Column(db.String, nullable=False)
    child_hairstyle = db.Column(db.String, nullable=False)
    child_eyecolor = db.Column(db.String, nullable=False)
    child_other_features = db.Column(db.String, nullable=False)
    child_location = db.Column(db.String, nullable=False)
    child_clothing = db.Column(db.String, nullable=False)
    child_interests = db.Column(db.String, nullable=False)
    story_setting = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='storyinputs')
    chatgptresponses = db.relationship('ChatGptResponse', back_populates='storyinput')
    dalleresponses = db.relationship('DallEResponse', back_populates = 'storyinput')

    serialize_rules = ('-user', '-chatgptresponses', '-dalleresponses')




# Eventually after MVP, we will need to go back here and make versions of story
class ChatGptResponse (db.Model, SerializerMixin):
    __tablename__ = "chatgpt_responses"
    id = db.Column(db.Integer, primary_key=True)
    full_response = db.Column(db.String, nullable=False)
    front_cover = db.Column(db.String, nullable=True)
    title_page = db.Column(db.String, nullable=True)
    page01_text = db.Column(db.String, nullable=True)
    page02_text = db.Column(db.String, nullable=True)
    page03_text = db.Column(db.String, nullable=True)
    page04_text = db.Column(db.String, nullable=True)
    page05_text = db.Column(db.String, nullable=True)
    page06_text = db.Column(db.String, nullable=True)
    page07_text = db.Column(db.String, nullable=True)
    page08_text = db.Column(db.String, nullable=True)
    page09_text = db.Column(db.String, nullable=True)
    page10_text = db.Column(db.String, nullable=True)
    back_cover = db.Column(db.String, nullable=True)

    storyinput_id = db.Column(db.Integer, db.ForeignKey('story_inputs.id'), nullable=False)

    storyinput = db.relationship('StoryInput', back_populates='chatgptresponses')

    serialize_rules = ('-storyinput',)




class DallEResponse (db.Model, SerializerMixin):
    __tablename__ = "dalle_responses"
    id = db.Column(db.Integer, primary_key=True)
    front_cover_imageurl = db.Column(db.String, nullable=True)
    page01_imageurl = db.Column(db.String, nullable=True)
    page02_imageurl = db.Column(db.String, nullable=True)
    page03_imageurl = db.Column(db.String, nullable=True)
    page04_imageurl = db.Column(db.String, nullable=True)
    page05_imageurl = db.Column(db.String, nullable=True)
    page06_imageurl = db.Column(db.String, nullable=True)
    page07_imageurl = db.Column(db.String, nullable=True)
    page08_imageurl = db.Column(db.String, nullable=True)
    page09_imageurl = db.Column(db.String, nullable=True)
    page10_imageurl = db.Column(db.String, nullable=True)
    
    storyinput_id = db.Column(db.Integer, db.ForeignKey('story_inputs.id'), nullable=False)

    storyinput = db.relationship('StoryInput', back_populates='dalleresponses')

    serialize_rules = ('-storyinput',)




# class StoryFinal (db.Model, SerializerMixin):
#     opening_page (standard, about company)
#     back_cover (standard, gene

