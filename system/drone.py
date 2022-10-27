from system.courier import Courier


class Drone(Courier):
    def __init__(self, position):
        super().__init__(position)
        self.battery = 100

    def move(self):
        pass
