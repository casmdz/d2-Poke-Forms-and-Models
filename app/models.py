from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Delete, update, Update
from flask_login import UserMixin


db = SQLAlchemy()   #this is our connection from pyton to elephant sql database

#create models from out ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), default='default_nickname', nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True) 
    email = db.Column(db.String(150), nullable=False, unique=True) 
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(300), default='', nullable=True)  # new user bio
    avatar_url = db.Column(db.String, nullable=True, default='https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp')


    post= db.relationship("Post", backref='author', lazy=True) #backref='user'
    
    def __init__(self, nickname, username, email, password, bio='', avatar_url=None):

        self.nickname = nickname
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.avatar_url = avatar_url
         
    def saveToDB(self):         #new method that adds the user  ! its a method that works for routes
        db.session.add(self)
        db.session.commit()
        
    def saveChanges(self):
        db.session.commit()
        
    def deleteFromDB(self):
        db.session.commit()
        
        
        
# class Pokemon(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(45), nullable=False, unique=True)
#     ability = db.Column(db.String(45), nullable=False)
#     base_xp = db.Column(db.Integer, nullable=False)
#     base_atk = db.Column(db.Integer, nullable=False)
#     base_hp = db.Column(db.Integer, nullable=False)
#     base_def = db.Column(db.Integer, nullable=False)
#     front_shiny = db.Column(db.String(145), nullable=False)
    # team = db.relationship('Team', backref='pokemon', lazy=True)

       

# class Team(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     poke_name= db.Column(db.String, db.ForeignKey('pokemon.name'), nullable=False, unique = True)
    
#     def __init__(self, user_id, poke_name):
#         self.user_id = user_id
#         self.poke_name = poke_name
    
#     def saveToDB(self):
#         db.session.add(self)
#         db.session.commit()

#     def deleteFromDB(self):
#         db.session.delete(self)
#         db.session.commit()


class Post(db.Model):  
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    img_url = db.Column(db.String, nullable=False) 
    caption = db.Column(db.String(1000))
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # how we create the instance
    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id
        
class Likes(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, primary_key=True)
    post_id= db.Column(db.Integer, primary_key=True)
    
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
    
    def saveToDB(self):         #new method that adds the user  ! its a method that works for routes
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.commit()