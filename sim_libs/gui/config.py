import random
"""
@author: Rudolf Anton Fortes
"""
# -------------------------
#  CONFIGURATION
# -------------------------

class Config:
    def __init__(self, seed=42):
        self.random_seed=(seed)
        self.BUS_ARRIVAL_MEAN = 3
        self.BUS_OCCUPANCY_MEAN = 100
        self.BUS_OCCUPANCY_STD = 30

        self.ORDER_ARRIVAL_MEAN=1
        self.ORDER_SIZE_MEAN=7
        self.ORDER_SIZE_STD=2

        self.PURCHASE_RATIO_MEAN = 0.4
        self.PURCHASE_GROUP_SIZE_MEAN = 2.25
        self.PURCHASE_GROUP_SIZE_STD = 0.50

        self.TIME_TO_WALK_TO_SELLERS_MEAN = 1
        self.TIME_TO_WALK_TO_SELLERS_STD = 0.25
        self.TIME_TO_WALK_TO_SCANNERS_MEAN = 0.5
        self.TIME_TO_WALK_TO_SCANNERS_STD = 0.1

        self.SELLER_LINES = 10
        self.SELLERS_PER_LINE = 1
        self.SELLER_MEAN = 1
        self.SELLER_STD = 0.2

        self.SCANNER_LINES = 4
        self.SCANNERS_PER_LINE = 1
        self.SCANNER_MEAN = 1 / 20
        self.SCANNER_STD = 0.01

        self.ARRIVALS = [random.expovariate(1 / self.BUS_ARRIVAL_MEAN) for _ in range(40)]
        self.ON_BOARD = [int(random.gauss(self.BUS_OCCUPANCY_MEAN, self.BUS_OCCUPANCY_STD)) for _ in range(40)]

        self.ORDERS = [random.expovariate(1 / self.ORDER_ARRIVAL_MEAN) for _ in range(300)]
        self.ORDER_SIZE = [int(random.gauss(self.ORDER_SIZE_MEAN, self.ORDER_SIZE_STD)) for _ in range(300)]


