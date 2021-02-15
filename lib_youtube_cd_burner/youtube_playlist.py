import logging
import math
import os

from lib_utils.file_funcs import delete_paths

from .playlist import Playlist
from .song import Song
from .youtube_dl_fix import Youtube_dl_fix


class MyLogger(object):
    """Logger class use by youtube_dl"""

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


class YoutubePlaylist(Playlist):
    """inits a youtube playlist instance"""

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
                zeroes = int(math.log10(len(self.urls))) + 1
                url_indicator = "{:0" + str(zeroes) + "d}"
                url_indicator = url_indicator.format(i)
                # Download songs
                ydl_opts['outtmpl'] = self.dl_path + "/" + url_indicator + og
                logging.debug(f"path fmt is {ydl_opts['outtmpl']}")
                with Youtube_dl_fix(ydl_opts) as ydl:
                    ydl.download([url])
        except Exception as e:
            print(f"dl songs {e}")
            logging.warning(f"Video download failed. Probably webm file {e}")

    def my_hook(self, d):
        """What happens when a song is downloaded"""

        name = d['filename'].rsplit('.', 1)[0]
        if d['status'] == 'finished':
            logging.info(f'Done downloading {name}')
            song = Song(d['filename'], name)
            # Makes sure that the song downloaded and has volume
            if os.path.exists(song.path):
                if song.volume > -float('Inf'):
                    self.songs.append(song)
                else:
                    logging.warning(f"{name} has no volume. Not including")
                    delete_paths(song.path)
            # If it didn't download don't include it
            else:
                logging.warning(f"{name} didn't download properly")
