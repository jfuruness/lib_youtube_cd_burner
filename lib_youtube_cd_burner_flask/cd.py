#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains class CD 

CD adds songs then normalizes the audio and burns them
"""

import subprocess
import time
from .logger import error_catcher

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__Version__ = "0.1.0"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

class CD:
    """CD class that adds songs and burns cds"""

    @error_catcher()
    def __init__(self, max_seconds, logger):
        """initializes cd and max seconds a cd can hold"""

        self.logger = logger
        self.max_seconds = max_seconds
        self.total_seconds = 0
        self.songs = []

    @error_catcher()
    def add_track(self, song):
        """Adds a song to a cd, returns false if over limit"""

        # If the song is not over the limit of seconds
        if self.total_seconds + song.seconds <= self.max_seconds:
            # Add the song 
            self.songs.append(song)
            # Increase total seconds
            self.total_seconds += song.seconds
            return True
        else:
            return False

    @error_catcher()
    def normalize_audio(self):
        """Makes audio not spike between switching songs"""

        avg_dbfs = sum([x.get_volume() for x in self.songs])/len(self.songs)
        for song in self.songs:
            song.match_target_amplitude(avg_dbfs)

    def burn(self):
        are_you_sure = "0"
        while are_you_sure != "1":
            times_to_burn = input("How many times would you like to burn this cd? input must be a number")
            try:
                times_to_burn = int(times_to_burn)
                if times_to_burn < 0:
                    continue
            except:
                continue
            are_you_sure = input("You said you want {} copies. If you are sure, enter 1. Else enter 0".format(times_to_burn))
        for i in range(times_to_burn):
            subprocess.run(["eject"])
            input("insert a blank cd and close! Then press enter!") #modify so no enter just insert
            #try except the comand to push cd back in
            # Wait for cd to mount
            seconds_to_wait = 10
            for i in range(seconds_to_wait):
                print("burning cd in {}".format(seconds_to_wait - i))
                time.sleep(i)
            args = [
                    "sudo",
                    "wodim",
                    "-v",
                    "dev=/dev/sr0",
                    "-dao", #sao????? same in wodim????
                    "-audio",
                    "-pad",
                    "speed=8" # for my cd player 10 is lowest, allow user to set speed option
                   ]
            args.extend([x.path for x in self.songs])
            output = subprocess.run(args)
            print("Just burned:")
            print(self)
            subprocess.run(["eject"])



    def __str__(self):
        lines = [
                 '\n',
                 "cd!!!!!!!!!!!!!!!!!!!!!!!",
                 "{} minutes".format(self.total_seconds/60),
                 "songs:"
                ]
        [lines.append(x.__str__()) for x in self.songs]
        lines.append("\n")
        return "\n".join(lines)
