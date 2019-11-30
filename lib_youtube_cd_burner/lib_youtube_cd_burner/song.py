#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains class Song

The song class formats the song to be used in an audio CD. The
formatting is neccessary or else the song will not play on a CD. This is
done through a series of steps.

1. The metadata is generated for the song
    -Handled in the _generate_meta_data function
    -This is so that other parts of the program can use this metadata
    -Must be called after any change to the song

2. The song is formatted in the format_song function

3. The song is converted to WAV format.
    -This is handled in _convert_to_wav function

4. The metadata is regenerated
    -Handled in the _generate_meta_data function
    -Must be called after every step because the metadata changes

5. Frame rate is set to 44100. Channels are set to 2.
    -Handled in the format_song function
    -This is neccessary for an audio CD

6. The new audio is exported to the file
    -Handled in format_song function
    -This overwrites the old file with the new song
    -The new song is now
        -WAV
        -Frame rate of 44100 Herz
        -2 Channels

7. The type of the audio is then changed to PCM16
    -Handled in the format_song function
    -This is neccessary for an audio CD

8. If remove_silence, silence at the end of song is removed
    -Handled in the format_song function
    -This is within a certain range of decibels
        -Later versions will be able to customize this
    -This function takes a while to run

9. Three seconds of silence are added to the song
    -Handled in the format_song function

10. Metadata is generated again, this time removing the audio_segment
    -The audio segment takes up a massive amount of ram

The song can also be changed to match the target amplitude. Details for
this can be found in the function match_target_amplitude.

Design Choices:
    -All songs are converted to WAV, 44100Hz, and have two channels
        -This is neccessary for audio CDs
    -All songs have an added three seconds
        -This will be an option in future version, 3 seconds is standard
    -remove_silence arg is false by default because it takes a while
    -Match target amplitude is included so that songs do not jump in
     volume from one song to the next

Possible Future Improvements:
    -remove_silence should be customizable for decible range
    -three seconds of silence should be customizable
"""

import os
import re
from os.path import basename, normpath
import soundfile as sf
from pydub import AudioSegment, silence
from subprocess import check_call, DEVNULL
from mutagen.easyid3 import EasyID3
from .utils import error_catcher

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__Version__ = "0.1.0"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Production"


class Song:
    """This class contains information about a song.

    This class can format a song and change its decible level.
    For an in depth explanation, see the top of the module"""

    __slots__ = ['path', 'logger', 'extension', 'audio_segment',
                 'milliseconds', 'seconds', 'volume', "og_path"]

#    @error_catcher()
    def __init__(self, path, name, logger):
        """Initializes path, name, and metadata"""

        # The path to the song file
        self.path = path
        # The logger
        self.logger = logger
        # Put this here so as not to pass around strings
        self.extension = path.split(".")[-1]
        # The meta data, for ex seconds
        self._generate_meta_data()
        self.logger.debug("Initialized Song with path {}".format(path))

    def __str__(self):
        """Returns the name of the song"""

        return self.name

    @error_catcher()
    def format_song(self, remove_silence=False, song_format="wav"):
        """This function formats a song.

        The song is converted to WAV, 44100 Herz, and bidrectional. Then
        the silence at the end of the song can optionally be removed if
        remove_silence is true, although this is slow, and three seconds
        are added on to the end of the song. For a more in depth
        explanation see the top of the module.
        """

        self.logger.info("Formatting {}".format(self.path))
        # Formats the audio segment to WAV, 44100Hz, and bidrectional
        self._format_audio_segment(song_format=song_format)

        if song_format in ["wav", "WAV"]:
            # Changes the audio to pcm_16, neccessary for CD's
            data, sample_rate = sf.read(self.path)
            sf.write(self.path, data, sample_rate, subtype='PCM_16')

        self._generate_meta_data(audio_segment=True)
        # Removes silence from the end of the playlist if called
        # Default is fale because it takes a long time
        if remove_silence:
            self.remove_silence()
        # We do NOT add silence here because later audio is normalized
        # It will change the silence, and also mess up the avg volume
        # Regenerates meta data and gets rid of the audio segment
        self._generate_meta_data()
        if self.path != self.og_path:
            os.remove(self.og_path)

    def add_silence(self):
        """Adds 3 seconds of silence"""

        self._generate_meta_data(audio_segment=True)
        # Adds three seconds to the end of the audio segment
        self.audio_segment += AudioSegment.silent(duration=3000)
        self.audio_segment.export(self.path, format=self.extension)
        self._generate_meta_data()

    # https://stackoverflow.com/a/42496373
    @error_catcher()
    def match_target_amplitude(self, target_dBFS):
        """Matches target amplitude.

        Used for when songs are different volumes back to back.
        """

        self._generate_meta_data(self.path, audio_segment=True)
        change_in_dBFS = target_dBFS - self.audio_segment.dBFS
        print(self.audio_segment.dBFS)
        print(change_in_dBFS)
        self.audio_segment = self.audio_segment.apply_gain(change_in_dBFS)
        self.audio_segment.export(self.path, format=self.extension)
        self._generate_meta_data(self.path)

    @error_catcher()
    def add_metadata(self, save_path):
        audio = EasyID3(self.path)
        # https://stackoverflow.com/a/3925147
        audio['title'] = basename(normpath(self.path))
        # https://stackoverflow.com/a/34970600
        audio['album'] = basename(normpath(save_path))
        audio.save()

########################
### Helper Functions ###
########################

    @error_catcher()
    def _format_audio_segment(self, song_format="wav"):
        """Changed to WAV, 44100Hz, bidirectional."""

        # Need this here because ffmpeg changes the song format outside of
        # my program, which will mess up the file extensions

        # Should prob have this section as a documented func for reformatting
        self.extension = "wav"
        self.path = "{}.{}".format(self.path.rsplit('.', 1)[0], "wav")
        # Must have this, pydub breaks on surround sound 5.1
        # this converts all songs to sterio
        converted = "{}.{}".format(self.path.rsplit('.', 1)[0], "converted.wav")
        convert_str = 'sudo ffmpeg -i "'
        convert_str += self.path
        convert_str += '" -ac 2 "'
        convert_str += converted + '"'
        check_call(convert_str, shell=True, stdout=DEVNULL, stderr=DEVNULL)
        self.path = converted
        self.og_path = self.path
        reformatted_path = [re.sub('[^А-яa-zA-Z0-9_/]+', ' ', x)
                            for x in self.path.split(".")[:-2]]

        new_path = ''.join(reformatted_path) + "." + self.path.split(".")[-1]
        os.rename(self.path, new_path)
        self.og_path = new_path
        self.path = new_path
        # Done so that the audio segment gets generated
        self._generate_meta_data(audio_segment=True)
        # Gets the new path for a WAV formatted song for audio CD
        new_path = "{}.{}".format(self.path.rsplit('.', 1)[0], song_format)
        self.extension = song_format
        # Sets the Herz to 44100 for audio CD
        self.audio_segment = self.audio_segment.set_frame_rate(44100)
        # Makes bidrectional for audio CD
        self.audio_segment = self.audio_segment.set_channels(2)
        # Exports with the format being a WAV
        self.audio_segment.export(new_path, format=self.extension)
        self._generate_meta_data(path=new_path)

    @error_catcher()
    def _remove_silence(self):
        """Removes the silence from the end of the song."""

        # Gets the last bit of silence that's at least one sec
        start, stop = silence.detect_silence(self.audio_segment,
                                             min_silence_len=1000,
                                             silence_thresh=-30)[-1]
        # If the stop is the same as the end of the song
        if stop == self.milliseconds:
            # Remove the last part of the song
            self.audio_segment = self.audio_segment[:start]
            self.audio_segment.export(self.path, format=self.extension)
            self.generate_meta_data(self.path)

    @error_catcher()
    def _generate_meta_data(self, path=None, audio_segment=False):
        """Generates path, seconds, volume and audio segment."""

        self.path = path if path else self.path
        self.audio_segment = AudioSegment.from_file(self.path, self.extension)
        self.milliseconds = len(self.audio_segment)
        self.seconds = self.milliseconds/1000
        self.volume = self.audio_segment.dBFS
        # Can't fit onto one line and would be unreadable
        if not audio_segment:
            # Gets rid of the massive amount of ram this consumes
            self.audio_segment = None
        self.path = "{}.{}".format(self.path.rsplit('.', 1)[0], self.extension)

    @property
    def name(self):
        return basename(normpath(self.path)).replace("." + self.extension, "")
