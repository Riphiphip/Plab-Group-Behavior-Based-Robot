""" 
Main file 

Oppgave:
    Jage en farget gjenstand uten å kollidere med andre hindringer eller
    kjøre ut av banen.
    Kamera: Leter etter gitt farge
    IR: Passer på kantene
    Ultralyd: Unngår kollisjon med andre gjenstander
    Alternativt: beskytte reviret sitt fra statistikkhefter

Behaviors:
    Idle: Tilfeldig hastighet, leter etter mål
    EdgeDetection: Kant
    Stop: Knappetrykk eller mål utført
    (RemoteControl: Fjernstyring fra kommandolinje)

Sensobs:
    EdgeFinder
    ColorFinder
"""

from RPi import GPIO
from project6_zumo.bbcon import BBCON
from project6_zumo.arbitrator import Arbitrator
from project6_zumo.motob import Motob
from project6_zumo.behaviors import RemoteControl, EdgeDetection, Idle, Anti_crash, ColorChasing
from project6_supply.sensors.zumo_button import ZumoButton
from project6_supply.motors import Motors
from project6_zumo.sensobs import Collition, ColorFinder
import wiringpi as wp

import sys


def main():
    wp.wiringPiSetupGpio()
    m = Motors()
    m.forward(0.2,0.2)

    btn = ZumoButton()
    btn.wait_for_press()
    a = Arbitrator()
    controller = BBCON(a)
    print("Created controller")
    collition_detector = Collition()
    color_finder = ColorFinder()
    print("Created common sensobs")
    #controller.add_behavior(RemoteControl(10))
    controller.add_behavior(EdgeDetection(100))
    controller.add_behavior(Anti_crash(10, sensors=[collition_detector]))
    controller.add_behavior(Idle(1))
    controller.add_behavior(ColorChasing(15, sensors=[color_finder, collition_detector]))
    controller.activate_behavior(controller.behaviors[0])
    controller.activate_behavior(controller.behaviors[1])
    controller.activate_behavior(controller.behaviors[2])
    controller.activate_behavior(controller.behaviors[3])
    print("Added behaviors:")
    for c in a.behaviors:
        print(c)
    controller.motobs = [Motob(None)]
    print("Added motob")
    print("Running loop")
    while 1:
        controller.run_one_timestep()

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()