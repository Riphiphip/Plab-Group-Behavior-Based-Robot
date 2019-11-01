""" Supplied camera module"""

import os
from time import sleep
from PIL import Image
from picamera import PiCamera


class Camera():
    """
    Uses RasPi camera to take a picture and save.
    """
    def __init__(self, img_width=50, img_height=37, filetype="png", camera=PiCamera()):
        
        self.camera = camera
        self.camera.resolution= (img_width, img_height)
        self.value = None
        self.filetype = str(filetype)
        sleep(2)

    def get_value(self):
        """Getter for value"""
        return self.value

    def update(self):
        """Update"""
        self.sensor_get_value()
        return self.value

    def reset(self):
        """Reset"""
        self.value = None

    def sensor_get_value(self):
        self.camera.capture('project6_supply/sensors/image.'+self.filetype, use_video_port=True)
        self.value = Image.open('project6_supply/sensors/image.'+self.filetype).convert('RGB')
