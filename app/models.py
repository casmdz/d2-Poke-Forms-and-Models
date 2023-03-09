from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Delete, update, Update
from flask_login import UserMixin
from secrets import token_hex
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()   #this is our connection from pyton to elephant sql database

# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable = False),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable = False)
# )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), default='default_nickname', nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True) 
    email = db.Column(db.String(150), nullable=False, unique=True) 
    password = db.Column(db.String, nullable=False)
    apitoken = db.Column(db.String)
    bio = db.Column(db.String(300), default='', nullable=True)  # new user bio
    avatar_url = db.Column(db.String, nullable=True, default='https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp')


    post= db.relationship("Post", backref='author', lazy=True) #backref='user'
    
    def __init__(self, nickname, username, email, password, bio='', avatar_url=None):

        self.nickname = nickname
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)
        self.bio = bio
        self.avatar_url = avatar_url
         
    def saveToDB(self):         #new method that adds the user  ! its a method that works for routes
        db.session.add(self)
        db.session.commit()
        
    def saveChanges(self):
        db.session.commit()
        
    def deleteFromDB(self):
        db.session.commit()
        
        
        
class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    poke_id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String(45), nullable=False, unique=True)
    image = db.Column(db.String)
    base_hp = db.Column(db.Integer, nullable=False)
    base_atk = db.Column(db.Integer, nullable=False)
    base_def = db.Column(db.Integer, nullable=False)
    ability = db.Column(db.String(45), nullable=False)
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
    likes = db.relationship("Likes", lazy=True)
    # object p is calling likes // p.likes ==> [<>]  list 
    
    # how we create the instance
    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def saveChanges(self):
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
        
    def getLikeCounter(self):
        return len(self.likes)  #w6d1 1:30:00
    #dont need to loop through all the posts // feed.html 
        
        
class Likes(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    post_id= db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
    
    def saveToDB(self): 
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.commit()
        
class Following(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    post_id= db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
    
    def saveToDB(self): 
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.commit()