# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:05:15 2019

@author: Joule
"""

from project6_zumo.bbcon import BBCON
from project6_zumo.behaviors.behavior import Behavior



class FaceHunting(Behavior):

    def __init__(self, controller: BBCON, priority: float, sensors=[]):
        if sensors
        self.controller = controller
        self.sensors = sensors
        self.motor_recomendation = (0, 0)
        self.active = False
        self.halt_rec = False
        self.priotity = priority
        self.match_deg = 0

    def consider_deactivation(self):
        """whenever a behavior is active, it should test whether it should deactivate."""
        pass

    def consider_activation(self):
        """whenever a behavior is inactive, it should test whether it should activate."""
        pass

    def update(self):
        """the main interface between the bbcon and the behavior (detailed below)"""
        pass

    def sense_and_act(self):
        faces = self.sensors[0].get_value[0]
