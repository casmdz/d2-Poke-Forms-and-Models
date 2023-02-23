from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from sqlalchemy import Delete

class UserCreationForm(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired()])
    username = StringField("Username", validators= [DataRequired()])
    email = StringField("Email", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()
    
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators= [DataRequired()])
    password = PasswordField("Password", validators= [DataRequired()])
    submit = SubmitField()
    

class ProfileUpdateForm(FlaskForm):
    nickname = StringField("Nickname")
    bio = TextAreaField("Bio", validators = [Length(max=300)] )  
    submit = SubmitField()
#validators=[Length(max=300)]
        #https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf 

class PokemonSearchForm(FlaskForm):
    pokemon = StringField('Pokemon', validators=[DataRequired()])
    submit = SubmitField('Search')
    

class PostForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    img_url = StringField("Image URL", validators = [DataRequired()])
    caption = StringField("Caption", validators = [DataRequired()])
    
    submit = SubmitField()
