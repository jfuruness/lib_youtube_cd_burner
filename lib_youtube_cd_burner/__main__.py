#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the flask app for the url"""

from .flask_app import app

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
