#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module creates the flask app to obtain urls"""

import os
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from .lib_youtube_cd_burner import main


__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"


class URLForm(FlaskForm):
    """URL Validator form for flask"""
    # Flasks URL validator sucks, so we don't use it
    # It says google.com is an invalid URL. wtf flask_wtf
    url = StringField('URL(s) (Comma separated if more than one)',
                      validators=[DataRequired()])
    # Saved path
    save_path_str = ("For a CD to burn, this must be empty! "
                     "save path ex: /home/anon/Desktop/songs")
    save_path = StringField(save_path_str)
    song_format = StringField("Desired Song Format. For CDs, must be wav",
                              default="wav")
    submit = SubmitField('Burn/Save')


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="db5791628bb0b13ce0c676dfde280ba245",
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=['GET', 'POST'])
    @app.route("/home", methods=['GET', 'POST'])
    def home():
        form = URLForm()
        if form.validate_on_submit():
            flash("Completed", "success")
            # Method call here to burn CDs!
            path = None if form.save_path.data == "" else form.save_path.data
            main(form.url.data,
                 save_path=path,
                 song_format=form.song_format.data.lower())
        return render_template('home.html', form=form)

    return app
