from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class URLForm(FlaskForm):
    """URL Validator form for flask"""
    # Flasks URL validator sucks, so we don't use it
    # It says google.com is an invalid URL. wtf flask_wtf
    url = StringField('URL', validators=[DataRequired()])
    # Saved path
    save_path = StringField("For a CD to burn, this must be empty! save path ex: /home/anon/Desktop/songs")
    submit = SubmitField('Burn CD')
