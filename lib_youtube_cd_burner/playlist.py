import logging
import os
from lib_utils.file_funcs import makedirs
from random import shuffle
from shutil import move

from .cd import CD, CDFullError
from .song_holder import SongHolder

class Playlist(SongHolder):
    """Playlist class that allows for download and manipulation of songs

    The playlist class can download songs, generate songs from downloads,
    format songs, generate cds, burn cds, and self destruct to remove files.
    """

    def __init__(self, urls: list, dl_path: str):
        """initializes playlist and directories"""

        self.dl_path = dl_path
        self.urls = urls
        super(Playlist, self).__init__()

    def generate_audio_medium(self,
                              cd_capacity=60*79+59,
                              remove_silence=False,
                              randomize=False,
                              save_path=None,  # If path is none CD gets burned
                              song_format="wav",
                              normalize_audio=True,
                              add_silence=True):
        """Takes a playlist and generates cds from it.

        remove_silence removes silence at the end of songs. randomize is
        that the songs are downloaded in order as they are in the
        playlist. cd_capacity is the amount of seconds that can go on a cd.
        """

        self.download_songs()
        # Removes silence, randomizes, changes song format
        self.format_1(remove_silence, randomize, song_format)

        if save_path is None:
            self.save_as_cds(cd_capacity, normalize_audio, add_silence)
        else:
            self.save_as_files(normalize_audio, add_silence, save_path)

        self.clean_up()

    def save_as_cds(self, cd_capacity, normalize_audio, add_silence):
        """Burns all cds, if normalize_audio, the cds are normalized volume"""

        self.generate_cds(cd_capacity)
        self.format_2(normalize_audio, add_silence)
        for cd in self.cds:
            cd.burn()

    def generate_cds(self, cd_capacity):
        """Generate CDs"""

        # If a song is too long for cd it's moved to the next CD
        for song in self.songs:
            try:
                self.cds[-1].add_track(song)
            except (CDFullError, IndexError):
                # If the cd is full or there are no cds, then create one
                self.cds.append(CD(cd_capacity))

    def save_as_files(self, normalize_audio, add_silence, save_path):
        """Saves audio as files"""

        self.format_2(normalize_audio, add_silence)
        makedirs(save_path)
        logging.info("moving songs now")
        for song in self.songs:
            song.add_metadata(save_path)
            dest = os.path.join(save_path,
                                f"{song.name.strip()}.{song.extension}")
            move(song.path, dest)

    def clean_up(self):
        """Deletes paths"""

        for song in self.songs:
            del song
        self.songs = []
