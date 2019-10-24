# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:05:15 2019

@author: Joule
"""

from project6_zumo.bbcon import BBCON
from project6_zumo.behaviors.behavior import Behavior


class FaceHunting(Behavior):
    '''Looks at last camera picture and determines whether there is
        a face or not. Attempts to follow the face if found'''

    ROTATION_SPEED = 1
    DRIVE_SPEED = 1

    def __init__(self, controller: BBCON, priority: float, sensors=[]):
        if sensors.length != 1:
            raise ValueError("Only takes one sensob")
        super().__init__(controller, priority, sensors=sensors)
        self.image_width = sensors[0].sensors[0].img_width
        self.image_height = sensors[0].sensors[0].img_height

    def consider_deactivation(self):
        """whenever a behavior is active, it should test whether it should deactivate."""
        #Skjønner ikke hva denne skal gjøre

    def consider_activation(self):
        """whenever a behavior is inactive, it should test whether it should activate."""
        #Skjønner ikke hva denne skal gjøre

    def update(self):
        if self.active:
            self.consider_deactivation()
            self.sense_and_act()
        else:
            self.consider_activation()

    def sense_and_act(self):
        faces = self.sensors[0].get_value[0]
        largest = -1
        relevant_face = -1
        for i, (_, _, w, h) in enumerate(faces):
            if w*h > largest:
                largest = w*h
                relevant_face = i
        if relevant_face == -1:
            self.match_deg = 0
            self.motor_recomendation = (1, self.ROTATION_SPEED)
            return

        face_X = faces[relevant_face][0]
        face_W = faces[relevant_face][2]
        img_middle = self.image_width/2

        if face_X + face_W * 0.6 <= img_middle:
            self.motor_recomendation = (2, self.ROTATION_SPEED)
        elif face_X + face_W * 0.4 >= img_middle:
            self.motor_recomendation = (1, self.ROTATION_SPEED)
        else:
            self.motor_recomendation = (0, self.DRIVE_SPEED)

        self.match_deg = 1
