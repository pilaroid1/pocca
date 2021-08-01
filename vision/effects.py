"""
VisionCam Brain
Author : 
Effects
"""
import cv2
import numpy as np

class Effects():
    def __init__(self):
        # Set Effects
        self.id = 0
        self.name = ["noeffect", "contours"]
        self.EFFECT_NONE = 0
        self.EFFECT_CONTOURS = 1

    # Tutorial   : https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    # Definition : https://en.wikipedia.org/wiki/Canny_edge_detector
    def canny_edge(self, frame, sigma=0.33):
        """
            Prepare images for Canny Filter
        """
        # Convert image to Gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert Grey image to blurred image
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        # Compute the median of the single channel pixel intensities
        v = np.median(blurred)

        """
            Apply Canny Filter
        """
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)

        # Convert result back to RGB to display
        frame = cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)
        return frame

    def color_change(self, frame, color):
        Conv_hsv_Gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
        frame[mask == 255] = color
        return frame
