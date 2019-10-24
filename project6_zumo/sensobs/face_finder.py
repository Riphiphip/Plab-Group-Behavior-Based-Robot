import numpy as np
import cv2 as cv
import os

from project6_zumo.sensobs.sensob import Sensob

class FaceFinder(Sensob):

    def __init__(self, sensors=[]):
        super().__init__(sensors=sensors)
        file_path = "resources/haarcascade_frontalface_default.xml"
        self.cascade = cv.CascadeClassifier(file_path)

    def update(self):
        raw_output = [s.get_value() for s in self.sensors]
        self.prevData = self.preprocess(raw_output)

    def get_value(self):
        return self.prevData

    def preprocess(self, sensor_data):
        output = []
        for im in sensor_data:
            current_camera = []
            cv_image = np.array(im)
            cv_image = cv.cvtColor(cv_image, cv.COLOR_RGB2GRAY)
            faces = self.cascade.detectMultiScale(cv_image, 1.1, 4)
            for (x, y, w, h) in faces:
                current_camera.append([x,y,w,h])
            output.append(current_camera)
        return output