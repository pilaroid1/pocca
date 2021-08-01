"""
POCCA (Python Open CV Camera Applications)
Author : µsini
Buttons Manager
"""

import pygame
from pygame.locals import *
from gpiozero import Button

class Buttons():
    NOACTION = -1
    BTN = 0
    BTN2 = 1
    BTN3 = 2
    BTN4 = 3
    name = []
    gpio = [ 17, 22, 23, 27]
    def __init__(self, TEXT):
        self.action = self.NOACTION
        self.exit = False
        self.debug = False
        self.buttons = []
        self.name = [ TEXT.BUTTON, TEXT.BUTTON + " 2", TEXT.BUTTON + " 3", TEXT.BUTTON + " 4"]
        self.pressed = TEXT.PRESSED
        for io in self.gpio:
            self.buttons.append(Button(io))
        self.buttons[0].when_released = self.btn
        self.buttons[1].when_released = self.btn2
        self.buttons[2].when_released = self.btn3
        self.buttons[3].when_released = self.btn4

    def btn(self):
        self.action = self.BTN

    def btn2(self):
        self.action = self.BTN2

    def btn3(self):
        self.action = self.BTN3

    def btn4(self):
        self.action = self.BTN4

    def check(self):
        if(self.action != self.NOACTION):
            action = self.action
            print(str(self.name[action]) + self.pressed)
            self.action = self.NOACTION
            return action
        return self.NOACTION

