#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains useful functions"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"


def normalize_audio(obj):
    """Makes audio not spike between switching songs"""

    # Average Volume
    avg_dbfs = sum([x.volume for x in obj.songs])/len(obj.songs)
    print([x.volume for x in obj.songs])
    print(avg_dbfs)
    for song in obj.songs:
        obj.logger.info("Normalizing audio for {}".format(song.name))
        song.match_target_amplitude(avg_dbfs)
        # After normalizing audio, now add silence
        song.add_silence()
