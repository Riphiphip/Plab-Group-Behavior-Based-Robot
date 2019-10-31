# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:33:57 2019

@author: Joule
"""

# import numpy as np
# import cv2 as cv
from abc import ABC, abstractmethod
import math

from PIL import Image
from project6_supply.sensors.reflectance_sensors import ReflectanceSensors


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
        self.prevData = 1
        self.sensors = sensors

    def update(self):
        raw_output = [s.get_value() for s in self.sensors]
        self.prevData = self.preprocess(raw_output)

    def get_value(self):
        return self.prevData

    @abstractmethod
    def preprocess(self, sensor_data):
        '''Preprocessing of raw data'''


# class FaceFinder(Sensob):

#     def __init__(self, sensors=[]):
#         super().__init__(sensors=sensors)
#         file_path = "resources/haarcascade_frontalface_default.xml"
#         self.cascade = cv.CascadeClassifier(file_path)


#     def preprocess(self, sensor_data):
#         output = []
#         for image in sensor_data:
#             current_camera = []
#             cv_image = np.array(image)
#             cv_image = cv.cvtColor(cv_image, cv.COLOR_RGB2GRAY)
#             faces = self.cascade.detectMultiScale(cv_image, 1.1, 4)
#             for (x, y, w, h) in faces:
#                 current_camera.append([x,y,w,h])
#             output.append(current_camera)
#         return output


class EdgeFinder(Sensob):
    """
        Uses Reflectance-sensors to look for edge
    """

    def __init__(self, sensors=[ReflectanceSensors(False, 400, 3000)]):
        super().__init__(sensors=sensors)

    def preprocess(self, sensor_data):
        return sum(sensor_data)

    def update(self):
        raw_output = self.sensors[0].update()
        self.prevData = raw_output
        return self.get_value()



class ColorFinder(Sensob):
    '''
    Looks for color R, G or B in image and determines if
    there is more of it to the left, right, center or not
    enough at all.
    Value: [left avg. color, middle avg. color, right avg.color]
    '''

    def __init__(self, sensors=[], color=0):
        super().__init__(sensors=sensors)
        self.color = color

    def preprocess(self, sensor_data: Image.Image):
        seg_width = (int)(math.floor(sensor_data.width/3))
        partitions = []
        for i in range(3):
            partitions.append(sensor_data.crop(box=(i*seg_width+1, 0, (i+1)*seg_width, sensor_data.height-1)))
            print((i*seg_width+1, 0, (i+1)*seg_width, sensor_data.height-1))
        for i, img in enumerate(partitions):
            partitions[i] = img.resize((1, 1)).getpixel(1, 1)[self.color]
        return partitions
        
        