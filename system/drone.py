from turtle import position
from system.courier import Courier


class Drone_type1(Courier):
# https://uavsystemsinternational.com/products/tarot-t-18-ready-fly-drone/
    
    def __init__(self, position):
        super().__init__(position)
        self.cost = 38062 # DKK
        self.battery = 25 # min
        # self.range = 3200 # m
        self.charge_time = 60 # 60 - 90 min
        self.avg_speed = 15 # m/s
        self.cargo_weight = 8 # kg

class Drone_type1(Courier):
# https://uavsystemsinternational.com/products/aurelia-x6-max-ready-to-fly
    
    def __init__(self, position):
        super().__init__(position)
        self.cost = 60.249 # DKK
        self.battery = 70 # min
        # self.range = 5000 # m
        self.charge_time = 90 # 60 - 90 min
        self.avg_speed = 15.5 # m/s
        self.cargo_weight = 6 # kg

class Drone_type1(Courier):
# https://uavsystemsinternational.com/products/aurelia-x8-max-ready-to-fly

    def __init__(self, position):
        super().__init__(position)
        self.cost = 75.502 # DKK
        self.battery = 70 # min
        # self.range = 15000 # m
        self.charge_time = 90 # 60 - 90 min
        self.avg_speed = 15 # m/s
        self.cargo_weight = 11 # kg