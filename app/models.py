from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Delete, update, Update
from flask_login import UserMixin


db = SQLAlchemy()   #this is our connection from pyton to elephant sql database

#create models from out ERD
class User(db.Model, UserMixin):
    # __tablename__ = 'poke_user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), default='default_nickname', nullable=False) #new
    username = db.Column(db.String(20), nullable=False, unique=True) 
    email = db.Column(db.String(150), nullable=False, unique=True) 
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(300))  # new user bio
    post= db.relationship("Post", backref='author', lazy=True) #backref='user'
    
    def __init__(self, nickname, username, email, password, bio):
        self.nickname = nickname
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        
    def saveToDB(self):         #new method that adds the user  ! its a method that works for routes
        db.session.add(self)
        db.session.commit()
        
    def saveChanges(self):
        db.session.add(self)
        db.session.commit()
        
    def deleteFromDB(self):
        db.session.commit()
        

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