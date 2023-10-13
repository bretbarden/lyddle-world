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
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    street_line1 = db.Column(db.String, nullable=True)
    street_line2 = db.Column(db.String, nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)

    # A user can have many StoryInputs
    storyinputs = db.relationship('StoryInput', back_populates='user')

    






class StoryInput (db.Model, SerializerMixin):
    id = db.Column(db.Integer, nullable=False)
    child_name = db.Column(db.String, nullable=False)
    child_age = db.Column(db.Integr, nullable = False )
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




# Eventually after MVP, we will need to go back here and make versions of story
class ChatGptResponse (db.Model, SerializerMixin):
    id = db.Column(db.Integer, nullable=False)
    full_response = db.Column(db.String, nullable=False)
    front_cover = db.Column(db.String, nullable=False)
    title_page = db.Column(db.String, nullable=False)
    page01 = db.Column(db.String, nullable=True)
    page02 = db.Column(db.String, nullable=True)
    page03 = db.Column(db.String, nullable=True)
    page04 = db.Column(db.String, nullable=True)
    page05 = db.Column(db.String, nullable=True)
    page06 = db.Column(db.String, nullable=True)
    page07 = db.Column(db.String, nullable=True)
    page08 = db.Column(db.String, nullable=True)
    page09 = db.Column(db.String, nullable=True)
    page10 = db.Column(db.String, nullable=True)
    back_cover = db.Column(db.String, nullable=True)

    storyinput_id = db.Column(db.Integer, db.ForeignKey('storyinputs.id'), nullable=False)

    storyinput = db.relationship('StoryInput', back_populates='chatgptresponses')




class DallEResponse (db.Model, SerializerMixin):
    id = db.Column(db.Integer, nullable=False)
    front_cover_image_url = db.Column(db.String, nullable=False)
    page01_image_url = db.Column(db.String, nullable=False)
    page02_image_url = db.Column(db.String, nullable=False)
    page03_image_url = db.Column(db.String, nullable=False)
    page04_image_url = db.Column(db.String, nullable=False)
    page05_image_url = db.Column(db.String, nullable=False)
    page06_image_url = db.Column(db.String, nullable=False)
    page07_image_url = db.Column(db.String, nullable=False)
    page08_image_url = db.Column(db.String, nullable=False)
    page09_image_url = db.Column(db.String, nullable=False)
    page10_image_url = db.Column(db.String, nullable=False)
    
    storyinput_id = db.Column(db.Integer, db.ForeignKey('storyinputs.id'), nullable=False)

    storyinput = db.relationship('StoryInput', back_populates='dalleresponses')




# class StoryFinal (db.Model, SerializerMixin):
#     opening_page (standard, about company)
#     back_cover (standard, gene

