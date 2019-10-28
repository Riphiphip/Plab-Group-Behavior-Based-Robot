""" Main file """

from project6_zumo.bbcon import BBCON
from project6_zumo.arbitrator import Arbitrator
from project6_zumo.motob import Motob
from project6_zumo.behaviors import RemoteControl

import sys


def main():
    a = Arbitrator()
    controller = BBCON(a)
    print("Created controller")
    controller.add_behavior(RemoteControl(controller, 10, [sys.stdin]))
    print("Added behaviors:")
    for c in a.behaviors:
        print(c)
    controller.motobs = [Motob(1)]
    print("Added motob")
    print("Running loop")
    while 1:
        controller.run_one_timestep()

main()