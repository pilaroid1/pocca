"""
POCCA (Python Open CV Camera Applications)
Author : µsini
Images Ressources Manager
"""

import pygame
import os

class Icons():
    def __init__(self, display):
        self.display = display
        self.folder = "../pocca/ressources/images/"
        self.images = {}
        for image in os.listdir(self.folder):
            self.images[os.path.splitext(image)[0]] = pygame.image.load(self.folder + image).convert_alpha()

