# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:28:46 2019

@author: Joule
"""
import random


class Arbitrator:
    """The arbitrator is a fairly simple class that makes a very important decision at each timestep: which
behavior wins and thus gets its motor recommendations transferred to the agent’s motobs, which
will then determine the overt action(s) of the agent.
The arbitrator may include an instance variable housing a pointer to the bbcon, such that the
arbitrator can easily fetch all of the bbcon’s active behaviors. The primary method of the arbitrator
is choose action, which should check all of the active behaviors and pick a winner.
This choice can either be very simple: pick the behavior with the highest weight; or it can include
an element of stochasticity. In this latter case, the arbitrator makes a random, but biased, choice
among the behaviors, with bias stemming from the behavior weights. For example, assume that
there are 3 active behaviors with weights in parentheses: B1(0.8), B4 (0.5), and B6 (0.7). To make
a stochastic choice among these behaviors, use the weights to generate a range for each behavior:
B1: [0, 0.8)
B4: [0.8, 1.3)
B6: [1.3, 2.0)
Next, generate a random real number, R, between 0 and 2.0 (= 0.8 + 0.7 + 0.5). Whichever of
the 3 ranges that R falls within, the corresponding behavior wins. Clearly, behaviors with higher
weights have a larger chance (but are not guaranteed) of winning.
You are free to choose a deterministic or a stochastic solution, or to implement both and let the
user decide by setting the value of a simple instance variable (e.g., named stochastic) in the arbitrator. Experience shows that many robotics problems are more easily solved with some element
of stochasticity. 4
"""

    def __init__(self):
        self.behaviors = []

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def remove_behavior(self, behavior):
        self.behaviors.remove(behavior)

    def choose_action(self):
        """Regardless of the selection strategy, choose action should return a tuple containing:
1. motor recommendations (one per motob) to move the robot, and
2. a boolean indicating whether or not the run should be halted.
In the cases of the simple deterministic and the stochastic arbitration strategies, both of these
values should come directly from the winning behavior."""
        cummulative_weight_list = [0]
        for behavior in self.behaviors:
            cummulative_weight_list.append(
                cummulative_weight_list[-1] + behavior.get_weight())
        choice = random.randint(0, cummulative_weight_list[-1])
        i = 0
        while cummulative_weight_list[i] < choice:
            i += 1
        # i-1 since the first entry in cummulative_weight_list is 0, and the 0th behavior's weight is in the 1st position
        return (self.behaviors[i-1].motor_recommendation, self.behaviors[i-1].halt_rec)
