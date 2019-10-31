# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:59:35 2019

@author: Joule
"""

from project6_supply.motors import Motors
#class Motors():
#    """dummy"""
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#    
#    def set_value(self, rec, dur=1):
#        print(rec)

class Motob:
    """The motor object (motob) manifests an interface between a behavior and one or more motors
    (a.k.a. actuators)

    Motobs allow behaviors to make motor recommendations at a relatively high level, such as (L,
    30) (i.e., turn 30 degrees to the left), which can then be translated into lower-level motor
    settings for individual actuators, such as the wheel speeds and directions (i.e., forward or
    backward) of a two-wheeled robot. 2
    In this case, a single motob would be associated with two motors, one for
    each wheel
    """

    def __init__(self, timestep, motors=Motors(), turn_speed=0.1):
        """It contains (at least) the following instance variables:
            1. motors - a list of the motors whose settings will be determined by the motob.
            Nope
            2. value - a holder of the most recent motor recommendation sent to the motob.
        Its primary methods are:
            1. update - receive a new motor recommendation, load it into the value slot, and
            operationalize it.
            2. operationalize - convert a motor recommendation into one or more motor settings,
            which are sent to the corresponding motor(s)."""
        self.duration = timestep
        self.turn_speed = turn_speed
        self.motors = motors
        self.value = None

    def update(self, motor_recommendation: (int, float)):
        """Set motors to recommended settings"""
        print("I am motob, i will update with recomendations", motor_recommendation)
        self.value = motor_recommendation
        self.operationalize(motor_recommendation)

    def operationalize(self, motor_recommendation: (int, float)):
        """Convert a motor recommendation into one or more motor settings,
            which are sent to the corresponding motor(s)."""
        settings, duration = self.convert_recommendation_to_motor_settings(
            motor_recommendation)
        self.motors.set_value(settings, dur=duration)

    def convert_recommendation_to_motor_settings(self, motor_recommendation: (int, float)):
        """
        Convert MR to MS.
        motor_recommendation:
         - [0]: int in [-1,1]; left
         - [1]: float speed, negative for bakwards
        """
        direction = motor_recommendation[0]
        speed = motor_recommendation[1]

        if direction == 0:
            return (speed, speed), self.duration
        elif direction == 1:
            return (speed + self.turn_speed, speed - self.turn_speed), self.duration
        elif direction == -1:
            return (speed - self.turn_speed, speed + self.turn_speed), self.duration
