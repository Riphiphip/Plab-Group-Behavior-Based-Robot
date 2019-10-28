"""Edge detection, avoid falling of the table"""

from project6_zumo.behaviors.behavior import Behavior


class EdgeDetection(Behavior):
    """Edge detection, avoid falling of the table"""

    def __init__(self, controller, priority, sensors=list()):
        super().__init__(controller, priority, sensors=sensors)
        