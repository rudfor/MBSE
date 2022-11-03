import simpy
import os
from random import seed, randint
seed(23)
rel_path = os.path.dirname(__file__)
#sys.path.append(os.path.join(rel_path, "..", "..", "sim_libs"))
import simpy


def resource_drone(env, resource):
    request = resource.request()  # Generate a request event
    yield request                 # Wait for access
    yield env.timeout(1)          # Do something
    resource.release(request)     # Release the resource


def drone(res):
    print_stats(res)
    with res.request() as req:
        yield req
        print_stats(res)
    print_stats()


def print_stats(res):
    print('%d of %d slots are allocated.' % (res.count, res.capacity))
    print('  Users:', res.drone)
    print('  Queued events:', res.queue)

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

