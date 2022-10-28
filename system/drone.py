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