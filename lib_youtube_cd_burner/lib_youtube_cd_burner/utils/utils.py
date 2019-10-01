#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains useful functions"""

import re
import sys
import datetime
import os
import functools
import traceback

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


def normalize_audio(obj):
    """Makes audio not spike between switching songs"""

    # Average Volume
    avg_dbfs = sum([x.volume for x in obj.songs])/len(obj.songs)
    for song in obj.songs:
        song.match_target_amplitude(avg_dbfs)
