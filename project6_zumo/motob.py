# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:59:35 2019

@author: Joule
"""

class Motob:
    """The motor object (motob) manifests an interface between a behavior and one or more motors
(a.k.a. actuators)

Motobs allow behaviors to make motor recommendations at a relatively high level, such as (L,
30) (i.e., turn 30 degrees to the left), which can then be translated into lower-level motor settings
for individual actuators, such as the wheel speeds and directions (i.e., forward or backward) of a
two-wheeled robot. 2
In this case, a single motob would be associated with two motors, one for
each wheel"""
    def __init__(self):
        """It contains (at least) the following instance variables:
            1. motors - a list of the motors whose settings will be determined by the motob.
            2. value - a holder of the most recent motor recommendation sent to the motob.
        Its primary methods are:
            1. update - receive a new motor recommendation, load it into the value slot, and operationalize
            it.
            2. operationalize - convert a motor recommendation into one or more motor settings, which
            are sent to the corresponding motor(s)."""