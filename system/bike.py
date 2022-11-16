from system.courier import Courier, CourierState
from utility.argparser import args


class Bike(Courier):
    def __init__(self, position):
        super().__init__(position, 0)
        self.cost_hour = args.BIKE_HOUR_COST  # DKK
        self.avg_speed = args.BIKE_AVG_SPEED  # m/min # m/s

    def courier_type(self):
        return "Bike"

    def status(self):
        if self.is_standby():
            return f"{self.courier_type()} {self.id} standby at kitchen"
        state_str = "delivering order" if self.state == CourierState.DeliveringOrder else "returning to kitchen"
        status_str = f"{self.courier_type()} {self.id} {state_str} with {self.distance_to_destination:.2f} m " \
                     f"/ {self.time_to_destination():.2f} min left"
        return status_str
