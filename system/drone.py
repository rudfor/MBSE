from abc import abstractmethod
from system.courier import Courier, CourierState
from utility.argparser import args


class Drone(Courier):
    def __init__(self, position):
        super().__init__(position, 0)
        self.cost = None  # DKK
        self.battery_capacity = None
        self.battery = None  # min
        self.charge_time = None  # 60 - 90 min
        self.avg_speed = None  # m/min  # m/s
        self.cargo_weight = None  # kg
        self.range = None
        self.speed = None

    def set_speed(self, weather_factor, traffic_factor):
        self.speed = self.avg_speed

    def move(self, delta_time_minutes, traffic_factor, weather_factor):
        if not self.is_standby():
            self.distance_to_destination -= delta_time_minutes * self.speed
            if self.state == CourierState.DeliveringOrder:
                self.battery -= (delta_time_minutes * (1 + (self.order.weight / 2))) / weather_factor
            else:
                self.battery -= delta_time_minutes / weather_factor
            if self.has_arrived():
                self.update_arrival()

    def take_order(self, order):
        #print(self.is_standby())
        # Drone can take order if it has sufficient battery for the round trip
        if not self.is_standby():
            return False
        #print(2 * order.distance / self.speed)
        if self.battery >= 2 * order.distance / self.speed:
            self.order = order
            self.distance_to_destination = self.order.distance
            self.state = CourierState.DeliveringOrder
            return True
        else:
            return False

    def time_to_destination(self):
        return self.distance_to_destination / self.speed

    def within_range(self, order):
        return order.distance <= self.range

    @abstractmethod
    def courier_type(self):
        pass

    def charge(self, dt):
        self.battery = min(self.battery_capacity, self.battery + dt * self.battery_capacity / self.charge_time)

    def status(self):
        if self.is_standby():
            return f"{self.courier_type()} {self.id} standby at kitchen. Remaining battery: {self.battery:.2f} min"
        state_str = f"delivering order {self.order.id}" if self.state == CourierState.DeliveringOrder else "returning to kitchen"
        status_str = f"{self.courier_type()} {self.id} {state_str} with {self.distance_to_destination:.2f} m " \
                     f"/ {self.time_to_destination():.2f} min left. Remaining battery: {self.battery:.2f} min"
        return status_str


class DefaultDrone(Drone):
    cost = args.DRONE_COST  # DKK

    def __init__(self, position):
        super().__init__(position)
        self.battery_capacity = args.DRONE_BAT_CAP
        self.battery = args.DRONE_FLIGHT_TIME  # min
        self.range = args.DRONE_RANGE  # m
        self.charge_time = args.DRONE_CHARGE_TIME  # 60 - 90 min
        self.avg_speed = args.DRONE_AVG_SPEED  # m/s
        self.cargo_weight = args.DRONE_WEIGHT_LIMIT  # kg
        self.speed = self.avg_speed

    def courier_type(self):
        return "DefaultDrone"


class DroneType1(Drone):
    # https://uavsystemsinternational.com/products/tarot-t-18-ready-fly-drone/
    cost = 38062  # DKK

    def __init__(self, position):
        super().__init__(position)
        self.battery_capacity = 25
        self.battery = 25  # min
        self.range = 3200  # m
        self.charge_time = 60  # 60 - 90 min
        self.avg_speed = 15 * 60  # m/min  # m/s
        self.cargo_weight = 8  # kg

    def courier_type(self):
        return "DroneType1"


class DroneType2(Drone):
    # https://uavsystemsinternational.com/products/aurelia-x6-max-ready-to-fly
    cost = 60249  # DKK

    def __init__(self, position):
        super().__init__(position)
        self.battery_capacity = 70
        self.battery = 70  # min
        self.range = 5000  # m
        self.charge_time = 90  # 60 - 90 min
        self.avg_speed = 15 * 60  # m/min  # m/s
        self.cargo_weight = 6  # kg

    def courier_type(self):
        return "DroneType2"


class DroneType3(Drone):
    # https://uavsystemsinternational.com/products/aurelia-x8-max-ready-to-fly
    cost = 75502  # DKK

    def __init__(self, position):
        super().__init__(position)
        self.battery_capacity = 70
        self.battery = 70  # min
        self.range = 15000  # m
        self.charge_time = 90  # 60 - 90 min
        self.avg_speed = 15 * 60  # m/min  # m/s # Can fly maximumm 56 km/h
        self.cargo_weight = 11  # kg

    def courier_type(self):
        return "DroneType3"
