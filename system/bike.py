from system.courier import Courier


class Bike(Courier):
    def __init__(self, position, distance_to_destination):
        super().__init__(position, distance_to_destination)
        self.cost_hour = 150 # DKK
        self.avg_speed = 3*60  # m/min # m/s
