from time import sleep

from project6_zumo.sensobs import ColorFinder
from project6_supply.sensors.camera import Camera

def main(c: ColorFinder, cam: Camera):
    cam.update()
    c.update()
    print(c.get_value())

if __name__ == "__main__":
    cam = Camera()
    c = ColorFinder(sensors=[c])
    try:
        while True:
            main(c)
            sleep(0.5)
    except KeyboardInterrupt:
        pass
