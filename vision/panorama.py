"""
VisionCam Brain
Author :
Panaorama Stitcher

Source : https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/
"""
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import time
import os
import uuid

class Panorama():
    def __init__(self, path_images="/media/usb/images", path_temp="/media/usb/tmp", pano_images=4, image_size=(1280,720)):
        self.status = -1
        self.path_images = path_images
        self.path_temp = path_temp
        self.stitched = None
        self.images = pano_images
        self.image_size = image_size

    def save(self, filename):
        print("📁 " + filename)
        cv2.imwrite(filename, self.stitched)
        return filename

    # Stitch images using Features Detections
    def join_images(self, filename_images, stitched_name = "stitched.png"):
        images = []
        for image in filename_images:
            images.append(cv2.imread(self.path_temp + "/" + image))
        # Create Stitcher Objects
        stitcher = cv2.Stitcher_create()
        # Apply Stitcher Algorithm to images
        (self.status, self.stitched) = stitcher.stitch(images)

        # Generate Borders
        self.stitched = cv2.copyMakeBorder(self.stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
        #cv2.imwrite(self.path_temp + stitched_name, self.stitched)

    """
    Manual Cropper
    """

    # Crop images to remove black borders
    def crop_images(self, crop_size):
        shape = self.stitched.shape
        self.stitched = self.stitched[crop_size:shape[0]-crop_size, crop_size:shape[1]-crop_size]

    """
    Automatic Cropper
    """
    # Apply a filter to get only Black parts
    # Not used here, as it has a tendency to fail if images has parts which are too dark
    def get_contours(self):
        gray = cv2.cvtColor(self.stitched, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("/media/usb/images/gray.png", gray)
        self.thres = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(self.thres.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        self.c = max(cnts, key=cv2.contourArea)
        # cv2.imwrite(self.path + "temp/threshold.png", self.thres)

    # Get value for the contours
    def set_contours_mask(self):
        self.mask = np.zeros(self.thres.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(self.c)
        cv2.rectangle(self.mask, (x,y), (x + w, y + h), 255, -1)

    # Apply crop based on contours detection
    def set_contours(self):
        minRect = self.mask.copy()
        sub = self.mask.copy()
        while cv2.countNonZero(sub) > 0:
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, self.thres)

        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        self.c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(self.c)
        self.stitched = self.stitched[y:y + h, x:x + w]
