#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains a main function for cmd line args.

Design Choices:
-Sudo must be used to make sure user can download properly
Possible Future Improvements:

"""

import os
import subprocess
import sys
from argparse import ArgumentParser
from .utils import Logger
from .playlist import Youtube_Playlist

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__Version__ = "0.1.0"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"


# https://stackoverflow.com/a/20153881
def upgrade_to_sudo(logger):
    """Upgrades to sudo permissions"""

    ret = 0
    if os.geteuid() != 0:
        msg = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
        # https://gist.github.com/davejamesmiller/1965559
        os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)
    if ret != 0:
        logger.warning("User is not a sudo user. Goodbye.")
        sys.exit(1)


def main(urls, logger_args={}, save_path=None, song_format="wav"):
    logger = Logger(logger_args).logger
    parser = ArgumentParser(description='CD Burner')
    parser.add_argument('-urls', action="store", dest="urls", default=None)
    upgrade_to_sudo(logger)
    Youtube_Playlist(urls, logger).generate_cds(save_path=save_path,
                                                song_format=song_format)
