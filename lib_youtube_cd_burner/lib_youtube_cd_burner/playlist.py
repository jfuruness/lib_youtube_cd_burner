#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains classes Playlist, MyLogger, and Youtube Playlist

The Youtube_Playlist class inherits from playlist, and adds it's own
download function.

MyLogger is a class that is used for the youtube_dl logger

The Playlist class generates CD's and burns them. It does this through
a series of steps.

1. All songs are downloaded.
    -Handled by the class that inherits the Playlist class
    -Starts in the generate_cds function
    -Customizable are cd length, remove silence, and randomizing the cd
2. All songs are formatted
    -Handled in the format_songs function
    -Songs need to be a very spefic format to be burned to a CD
        -Handled in the song class
3. All songs are added to CD's
    -If a CD runs out of room, create another CD
4. All CD's are burned
    -Handled in the burn_cds function
5. All paths are destoryed to clean up

Design Choices:
    -by default remove_silence is false because it takes a while
    -Playlist is it's own class in the hopes for a spotify cd burner
Possible Future Improvements:
    -Spotify playlists?
"""

import os
from random import shuffle
from youtube_dl import YoutubeDL
from shutil import rmtree, copytree, move
from .song import Song
from .cd import CD
from .utils import Youtube_dl_fix, Logger, error_catcher, utils

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__Version__ = "0.1.0"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


class MyLogger(object):
    """Logger class use by youtube_dl"""

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


class Playlist:
    """Playlist class that allows for download and manipulation of songs

    The playlist class can download songs, generate songs from downloads,
    format songs, generate cds, burn cds, and self destruct to remove files.
    """

    @error_catcher()
    def __init__(self,
                 urls,
                 logger=Logger().logger,
                 path="/tmp/lib_cd_burner_songs"):
        """initializes playlist and directories"""

        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.songs = []
        self.cds = []
        # URLs should be in the format of: "url1, url2, url3"
        # This solves the problems of multiple playlists
        # in a single folder not being normalized
        self.urls = urls.replace(" ", "").split(",")
        self.logger = logger

    @error_catcher()
    def generate_cds(self,
                     cd_capacity=60*79+59,
                     remove_silence=False,
                     randomize=False,
                     save_path=None,  # If path is none CD gets burned
                     song_format="wav"):
        """Takes a playlist and generates cds from it.

        Takes a playlist and generates cds from it. remove_silence
        removes silence at the end of songs. randomize is that the songs are
        downloaded in order as they are in the playlist. cd_capacity is the
        amount of seconds that can go on a cd"""

        self.download_songs()
        # Format songs for burn, must do this now to add the three second gap
        self.format_songs(remove_silence, song_format)
        # Randomizes songs if needed
        if randomize:
            shuffle(self.songs)
        if save_path is None:
            room_left = False
            # If the song is added and the cd is too long, it will not add the song
            # And a new cd will be created
            for song in self.songs:
                # If the cd is full, then create a new one
                if not room_left:
                    self.cds.append(CD(cd_capacity, self.logger))
                    room_left = True
                # Add the song to the cd
                room_left = self.cds[-1].add_track(song)
            self.burn_cds()
        else:
            utils.normalize_audio(self)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            self.logger.info("moving songs now")
            for song in self.songs:
                song.add_metadata(save_path)
                move(song.path, os.path.join(save_path,
                                             song.name + "." + song.extension))
        self.clean_up()

    @error_catcher()
    def format_songs(self, remove_silence, song_format):
        """Formats all songs for the cd to be burned

        Formats all songs in cd ro be burned. remove_silence removes the
        silence at the ends of songs.
        remove_silence takes a long time to process, so be default it is false
        """

        for song in self.songs:
            song.format_song(remove_silence, song_format)

    @error_catcher()
    def burn_cds(self, normalize_audio=True):
        """Burns all cds, if normalize_audio, the cds are normalized volume"""

        for cd in self.cds:
            # Normalizing the audio makes it so that the audio doesn't spike
            # if songs are recoreded at different volumes when switching songs
            if normalize_audio:
                utils.normalize_audio(cd)
            cd.burn()

    @error_catcher()
    def clean_up(self):
        """Deletes paths"""

        for song in self.songs:
            if os.path.exists(song.path):
                # rm -rf path
                os.remove(song.path)


class Youtube_Playlist(Playlist):
    """inits a youtube playlist instance"""

    @error_catcher()
    def download_songs(self):
        """Downloads songs and adds to self.songs"""

        # Options for the downloader
        ydl_opts = {
            'ignoreerrors': True,
            'age_limit': 25,
            'retries': 3,
            'format': 'bestaudio[asr=44100]/best',
            'outtmpl': '_%(playlist_index)s- %(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook]
        }
        try:
            og = ydl_opts['outtmpl']
            for i, url in enumerate(self.urls):
                # Download songs
                ydl_opts['outtmpl'] = self.path + "/" + str(i) + og
                with Youtube_dl_fix(ydl_opts) as ydl:
                    ydl.download([url])
        except Exception as e:
            self.logger.warning("Video download failed. Probably webm file")
            self.logger.warning(e)

    @error_catcher()
    def my_hook(self, d):
        """What happens when a song is downloaded"""

        name = d['filename'].rsplit('.', 1)[0]
        if d['status'] == 'finished':
            self.logger.info('Done downloading {}'.format(name))
            song = Song(d['filename'], name, self.logger)
            # Makes sure that the song downloaded and has volume
            if os.path.exists(song.path) and song.volume > -float('Inf'):
                self.songs.append(song)
            # If it didn't download don't include it
            else:
                if os.path.exists(song.path):
                    os.remove(song.path)
                self.logger.info("Not adding song, didn't download properly")
