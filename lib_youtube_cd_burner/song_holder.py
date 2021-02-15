import logging


class SongHolder:
    """Parent class that contains songs"""

    def __init__(self):
        self.songs = []

    def format_1(self,
                 remove_silence: bool,
                 randomize: bool,
                 song_format: str):
        """Removes silence. Formats as wav, mp3, etc. Randomizes"""

        # removes silence and formats song
        for song in self.songs:
            song.format_song(remove_silence, song_format)
        if randomize:
            shuffle(self.songs)

    def format_2(self, normalize, add_silence):
        """Normalize audio and add silence

        Cannot combine with format 1 since format 1 can occur before
        songs are split into CDs, but this must occur only after."""

        if normalize:
            self.normalize_audio()
        if add_silence:
            # After normalizing audio, now add silence
            for song in self.songs:
                song.add_silence()

    def normalize_audio(self):
        """Makes audio not spike as much between switching songs"""

        # Average Volume
        avg_dbfs = sum([x.volume for x in self.songs])/len(self.songs)
        logging.debug(f"Volumes: {[x.volume for x in self.songs]}")
        logging.debug(f"avg dbfs: {avg_dbfs}")
        for song in self.songs:
            logging.info(f"Normalizing audio for {song.name}")
            song.match_target_amplitude(avg_dbfs)
