import pygame
import os


class MusicPlayer:
    def __init__(self, folder):
        pygame.mixer.init()
        self.folder = folder
        self.playlist = [f for f in os.listdir(folder) if f.endswith(".wav")]
        self.playlist.sort()
        self.index = 0

    def load(self):
        track = self.playlist[self.index]
        path = os.path.join(self.folder, track)
        pygame.mixer.music.load(path)

    def play(self):
        self.load()
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        pygame.mixer.music.stop()
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.playlist)
        pygame.mixer.music.stop()
        self.play()

    def current(self):
        return self.playlist[self.index]