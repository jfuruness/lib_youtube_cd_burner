#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module creates the flask app to obtain urls"""

from .__init__ import create_app


__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"

create_app().run(debug=True)
