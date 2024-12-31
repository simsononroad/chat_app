import flask
from flask_wtf import FlaskForm
from wtforms import StringField

class belepes(FlaskForm):
    name = StringField(
        name='username',
        render_kw={'placeholder': 'Felhasználónév'}
    )