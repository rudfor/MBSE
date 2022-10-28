from system.courier import Courier


class Bike(Courier):
    def __init__(self, position):
        super().__init__(position)
        self.cost_hour = 150 # DKK
        self.avg_speed = 3 # m/s
