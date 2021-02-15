from argparse import ArgumentParser
import logging

from lib_utils.print_funcs import config_logging

from .app import App
from .youtube_playlist import YoutubePlaylist


def main():
    parser = ArgumentParser(description='CD Burner')
    url = "https://www.youtube.com/watch?v=jLtbFWJm9_M"
    parser.add_argument('--run', action="store", default=False)
    parser.add_argument('--urls', action="store", default=url)
    parser.add_argument('--dl_path', action="store", default="/tmp/yt")
    parser.add_argument('--save_path', action="store", default="/tmp/yt2")
    parser.add_argument('--song_format', action="store", default="mp3")
    args = parser.parse_args()
    config_logging(logging.DEBUG)
    if args.run:
        YoutubePlaylist(args.urls.split(","),
                        args.dl_path).generate_audio_medium(save_path=args.save_path,
                                                            song_format=args.song_format)
    else:
        App.create_app()
