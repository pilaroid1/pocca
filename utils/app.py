from pocca.utils.secrets import Secrets
from pocca.utils.system import System
import configparser
import signal

class App():
    def __init__(self, settings_file = "/media/usb/pilaroid.ini", secrets_file = "/media/usb/secrets.ini"):

        # Settings
        self.settings_file = settings_file
        self.settings = configparser.ConfigParser()
        self.settings.read(settings_file)

        # Secrets
        self.secret_file = secrets_file
        self.secrets = configparser.ConfigParser()
        self.secrets.read(secrets_file)

        self.running = True

        self.decoder = Secrets()
        # System Info
        self.system = System()

        # Translation
        try:
            if self.settings["APPLICATION"]["lang"] == "fr":
                from pocca.localization.fr import TEXT
            elif self.settings["APPLICATION"]["lang"] == "en":
                from pocca.localization.en import TEXT
        except:
            from pocca.localization.en import TEXT

        self.TEXT = TEXT()

        # Path
        self.path = {}
        try:
            self.path["images"] = self.settings["FOLDERS"]["images"]
        except:
            self.path["images"] = "/media/usb/images"
        try:
            self.path["temp"] = self.settings["FOLDERS"]["temp"]
        except:
            self.path["temp"] = "/media/usb/tmp"

        self.get_camera_resolution()

    def get_camera_resolution(self):
        if self.settings.has_section("CAMERA"):
            if self.settings.has_option("CAMERA", "ratio") and self.settings.has_option("CAMERA","quality"):
                if self.settings["CAMERA"]["ratio"] == "16:9":
                    if self.settings["CAMERA"]["quality"] == "high":
                        self.camera_resolution = (1920,1080)
                    elif self.settings["CAMERA"]["quality"] == "medium":
                        self.camera_resolution = (1640,922)
                    elif self.settings["CAMERA"]["quality"] == "low":
                        self.camera_resolution = (1280,720)
                if self.settings["CAMERA"]["ratio"] == "4:3":
                    if self.settings["CAMERA"]["quality"] == "high":
                        self.camera_resolution = (1152,864)
                    if self.settings["CAMERA"]["quality"] == "medium":
                        self.camera_resolution = (640,480)
                    if self.settings["CAMERA"]["quality"] == "low":
                        self.camera_resolution = (320,240)
        else:
            self.camera_resolution = (1280,720)

    def stop_function(self, sigint_handler):
        signal.signal(signal.SIGINT, sigint_handler)

    def clear_terminal(self):
        print("\033c", end="") # Clear Terminal
