from system.courier import Courier


class Bike(Courier):
    def __init__(self, position):
        super().__init__(position, 0)
        self.cost_hour = 150 # DKK
        self.avg_speed = 3*60  # m/min # m/s
