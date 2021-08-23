"""
POCCA (Python Open CV Camera Applications)
Author : µsini
Screen Interface Manager
"""

import os
import cv2
from pocca.display.icons import Icons
from pocca.display.sounds import Sounds
import pygame
class Interface():
    def __init__(self, settings, system):
        # Get Screen Resolution
        self.settings = settings
        self.system = system
        try:
            self.resolution = system.info["resolution"]
        except:
            self.resolution = 320, 240
        # Add Pygame module into class
        self.pygame = pygame

        # Default state
        self.state = "viewfinder"
        self.start()

    def start(self):
        # Pygame
        # Screen
        if self.system.info["screen"] != None:
            # Create env variable for TFT Screen
            os.environ['XDG_RUNTIME_DIR'] = "/run/user/0" # Need for VSCode debugger
            os.environ['SDL_VIDEODRIVER'] = "fbcon"
            os.environ['SDL_FBDEV'] = "/dev/fb1"

        # Generate Pygame interface
        self.pygame.init()
        # Hide Mouse
        self.pygame.mouse.set_visible(False)
        # Set Display
        self.display = self.pygame.display.set_mode(self.resolution, 0)
        # Set Clock
        self.clock = self.pygame.time.Clock()

        self.font = pygame.font.Font("/media/usb/apps/pocca/display/font.ttf", 32)

        # Show Loading Screen
        # self.loading = LoadingScreen(self.pygame.display)
        self.icons = Icons(self.pygame.display)
        self.sounds = Sounds(self.pygame.mixer)
        # self.icons.index = "preview"

    # Display image on top left of the screen
    def top_left(self, icon_name):
        self.image(icon_name, 0, 0)

    # Display image on top right of the screen
    def top_right(self,icon_name):
        self.image(icon_name, (self.resolution[0] - 70), 0)

    def bottom(self,icon_name):
        self.image(icon_name, 0, self.resolution[1] - 70)

    # Display image saved in memory and update display
    def image(self, icon_name, top=0, left=0):
        self.display.blit(self.icons.images[icon_name], (top, left))

    # Load an image from disk and display it
    def load(self, filename, pos = (0,0)):
        image = self.pygame.image.load(filename)
        image = self.pygame.transform.scale(image, self.resolution)
        self.display.blit(image,pos)

    def to_screen_partial(self, frame, pos=(0,0)):
        self.display.blit(self.pygame.surfarray.make_surface(frame), pos)

    # Load a frame and display it
    def to_screen(self, frame):
        # Change BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Blit Array, fill the screen with the image (faster process)
        self.pygame.surfarray.blit_array(self.display, frame)

    def update(self):
        self.pygame.display.update()

    # Stop Pygame
    def stop(self):
        self.pygame.quit()

    def systemInfo(self):
        self.system.update()
        hostname = self.font.render("NAME:" + self.system.info["hostname"], 1, (255,255,255))
        self.display.blit(hostname, (0,0))
        ip = self.font.render("IP:" + self.system.info["ip"], 1, (255,255,255))
        self.display.blit(ip, (0,32))
        ssid = self.font.render("SSID:" + self.system.info["ssid"], 1, (255,255,255))
        self.display.blit(ssid, (0,64))
        app = self.font.render("APP:" + self.system.info["current_app"], 1, (255,255,255))
        self.display.blit(app, (0,96))
        internet = self.font.render("INTERNET:" + str(self.system.info["internet"]), 1, (255,255,255))
        self.display.blit(internet, (0, 128))
        quality = self.font.render("CAMERA:" + self.settings["CAMERA"]["ratio"] + " " + self.settings["CAMERA"]["quality"], 1, (255,255,255))
        self.display.blit(quality, (0, 160)) #image_size = self.font.
        fps = self.font.render("FPS:" + str(int(self.clock.get_fps())), 1, (255,255,255))
        self.display.blit(fps, (0, 192))

    # Play an audio file save in memory
    def play_audio(self, filename):
        self.sounds.audio[filename].play()

