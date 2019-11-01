# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:33:57 2019

@author: Joule
"""

# import numpy as np
# import cv2 as cv
from abc import ABC, abstractmethod
import math
import colorsys

from PIL import Image
from project6_supply.sensors.reflectance_sensors import ReflectanceSensors
from project6_supply.sensors.ultrasonic import Ultrasonic
from project6_supply.sensors.camera import Camera
from project6_supply.imager2 import Imager


class Sensob(ABC):
    """A sensob serves as an interface between (one or more) sensors (of the agent) and the bbcon’s
    behaviors. Note that a single sensor may be shared by
    several sensobs, and a sensob may employ several sensors. The main method for a sensob is update, which should force the sensob to fetch the relevant sensor
    value(s) and convert them into the pre-processed sensob value. This should only need to be done
    once each timestep. So even if several behaviors share the same sensob, S, there should be no need
    for S to update more than once each timestep.

    The main instance variables of a sensob are a) its associated sensor(s) and b) its value."""

    """You will write code for sensobs, and that code will call the SWs. Each SW provides a very simple
    interface for sensobs, with just a few (standard) methods such as update and get value. Each SW
    does a small amount of preprocessing of the (completely) raw sensory data, but the information
    that each sensob receives (by calling a wrapper’s get value method) is also fairly basic, and open
    for many additional forms of preprocessing."""

    def __init__(self, sensors=[]):
        self.data = 1
        self.sensors = sensors

    def update(self):
        raw_output = [s.get_value() for s in self.sensors]
        self.data = self.preprocess(raw_output)

    def get_value(self):
        return self.data

    @abstractmethod
    def preprocess(self, sensor_data):
        '''Preprocessing of raw data'''


class EdgeFinder(Sensob):
    """
        Uses Reflectance-sensors to look for edge
    """

    def __init__(self, sensors=[ReflectanceSensors(False, 400, 3000)]):
        super().__init__(sensors=sensors)
    
    def __str__(self):
        return "EdgeFinder"

    def preprocess(self, sensor_data):
        return sensor_data

    def update(self):
        raw_output = self.sensors[0].update()
        print("IR sensors returns", raw_output)
        self.data = self.preprocess(raw_output)
        return self.data


class ColorFinder(Sensob):
    '''
    Looks for color R, G or B in image and determines if
    there is more of it to the left, right, center or not
    enough at all.
    Value: [left avg. color, middle avg. color, right avg.color]
    '''

    def __init__(self, sensors=[Camera()], color=None, threshold=5, seg_number=3):
        super().__init__(sensors=sensors)
        self.threshold = threshold
        self.seg_number = seg_number
        self.camera = Camera()
        self.data = None
        if color:
            self.color = color
        else:
            self.calibrate()

    def preprocess(self, sensor_data):
        '''Gives a percentage of pixels of an image classified as self.color'''
        width = sensor_data.width
        height = sensor_data.height
        seg_width = (int)(math.floor(width/self.seg_number))
        partitions = []
        for i in range(self.seg_number):
            partitions.append(sensor_data.crop(box=(i*seg_width, 0, (i+1)*seg_width, sensor_data.height-1)))
        for i, part in enumerate(partitions):
            valid_count = 0
            pixel_count = 0
            for x in range(seg_width-1):
                for y in range(height-1):
                    pix = part.getpixel((x, y))
                    hls_rep = colorsys.rgb_to_hls(pix[0], pix[1], pix[2])
                    if hls_rep[0] < self.color[0] + self.threshold and hls_rep > self.color[1] - self.threshold:
                        valid_count += 1
                    pixel_count += 1
            partitions[i] = valid_count/pixel_count
        return partitions

    def update(self):
        output = []
        for camera in self.sensors:
            output.append(self.preprocess(camera.get_value()))
        self.data = output
        return output
    
    # def find_direction(self):
    #     self.imager.get_image_dims()
    #     total_pixels = int(self.imager.xmax) * int(self.imager.ymax) / 3 #total pixel per side
    #     list_sides = [0, 0, 0]
    #     for side in range(3):
    #         green_pixels = 0
    #         for x in range(int(int(self.imager.xmax)/3)*(side),
    #                        int(int(self.imager.xmax)/3)*(side+1)):
    #             for y in range(int(self.imager.ymax)):
    #                 r, g, b = self.imager.get_pixel(x, y)
    #                 if g-r > 40 and g-b > 40:
    #                     green_pixels += 1
    #         list_sides[side] = green_pixels / total_pixels
    #     self.data = list_sides
    #     return list_sides

    # def get_pixel(self, x, y):
    #     return self.picture.getpixel((x, y))

    def calibrate(self):
        '''Estimates color of object in front of camera to be used for reference'''
        ref_img = (self.sensors[0].update())
        l_thresh = (int)(math.floor(ref_img.width/3))
        r_thresh = 2*l_thresh
        ref_img = ref_img.resize((1, 1), box=(l_thresh, 0, r_thresh, ref_img.height-1))
        pix_rgb = ref_img.getpixel((0, 0))
        self.color = colorsys.rgb_to_hls(pix_rgb[0], pix_rgb[1], pix_rgb[2])
        print("Kalibrert farge (HSV): " + str(self.color))     

class Collition(Sensob):
    """ Ultrasound collition detection.
    Returns distance in cm. """

    def __init__(self, sensors=[Ultrasonic()]):
        super().__init__(sensors=sensors)
        # Set data to very high value
        self.data = 1500

    def __str__(self):
        return "Collition"

    def update(self):
        raw_output = [s.get_value() for s in self.sensors]
        self.data = self.preprocess(raw_output)
        

    def preprocess(self, sensor_data):
        print("Ultrasonic snesob output is:",sensor_data[0])
        self.data = sensor_data[0]
        return sensor_data[0]