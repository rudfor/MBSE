from system.courier import Courier
from utility.argparser import args


class Bike(Courier):
    def __init__(self, position):
        super().__init__(position, 0)
        self.cost_hour = args.BIKE_HOUR_COST # DKK
        self.avg_speed = args.BIKE_AVG_SPEED  # m/min # m/s

    def courier_type(self):
        return "Bike"