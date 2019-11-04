# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:25:08 2019

@author: Joule

The highest-level class, BBCON (Behavior-Based Controller) should only require one instance (per
robot). At each timestep, the robot should call its bbcon to determine its next move. A bbcon
should contain (at least) the following instance variables:
"""
from time import sleep
#from project6_zumo.behaviors import Behavior
from project6_zumo.arbitrator import Arbitrator
from project6_zumo.motob import Motob
from project6_zumo.sensobs import Sensob
from project6_zumo.behaviors import Behavior

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
        self.active_behaviors = []
        self.sensobs = dict()
        self.sensors = dict()
        self.motobs = []
        self.arbitrator = arbitrator
        

    def add_behavior(self, behavior):
        """ append a newly-created behavior onto the behaviors list"""
        self.behaviors.append(behavior)

    def add_sensors(self, sensob: Sensob):
        """Tracks what sensors are in use"""
        for sensor in sensob.sensors:
            if not(sensor in self.sensors):
                self.sensors[sensor] = set()
            self.sensors.get(sensor).add(sensob)
    
    def add_sensobs(self, behavior: Behavior):
        """Tracks what sensobs are in use"""
        for sensob in behavior.sensors:
            if not(sensob in self.sensobs):
                self.sensobs[sensob] = set()
            self.sensobs[sensob].add(behavior)
            self.add_sensors(sensob)
    
    def remove_sensors(self, sensob: Sensob):
        if sensob in self.sensobs:
            for sensor in sensob.sensors:
                if sensor in self.sensors:
                    self.sensors[sensor].remove(sensob)
                if len(self.sensors[sensor]) <= 0:
                    del self.sensors[sensor]

    def remove_sensobs(self, behavior: Behavior):
        if behavior in self.active_behaviors:
            for sensob in behavior.sensors:
                if sensob in self.sensobs:
                    self.sensobs[sensob].remove(behavior)
                    self.remove_sensors(sensob)
                if len(self.sensobs[sensob]) <= 0:
                    del self.sensobs[sensob]

    def activate_behavior(self, behavior: Behavior):
        """add an existing behavior onto the active-behaviors list"""
        if behavior in self.behaviors:
            self.active_behaviors.append(behavior)
            self.arbitrator.add_behavior(behavior)
            self.add_sensobs(behavior)
            behavior.active = True
        else:
            raise ValueError("Behavior does not exist")

    def deactive_behavior(self, behavior: Behavior):
        """remove an existing behavior from the active behaviors list"""
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)
            self.arbitrator.remove_behavior(behavior)
            self.remove_sensobs(behavior)
            behavior.active = False
        else:
            raise ValueError("Behavior does not exist")

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
        
        for sensor in self.sensors:
            sensor.update()
        for sensob in self.sensobs:
            sensob.update()
        for behavior in self.behaviors:
            behavior.update()
            if behavior.active:
                if behavior.consider_deactivation():
                    self.deactive_behavior(behavior)
            elif behavior.consider_activation():
               self.activate_behavior(behavior) 
                
        motor_recommendations, is_halting = self.arbitrator.choose_action()
        if not is_halting:
            for motob in self.motobs:
                motob.update(motor_recommendations)
                sleep(0.05)
        # .reset() should be implemented or not used at all
        #for sensob in self.sensobs:
        #    sensob.reset()