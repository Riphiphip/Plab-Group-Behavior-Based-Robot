# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:33:57 2019

@author: Joule
"""


class Sensob:
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
        self.sensors = sensors

    def update(self):
        raw_output = [s.get_value() for s in self.sensors]
        return self.preprocess(raw_output)

    def preprocess(self, sensor_data):
        return sensor_data
