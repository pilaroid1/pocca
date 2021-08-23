"""
VisionCam Brain
Author :
PiCamera Manager
"""

import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import os
import cv2
import uuid
import json

class Camera():
    def __init__(self, settings, TEXT, camera_resolution):
        self.active = False

        # Get Camera Resolution
        self.resolution = camera_resolution
        #int(settings["CAMERA"]["width"]), int(settings["CAMERA"]["height"])

        # Create PiCamera Stream
        self.stream = PiCamera()
        self.rawCapture = ""
        self.capture = False
        self.frame = ""
        self.temp_path = settings["FOLDERS"]["temp"]
        self.start(self.resolution)
        self.type = settings["APPLICATION"]["type"]
        self.name = settings["APPLICATION"]["name"]

    # Start picamera capture
    def start(self, resolution):
        # Set Camera Resolution
        self.stream.resolution = resolution
        #self.resolution
        # self.stream.framerate = 32
        self.rawCapture = PiRGBArray(self.stream, self.resolution)
        time.sleep(0.1)

    # Resize frame (to fit screen for ex.)
    def resize(self, frame, size):
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, size, interpolation = cv2.INTER_AREA)
        frame = frame.swapaxes(0, 1)
        return frame

    # Save frame to disk
    def save(self, frame, path="/media/usb/images", filename="img"):
        open(self.temp_path + "/" + "usbaccess", "x")
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        list_images = os.listdir(path)
        img_nb = len(list_images)
        filename = path + "/" + filename + str(img_nb) + ".jpg"
        print("📁 " + filename)
        cv2.imwrite(filename, frame)
        os.remove(self.temp_path + "/" + "usbaccess")
        return filename

    # Save frame to disk with an unique ID
    def save_uid(self, frame, path="/media/usb/images", filename="img"):
        open(self.temp_path + "/" + "usbaccess", "x")
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        list_images = os.listdir(path)
        img_nb = len(list_images)
        filename = path + "/" + filename + str(uuid.uuid4())[:8] + ".jpg"
        print("📁 " + filename)
        cv2.imwrite(filename, frame)
        os.remove(self.temp_path + "/" + "usbaccess")
        return filename

    def save_timestamp(self, filename):
        ts = time.time()
        objTimeStamp = {
            "filename": os.path.basename(filename),
            "timestamp": ts
        }
        with open(self.temp_path + "/last_image.json", 'w') as outfile:
            json.dump(objTimeStamp, outfile)

    # Crop an image vertically
    def crop_v(self, frame, crop):
        frame = frame[0:720, crop[0]:crop[1]]
        return frame

    # Delete temp images
    def clear_temp(self):
        try:
            os.remove(self.temp_path + "/" + "usbaccess")
        except:
            pass
        try:
            if(len(os.listdir(self.temp_path + "/images/")) != 0):
                for img in os.listdir(self.temp_path + "/images/"):
                    #print("Effacement" + self.temp_path)
                    os.remove(self.temp_path + "/images/"+ img)
        except:
            print("Impossible d'effacer ce fichier")

    # Count files in folder
    def count(self):
        return len(os.listdir(self.temp_path + "/images"))

    def refresh(self):
        self.rawCapture.truncate(0)

    def enable(self):
        self.active = True

    def disable(self):
        self.active = False

    def stop(self):
        self.stream.close()
