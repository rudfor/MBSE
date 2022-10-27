import itertools

from system.bike import Bike
from system.drone import Drone
from system.kitchen import Kitchen
from environment.order_generator import OrderGenerator
from utility.point import Point

# Smallest time unit
time_quantum = 1
# Number of times to run the simulation (advance the time unit)
time_quantum_rounds = 1000

total_score = 0

order_generator = OrderGenerator()

kitchen = Kitchen(Point(0, 0))
num_drones = 10
num_bikes = 10
drones = [Drone(kitchen.position) for _ in range(0, num_drones)]
bikes = [Bike(kitchen.position) for _ in range(0, num_bikes)]


def calculate_score(order):
    pass


def run_simulator():
    for _ in range(0, time_quantum_rounds):
        orders = order_generator.advance(1)

        kitchen.receive_orders(orders)

        couriers = itertools.chain(drones, bikes)

        for courier in couriers:
            if kitchen.courier_present(courier):
                kitchen.pickup_order(courier)

        for courier in couriers:
            if courier.order_delivered():
                total_score += calculate_score(courier.order)

        for courier in couriers:
            courier.move()
