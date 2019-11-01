from time import sleep

from project6_zumo.sensobs import ColorFinder
from project6_supply.sensors.camera import Camera
from project6_zumo.behaviors import ColorChasing

def main(c: ColorFinder, cam: Camera, b: ColorChasing):
    cam.update()
    c.update()
    b.update()
    print(c.get_value(), " --> ", b.motor_recommendation, b.get_weight())

if __name__ == "__main__":
    cam = Camera()
    c = ColorFinder(sensors=[cam])
    b = ColorChasing(10, sensors=[c])
    try:
        while True:
            main(c, cam, b)
            sleep(0.5)
    except KeyboardInterrupt:
        pass
