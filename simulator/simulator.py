import itertools

from environment.order import Order
from experiment.test3 import Map
from system.bike import Bike
from system.drone import Drone_type1
from system.kitchen import Kitchen
from environment.order_generator import OrderGenerator
from utility.point import Point

# total_score = 0

# order_generator = OrderGenerator()

# kitchen = Kitchen(Point(0, 0))
#num_drones = 10
# drones = [Drone_type1(kitchen.position) for _ in range(0, num_drones)]
# bikes = [Bike(kitchen.position) for _ in range(0, num_bikes)]


TIME_LIMIT_MINUTES = 60
ORDER_INTERVAL_MINUTES = 10

MAP = Map()

# 5 km/h
AVG_BIKE_SPEED_METERS_PER_HOUR = 5000

num_bikes = 1
bikes = [Bike(Point(45501638, 45521416)) for _ in range(0, num_bikes)]

# def calculate_score(order):
#     pass


def run_simulator():
    current_time_minutes = 0

    while current_time_minutes <= TIME_LIMIT_MINUTES:
        current_time_minutes += ORDER_INTERVAL_MINUTES

        if current_time_minutes % ORDER_INTERVAL_MINUTES == 0:
            # Generate random order destination
            order_start, order_end = MAP.next_destination()
            distance = MAP.path_length(order_start, order_end)
            print(f"order at time {current_time_minutes}: ({order_start}, {order_end}), distance: {distance}")

            # Create bike courier
            for bike in bikes:
                if not bike.is_delivering():
                    bike.order = Order(order_start, order_end, None)

            # Move bike couriers
            for bike in bikes:
                bike.move(ORDER_INTERVAL_MINUTES)


            # map.plot_path(order_start, order_end)
        ######
        # orders = order_generator.advance(1)
        #
        # kitchen.receive_orders(orders)
        #
        # couriers = itertools.chain(drones, bikes)
        #
        # for courier in couriers:
        #     if kitchen.courier_present(courier):
        #         kitchen.pickup_order(courier)
        #
        # for courier in couriers:
        #     if courier.order_delivered():
        #         total_score += calculate_score(courier.order)
        #
        # for courier in couriers:
        #     courier.move()
