import os
import pygame


class MusicPlayer:
    EXTENSIONS = (".wav", ".mp3")

    def __init__(self, folder):
        pygame.mixer.init()
        # Playlist: all supported audio files in the folder, sorted by name
        self.playlist = sorted(
            os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(self.EXTENSIONS)
        )
        self.index = 0            # current position in the playlist
        self.playing = False
        self.length = self._get_length()

    def _get_length(self):
        """Length of the current track in seconds."""
        if not self.playlist:
            return 0
        return pygame.mixer.Sound(self.playlist[self.index]).get_length()

    def name(self):
        if not self.playlist:
            return "No tracks"
        return os.path.basename(self.playlist[self.index])

    def play(self):
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        if not self.playlist:
            return
        self.index = (self.index + 1) % len(self.playlist)   # wraps around to the start
        self.length = self._get_length()
        self.play()

    def previous(self):
        if not self.playlist:
            return
        self.index = (self.index - 1) % len(self.playlist)   # wraps around to the end
        self.length = self._get_length()
        self.play()

    def position(self):
        """Seconds played so far."""
        if not self.playing:
            return 0
        pos = pygame.mixer.music.get_pos()   # milliseconds
        return max(pos, 0) / 1000

    def check_end(self):
        """If the track finished by itself, go to the next one."""
        if self.playing and not pygame.mixer.music.get_busy():
            self.next()