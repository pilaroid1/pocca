"""
VisionCam Brain
Author :
FFMPEG Converter wrapper
"""
import os
import uuid

class Convert():
    error_level = -1
    def __init__(self, TEXT):
        self.text_convert_gif = TEXT.CONVERT_TO_GIF

    # https://stackoverflow.com/questions/44292168/generate-gif-from-jpeg-images-using-ffmpeg
    def gif(self, source, destination, gif_fps):
        # Get Timestamp
        image_id = str(uuid.uuid4())[:8]

        # Execute FFMPEG silent, to convert list of images into a gif
        result = os.system("ffmpeg -hide_banner -loglevel error -y -f image2 -r "+ gif_fps + " -i " + source + "/gif%d.jpg " + source + "/gif" + image_id + ".gif")
        os.rename(source + "/gif" + image_id + ".gif", destination + "/gif" + image_id + ".gif")
        filename = destination + "/gif" + image_id + ".gif"
        self.error_level = result
        return result, filename
