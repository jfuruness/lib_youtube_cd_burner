import subprocess
import time
import fcntl
import os
from contextlib import contextmanager

from .disk_values_enum import DiskValues
from .song_holder import SongHolder

class CDFullError(Exception):
    pass

class CD(SongHolder):
    """CD class that adds songs and burns cds"""

    def __init__(self, max_seconds):
        """initializes cd and max seconds a cd can hold"""

        self.max_seconds = max_seconds
        self.total_seconds = 0
        super(CD, self).__init__()

    def add_track(self, song):
        """Adds a song to a cd, returns false if over limit"""

        # If the song is not over the limit of seconds
        if self.total_seconds + song.seconds <= self.max_seconds:
            # Add the song
            self.songs.append(song)
            # Increase total seconds
            self.total_seconds += song.seconds
        # Song too long return false, cd full
        else:
            raise CDFullError

    def burn(self, times_to_burn=1):
        """Burns a cd times_to_burn times"""

        for i in range(times_to_burn):
            # Wait for disk insertion
            if self._get_disk():
                # args for bash command
                args = [#"sudo",
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
                logging.debug(output)
                logging.info("Just burned {}".format(self))
                # Pops the new cd out
                CD.eject()
            else:
                logging.warning("Disk not inserted, exiting")

    def _get_disk(self):
        """Waits for disk insertion"""

        # Pops out cd
        CD.eject()
        logging.info("Insert cd!")

        while self._get_disk_val() == Disk_Values.OPEN.value:
            logging.info("Disk tray open\r")
            time.sleep(1)
        while self._get_disk_val() == Disk_Values.READING.value:
            logging.info("Reading in disk\r")
            time.sleep(1)
        if self._get_disk_val() == Disk_Values.NO_DISK.value:
            logging.warning("No disk inserted")
            return False
        elif self._get_disk_val() == Disk_Values.DISK_IN_TRAY.value:
            logging.info("Disk in tray and read")
            return True

    def _get_disk_val(self):

        # https://superuser.com/a/1367091
        # 1 for no disk, 2 for open, 3 for reading, 4 for disk in tray
        with self._open_disk_fd() as fd:
            return fcntl.ioctl(fd, 0x5326)

    @contextmanager
    def _open_disk_fd(self):
        fd = os.open('/dev/sr0', os.O_RDONLY | os.O_NONBLOCK)
        yield fd
        os.close(fd)

    @staticmethod
    def eject(self):
        """Pops out CD"""
        subprocess.run(["eject"])

    def __str__(self):
        """For when cd's are printed"""

        lines = ["cd is {} minutes".format(self.total_seconds/60),
                 "songs:"]
        [lines.append("    " + x.__str__()) for x in self.songs]
        lines.append("\n")
        return "\n".join(lines)
