from abc import abstractmethod

from system.courier import Courier, CourierState


class Drone(Courier):
    def __init__(self, position):
        super().__init__(position, 0)
        self.cost = None  # DKK
        self.battery_capacity = None
        self.battery = None  # min
        self.charge_time = None  # 60 - 90 min
        self.avg_speed = None  # m/min  # m/s
        self.cargo_weight = None  # kg

    def move(self, delta_time_minutes):
        if not self.is_standby():
            self.distance_to_destination -= delta_time_minutes * self.avg_speed
            self.battery -= delta_time_minutes
            if self.has_arrived():
                self.update_arrival()

    def take_order(self, order):
        if self.battery >= order.distance / self.avg_speed:
            self.order = order
            self.distance_to_destination = self.order.distance
            self.state = CourierState.DeliveringOrder
            return True
        else:
            return False

    @abstractmethod
    def courier_type(self):
        pass

    def charge(self, dt):
        self.battery = min(self.battery_capacity, self.battery + dt * self.battery_capacity / self.charge_time)


class DroneType1(Drone):
    # https://uavsystemsinternational.com/products/tarot-t-18-ready-fly-drone/

    def __init__(self, position):
        super().__init__(position)
        self.cost = 38062  # DKK
        self.battery_capacity = 25
        self.battery = 25  # min
        # self.range = 3200 # m
        self.charge_time = 60  # 60 - 90 min
        self.avg_speed = 15 / 2 * 60 # m/min  # m/s
        self.cargo_weight = 8  # kg

    def courier_type(self):
        return "DroneType1"


class DroneType2(Drone):
    # https://uavsystemsinternational.com/products/aurelia-x6-max-ready-to-fly

    def __init__(self, position):
        super().__init__(position)
        self.cost = 60.249  # DKK
        self.battery_capacity = 70
        self.battery = 70  # min
        # self.range = 5000 # m
        self.charge_time = 90  # 60 - 90 min
        self.avg_speed = 15.5 / 2 * 60  # m/min  # m/s
        self.cargo_weight = 6  # kg

    def courier_type(self):
        return "DroneType2"


class DroneType3(Drone):
    # https://uavsystemsinternational.com/products/aurelia-x8-max-ready-to-fly

    def __init__(self, position):
        super().__init__(position)
        self.cost = 75.502  # DKK
        self.battery_capacity = 70
        self.battery = 70  # min
        # self.range = 15000 # m
        self.charge_time = 90  # 60 - 90 min
        self.avg_speed = 15 / 2 * 60  # m/min  # m/s
        self.cargo_weight = 11  # kg

    def courier_type(self):
        return "DroneType3"
