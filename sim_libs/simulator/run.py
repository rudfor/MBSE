import simpy
import os
from random import seed, randint
seed(23)
rel_path = os.path.dirname(__file__)
#sys.path.append(os.path.join(rel_path, "..", "..", "sim_libs"))
import simpy


class Simulator:
    def __init__(self, sim):
        self.sim = sim
        print(f"started")


class DRONE:
    def __init__(self, drone):
        self.env = env
        self.graph = sim_libs.map.OsmnxApi()

class RUN:
    def __init__(self):
        print(f"started")

