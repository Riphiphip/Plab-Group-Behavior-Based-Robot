# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:25:08 2019

@author: Joule
"""

"""The highest-level class, BBCON (Behavior-Based Controller) should only require one instance (per
robot). At each timestep, the robot should call its bbcon to determine its next move. A bbcon
should contain (at least) the following instance variables:"""

class BBCON:
    """The highest-level class, BBCON (Behavior-Based Controller) should only require one instance (per
robot). At each timestep, the robot should call its bbcon to determine its next move. A bbcon
should contain (at least) the following instance variables:"""

    def __init__(self, arbitrator):
        """behaviors - a list of all the behavior objects used by the bbcon
        2. active-behaviors - a list of all behaviors that are currently active.
        3. sensobs - a list of all sensory objects used by the bbcon
        4. motobs - a list of all motor objects used by the bbcon
        5. arbitrator - the arbitrator object that will resolve actuator requests produced by the behaviors."""
        self.behaviors = []
        self.active-behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = arbitrator
        

    def add_behavior(self, behavior):
        """ append a newly-created behavior onto the behaviors list"""
        pass

    def add_sensob(self, sensor):
        """- append a newly-created sensob onto the sensobs list"""
        pass

    def activate_behavior(self, behavior):
        """add an existing behavior onto the active-behaviors list"""
        pass

    def deactive_behavior(self, behavior):
        """remove an existing behavior from the active behaviors list"""
        pass

    def  run_one_timestep(self):
        """In addition, BBCON must include a method named run one timestep, which constitutes the core
        BBCON activity. It should perform (at least) the following actions on each call:
            """
        """1. Update all sensobs - These updates will involve querying the relevant sensors for their values, along with any pre-processing of those values (as described below)
        2. Update all behaviors - These updates involve reading relevant sensob values and producing
        a motor recommendation.
        3. Invoke the arbitrator by calling arbitrator.choose action, which will choose a winning behavior and return that behavior’s motor recommendations and halt request flag.
        4. Update the motobs based on these motor recommendations. The motobs will then update
        the settings of all motors.
        5. Wait - This pause (in code execution) will allow the motor settings to remain active for a short
        period of time, e.g., one half second, thus producing activity in the robot, such as moving
        forward or turning.
        6. Reset the sensobs - Each sensob may need to reset itself, or its associated sensor(s), in some
        way."""
        pass