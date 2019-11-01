# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:05:15 2019
"""
import sys
import random

from abc import ABC, abstractmethod
from project6_zumo.sensobs import EdgeFinder, ColorFinder, Collition


class Behavior(ABC):
    """The core of BBR are the behaviors themselves, each a modular unit
    designed to analyze a subset of the sensory information as the basis for
    determining a motor request. Behaviors operate in a vacuum in the sense
    that they have no knowledge of or direct connection to other behaviors.
    It violates the fundamental principles of BBR to design behaviors that
    communicate directly with one another. All interaction occurs indirectly
    via either the arbitrator or via information posted by one behavior (in
    the bbcon) and read by a second behavior (from the bbcon).

    One important condition for receiving a passing mark on this project is
    that your group’s code obey’s this simple, yet extremely important,
    principle.
    """

    def __init__(self, priority: float, sensors=list()):
        """
        The primary instance variables for a behavior object are the following:
        1. bbcon - pointer to the controller that uses this behavior.
        2. sensobs - a list of all sensobs that this behavior uses.
        3. motor recommendations - a list of recommendations, one per motob,
        that this behavior provides to the arbitrator. In this assignment, we
        assume that ALL motobs (and there will only be one or a small few) are
        used by all behaviors.
        4. active flag - boolean variable indicating that the behavior is
        currently active or inactive.
        5. halt request - some behaviors can request the robot to completely
        halt activity (and thus
        end the run).
        6. priority - a static, pre-defined value indicating the importance of this behavior.
        7. match degree - a real number in the range [0, 1] indicating the degree to which current
        conditions warrant the performance of this behavior.
        8. weight - the product of the priority and the match degree, which the arbitrator uses as
        the basis for selecting the winning behavior for a timestep.

        As a brief review of these variables, the pointer up to the bbcon allows each behavior to
        check the bbcon for any important posts (by other behaviors) in cases where limited
        interaction between behaviors occurs. This should not be a dominant factor in your
        implementation, as a behavior should base its motor recommendations primarily on sensobs,
        but occasionally it can save a lot of work if one behavior posts information to the bbcon
        that another behavior can read. The bbcon pointer also enables easy coordination in cases
        where a behavior activates or deactives (based on sensory input) and needs to inform the
        bbcon (in order to be added or removed from bbcon.active behaviors).
        """
        self.sensors = sensors
        self.motor_recommendation = (0, 0)
        self.active = False
        self.halt_rec = False
        self.priority = priority
        self.match_deg = 0

    def get_weight(self):
        """Return weight"""
        return self.match_deg * self.priority

    def consider_deactivation(self):
        """whenever a behavior is active, it should test whether it should deactivate."""
        # Skjønner ikke hva denne skal gjøre

    def consider_activation(self):
        """whenever a behavior is inactive, it should test whether it should activate."""
        # Skjønner ikke hva denne skal gjøre

    @abstractmethod
    def update(self):
        """the main interface between the bbcon and the behavior (detailed below)"""

    @abstractmethod
    def sense_and_act(self):
        """the core computations performed by the behavior that use sensob readings
        to produce motor recommendations (and halt requests)"""


class ColorChasing(Behavior):
    """Chase a color. Stop when it's hit"""

    def __init__(self, priority, treshold=0.2, distance_treshold=2,
                 sensors=[ColorFinder(), Collition()]):
        super().__init__(priority, sensors=sensors)
        self.camera = sensors[0]
        self.collition = sensors[1]
        self.tresh = treshold
        self.dist_tresh = distance_treshold

    def consider_activation(self):
        pass

    def consider_deactivation(self):
        pass

    def sense_and_act(self):
        """ camera.get_value() returns [float, float, float] percentage of targeted color in left,
        middle and right. Chase in direction with highest value if any is above treshold.
        Stop if target is hit.
        """
        # cam = self.camera.get_value()
        # print("I am green detector, i see so much green here", cam)

        # max_index = 0
        # if self.match_deg != 0:
        #     self.match_deg = 0
        # for i in range(3):
        #     if cam[i] == max(cam):
        #         max_index = i
        #         self.match_deg = cam[i]
        #         self.motor_recommendation = (i-1, 0.2)
                
        cam = self.camera.get_value()[0]
        dist = self.collition.get_value()
        hit = max(cam) if cam[1] < 0.9 else cam[1]
        # Set match degree to hit
        if hit > 0.1:
            self.match_deg = hit
        else:
            self.match_deg = 0
        # Set direction
        direction = cam.index(hit) - 1

        if hit > self.tresh:
            # Best hit is above treshold
            self.match_deg = 1
            print("Target aquired in sector ", direction)
            print("Certainty: ", hit)

            if dist <= self.dist_tresh:
                # Target hit, stop
                print("-----------\nTarget hit!\n-----------")
                self.motor_recommendation = (0, 0)
            else:
                self.motor_recommendation = (direction, 0.5)
        else:
            # Turn on place
            self.motor_recommendation = (direction, 0.2)
        

    def update(self):
        if self.active:
            self.sense_and_act()
            self.consider_deactivation()
        else:
            self.consider_activation()


class Anti_crash(Behavior):
    """Avoid crashing into an object"""

    def __init__(self, priority, sensors=[Collition()]):
        super().__init__(priority, sensors=sensors)
        self.motor_recommendation = (0, -0.2)
        self.match_deg = 0
        self.collition = sensors[0]
    
    def update(self):
        """analyze how near an object is"""
        self.sensors[0].update()
        if self.active:
            self.sense_and_act()
            self.consider_deactivation()
        else:
            self.consider_activation()
        

    def sense_and_act(self):
        """If objects are near, back off"""
        dist = self.collition.get_value()
        if dist == None:
            dist = 1000
        if dist < 12:
            self.match_deg = 1
        else:
            self.match_deg = 0
        return self.motor_recommendation

class EdgeDetection(Behavior):
    """Edge detection, avoid falling of the table"""

    def __init__(self, priority, sensors=[EdgeFinder()]):
        super().__init__(priority, sensors=sensors)
        self.motor_recommendation = (0, -0.4)

    def update(self):
        """the main interface between the bbcon and the behavior (detailed below)"""
        """
        if self.match_deg > 0:
            self.match_deg -= 0.1
        if self.sensors[0].get_value() < 0.7:
            self.match_deg = 1
        """
        vals = self.sensors[0].get_value()

        if self.match_deg > 0:
            self.match_deg -= 1   #0.15
            if self.match_deg < 0:
                self.match_deg = 0
        if min(vals) < 0.6:
            self.match_deg = 1

    def sense_and_act(self):
        """the core computations performed by the behavior that use sensob readings
        to produce motor recommendations (and halt requests)"""
        return self.motor_recommendation

    def __str__(self):
        return "EdgeDetection Behavior"


class RemoteControl(Behavior):
    """Interface for remote control"""

    def __init__(self, priority, sensors=[sys.stdin]):
        super().__init__(priority, sensors=sensors)
        # Sensors is a UI, like iostream or arrow buttons stream

    def __str__(self):
        return "RemoteControl Behavior"

    def consider_deactivation(self):
        """whenever a behavior is active, it should test whether it should deactivate."""
        # Skjønner ikke hva denne skal gjøre

    def consider_activation(self):
        """whenever a behavior is inactive, it should test whether it should activate."""
        # Skjønner ikke hva denne skal gjøre

    def update(self):
        """the main interface between the bbcon and the behavior (detailed below)"""
        print("Reading input")
        instr = self.sensors[0].readline().split()
        self.motor_recommendation = (int(instr[0]), float(instr[1]))
        print("Direction: {} \tSpeed: {}".format(
            self.motor_recommendation[0], self.motor_recommendation[1]))
        self.match_deg = 1
        return self.motor_recommendation

    def sense_and_act(self):
        """the core computations performed by the behavior that use sensob readings
        to produce motor recommendations (and halt requests)"""
        return self.motor_recommendation


class Idle(Behavior):
    """Idle wandering"""

    def __init__(self, priority, load=5, maxmin=(10, 20), sensors=list()):
        super().__init__(priority, sensors=sensors)
        self.load = load
        self.maxmin = maxmin
        self.countdown = 0
        self.match_deg = 1

    def consider_activation(self):
        pass

    def consider_deactivation(self):
        pass

    def update(self):
        """Return a random rotation and speed"""
        if not self.countdown:
            direction = random.randint(-1, 3)
            if direction > 2: # Set preferance for turning right
                direction = 2
            self.motor_recommendation = (
                random.randint(-1, 1), random.randint(self.maxmin[0], self.maxmin[1]) / 100)
            self.countdown = self.load
        else:
            self.countdown -= 1

    def sense_and_act(self):
        """the core computations performed by the behavior that use sensob readings
        to produce motor recommendations (and halt requests)"""
        return self.motor_recommendation
    
    def __str__(self):
        return "ISitIdle Behavior"


"""
The call to update will initiate calls to these other methods, since an update will involve the
following activities:
• Update the activity status - Each behavior will have its own tests for becoming active or
inactive. Some behaviors may be active all of the time, so the tests are trivial, whereas other
behaviors may be computationally expensive to run and thus the bbcon can spare resources
if it shuts them off in cases where they are clearly not needed. For example, behaviors that
require camera images, particularly images that are preprocessed by sensobs, are expensive.
If all behaviors that use a particular camera-based sensob are inactive, then the expensive
image-processing computations can be avoided for that period of inactivity. Hence, when a
behavior becomes active or inactive, its sensobs should be informed of the status change so
that they too may activate or deactivate. Of course, for sensobs that are used by two or more
behaviors, some simple extra bookkeeping is required: if sensob S is used by both behaviors
A and B, then S can only deactivate when both A and B are inactive.
• Call sense and act
• Update the behavior’s weight - Use the match degree (calculated by sense and act) multiplied by
the behavior’s user-defined priority.

The central computation of a behavior occurs in its sense and act method. The activity in this
method will be highly specialized for each behavior but will typically involve gathering the values
of its sensobs (and possibly checking for relevant posts on the bbcon). Using that information, the
behavior will then determine motor recommendations, and possibly a halt request. It must also
set the match degree slot to a real value in the range [0, 1].
NTNU Trondheim, fall term 2019 TDT4113-PA5 V1.0, compiled: October 15, 2019
TDT4113 (PLAB2) Project 6 — Robot 2.7 Class Arbitrator 12
In some cases, a behavior may require instance variables that maintain some memory of previous
states of the sensobs. For instance, a red-object tracking behavior might record the fraction of
red in the previous camera image and then compare it to the fraction in the current image to
determine the movement of the red object relative to the agent. Similarly, a line-following
behavior may want to record a series of recent line readings to indicate whether the agent is
successfully staying on the line or gradually losing touch with it.

In general, behaviors can perform many operations, but they MUST:
• consider activation or deactivation
• produce motor recommendations
• update the match degree
and they MUST NOT communicate directly with other behaviors.
"""
