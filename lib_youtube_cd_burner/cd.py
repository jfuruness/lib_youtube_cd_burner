#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains class CD

The CD class can add songs, normalize the audio, and burn itself.

When adding songs, the cd burner makes sure it doesn't go over
it's capacity. If it does it returns false.

Normalizing the audio is used to make sure one song isn't louder
than the rest on the track.

Design Choices:
-Normalized audio is used to ensure songs are similar volume
-Burn speed set as low as possible to make sure for a smooth burn for
 use in things such as car players etc
Possible Future Improvements:
-Allow user to set burn speed
"""

import subprocess
import time
import fcntl
import os
from .utils import error_catcher

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
        # Song too long return false, cd full
        else:
            return False

    @error_catcher()
    def normalize_audio(self):
        """Makes audio not spike between switching songs"""

        # Average Volume
        avg_dbfs = sum([x.volume for x in self.songs])/len(self.songs)
        for song in self.songs:
            song.match_target_amplitude(avg_dbfs)

    def burn(self, times_to_burn=1):
        """Burns a cd times_to_burn times"""

        for i in range(times_to_burn):
            # Wait for disk insertion
            self._get_disk()
            # Wait for CD to mount
            self._wait_for_cd_to_mount()
            # args for bash command
            args = ["sudo",
                    "wodim",
                    "-v",
                    "dev=/dev/sr0",
                    "-dao",  # sao????? same in wodim????
                    "-audio",
                    "-pad",
                    "speed=8"  # for my cd player 10 is lowest
                    ]
            # Adds all the songs to burn in order
            args.extend([x.path for x in self.songs])
            # Actually burns the cd
            output = subprocess.run(args)
            self.logger.debug(output)
            self.logger.info("Just burned {}".format(self))
            # Pops the new cd out
            subprocess.run(["eject"])

    def _wait_for_cd_to_mount(self, seconds_to_wait=10):
        """Waits seconds to wait to mount cd."""

        for i in range(seconds_to_wait):
            self.logger.debug("burning cd in {}".format(seconds_to_wait - i))
            time.sleep(i)

    def _get_disk(self):
        """Waits for disk insertion"""

        # Pops out cd
        subprocess.run(["eject"])
        self.logger.info("Insert cd!")
        # 1 for no disk, 2 for open, 3 for reading, 4 for disk in tray
        rv = 2
        # While cd drive is open
        while rv == 2:
            # https://superuser.com/a/1367091
            # Gets CD
            fd = os.open('/dev/sr0', os.O_RDONLY | os.O_NONBLOCK)
            rv = fcntl.ioctl(fd, 0x5326)
            os.close(fd)
            time.sleep(1)

    def __str__(self):
        """For when cd's are printed"""

        lines = ["cd is {} minutes".format(self.total_seconds/60),
                 "songs:"]
        [lines.append("    " + x.__str__()) for x in self.songs]
        lines.append("\n")
        return "\n".join(lines)
