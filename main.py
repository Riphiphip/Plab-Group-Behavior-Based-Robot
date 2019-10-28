""" Main file """

from project6_zumo.bbcon import BBCON
from project6_zumo.arbitrator import Arbitrator
from project6_zumo.motob import Motob
from project6_zumo.behaviors import RemoteControl

import sys


def main():
    a = Arbitrator()
    controller = BBCON(a)
    a.add_behavior(RemoteControl(controller, 10, [sys.stdin]))
    for c in controller.behaviors:
        print(c)
    controller.motobs = [Motob(1)]
    while 1:
        controller.run_one_timestep()

main()