"""
POCCA (Python Open CV Camera Applications)
Author : µsini
Audio Manager
"""

import pygame
import os

class Sounds():
    def __init__(self, mixer):
        self.mixer = mixer
        self.folder = "../pocca/ressources/audio/"
        self.audio = {}
        for sound in os.listdir(self.folder):
            self.audio[os.path.splitext(sound)[0]] = self.mixer.Sound(self.folder + sound)


