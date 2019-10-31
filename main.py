""" 
Main file 

Oppgave:
    Jage en farget gjenstand uten å kollidere med andre hindringer eller
    kjøre ut av banen.
    Kamera: Leter etter gitt farge
    IR: Passer på kantene
    Ultralyd: Unngår kollisjon med andre gjenstander, gjenkjenner kollisjon
    med målet

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
from project6_zumo.behaviors import RemoteControl, EdgeDetection, Idle, ColorChasing
from project6_supply.sensors.zumo_button import ZumoButton
from project6_supply.sensors.motors import Motor
import wiringpi as wp

import sys


def main():
    wp.wiringPiSetupGpio()
    m = Motor()
    m.forward(0.2,0.2)

    btn = ZumoButton()
    btn.wait_for_press()
    a = Arbitrator()
    controller = BBCON(a)
    print("Created controller")
    #controller.add_behavior(RemoteControl(10))
    controller.add_behavior(EdgeDetection(100))
    controller.add_behavior(ColorChasing(50))
    controller.add_behavior(Idle(1))
    controller.activate_behavior(controller.behaviors[0])
    controller.activate_behavior(controller.behaviors[1])
    controller.activate_behavior(controller.behaviors[2])
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