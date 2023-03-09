#search forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, URL
from sqlalchemy import Delete


class PokemonSearchForm(FlaskForm):
    pokemon_name = StringField('Pokemon', validators=[DataRequired()])
    submit = SubmitField('Search')