#make it so that it displays downloading bar
import os
from .playlist import Youtube_Playlist
from .logger import Logger
import sys
import time
import shutil
import subprocess
#burin cds, add option to make random burn
#add about sudo, and about multiple disc drives
class CD_Burner(Logger):
    def __init__(self):
        # Need sudo to access cd, and wodim
        self.logger = self._initialize_logger({})
        self.upgrade_to_sudo()
        self.playlists = []
        playlist_strings = self.get_playlist_strings()
        for i in range(len(playlist_strings)):
            if "youtube" in playlist_strings[i]:
                self.playlists.append(Youtube_Playlist(playlist_strings[i], self.logger))
            else:
                self.playlists.append(Playlist(playlist_strings[i], "directory", playlist_strings[i]))
        
    def get_playlist_strings(self):
        playlist_strings = []
        playlist_string = input("Enter playlist, either as a url or as a directory path: ")
        while playlist_string != "q":
            playlist_strings.append(playlist_string)
            playlist_string = input("Enter another playlist url, or q when done")
        return playlist_strings

    #https://stackoverflow.com/a/20153881
    def upgrade_to_sudo(self):
        ret = 0
        if os.geteuid() != 0:
            msg = "[sudo] password for %u:"
            ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
            #https://gist.github.com/davejamesmiller/1965559
            os.execvp("sudo", ["sudo"] + ["python3"] + sys.argv)
            print(ret)
            print("upgraded?")
        if ret != 0:
            print("User is not a sudo user. This application will now exit.")
            sys.exit(1)

    def yes_no_input(self, query):
        answer = input("{} Yes or No: ".format(query)).lower().strip()
        while answer not in ['yes', 'no']:
            answer = input("{} Yes or No?".format(query))
        if answer == 'yes':
            return True
        else:
            return False


    def create_cds(self, cd_by_cd=False):
        if cd_by_cd:
            for playlist in self.playlists:
                playlist.download_songs()
                playlist.generate_cds()
                if self.yes_no_input("Would you like to burn CDs?"):
                    playlist.burn_cds()
                if self.yes_no_input("Would you like to delete all the files in this playlist?"):
                    playlist.clean_up()
            if self.yes_no_input("Would you like to delete all the files?"):
                self.clean_up()
        else:
            print(self.playlists)
            for x in self.playlists:
                x.download_songs()
                x.generate_cds()
            if self.yes_no_input("Would you like to burn CDs?"):
                for x in self.playlists:
                    x.burn_cds()
