from experiment.test3 import Map
from simulator.config import KITCHEN_NODE
from simulator.event import EventType, Event
from system.bike import Bike
from system.courier import CourierState
from environment.order_generator import OrderGenerator
from system.drone import DroneType1
from utility.point import Point

# Simulation configuration
TIME_LIMIT_MINUTES = 90

# Environment
MAP = Map()
ORDER_GENERATOR = OrderGenerator(MAP)

# System
kitchen_node = KITCHEN_NODE
kitchen_position = Point(45501638, 45521416)
num_bikes = 3
num_drones = 3
bikes = [Bike(kitchen_position) for _ in range(0, num_bikes)]
#drones = [DroneType1(kitchen_position) for _ in range(0, num_bikes)]
# couriers = bikes.extend(drones)


def run_simulator():
    current_time_minutes = 0
    # Let's always start with an order, for testing purposes
    next_order = Event(EventType.Order, 0, None)
    orders = []

    print_simulation_configuration()

    # Main loop. Simulate a specified number of minutes.
    while current_time_minutes <= TIME_LIMIT_MINUTES:
        # Get next event
        next_event = get_next_event(next_order)

        # Increment and print current time
        current_time_minutes += next_event.event_time
        print(f"Time: {current_time_minutes:.2f} minutes")

        # Move all couriers (bikes)
        for bike in bikes:
            bike.move(next_event.event_time)

        # Perform operations depending on event type
        match next_event.event_type:
            case EventType.Order:
                # Generate order with random destination and append it to the orders queue
                order = ORDER_GENERATOR.generate_order(current_time_minutes)
                orders.append(order)
                print(f"EVENT: Incoming order {order}")

                next_order = Event(EventType.Order, ORDER_GENERATOR.generate_time_until_order(), None)

            case EventType.Bike:
                event_bike = next_event.event_obj
                bike_event_str = "arrived at order destination" if next_event.event_obj.state == CourierState.ReturningToKitchen else "returned to kitchen"
                print(f"EVENT: Bike {event_bike.id} {bike_event_str}")
                if event_bike.state == CourierState.ReturningToKitchen:
                    MAP.plot_path(kitchen_node, event_bike.order.destination.y, 'r')
                elif event_bike.state == CourierState.DeliveringOrder:
                    MAP.plot_path(kitchen_node, event_bike.order.destination.y, 'b')

        accept_orders(orders)

        #

        print_state()


def get_next_event(next_order):
    # Find time until next bike event (when bike arrives at order destination or back to kitchen)
    bike_event = next_bike_event()

    # Reduce time to next event to time of order, if order happens before any bike event

    # If no bike events or order happens before bike event
    if bike_event is None or next_order.event_time < bike_event.event_time:
        return next_order

    # If order happens after (there must be a bike event at this point, otherwise we would have returned an order event)
    next_order.event_time -= bike_event.event_time
    return bike_event


def accept_orders(orders):
    # Assign orders to standby couriers (bikes), if any
    # TODO: when drones, select drone based on order distance and drone battery life
    for bike in bikes:
        if orders and bike.is_standby():
            order = orders[0]
            bike.take_order(orders[0])
            del orders[0]
            print(f"ACTION: Bike {bike.id} accepted order {order}")
            break

    if orders:
        print(f"ACTION: No bikes to take the following {len(orders)} order(s):")
        for order in orders:
            print(order)


def print_simulation_configuration():
    print("Simulation configuration:")
    print(f"TIME_LIMIT_MINUTES: {TIME_LIMIT_MINUTES}")
    print(f"Kitchen at position {kitchen_position}")
    print(f"{num_bikes} bikes available")
    print("-----------------------------------------------------------------------------------------------------------")


def adjust_event_for_order(time_until_next_event_minutes, time_until_next_order_minutes):
    order_is_next_event = False
    if time_until_next_event_minutes is None or time_until_next_order_minutes < time_until_next_event_minutes:
        time_until_next_event_minutes = time_until_next_order_minutes
        order_is_next_event = True
    elif time_until_next_event_minutes is not None:
        time_until_next_order_minutes -= time_until_next_event_minutes
    return order_is_next_event, time_until_next_event_minutes


def next_bike_event():
    time_until_next_event_minutes = None
    bike_event = None
    for bike in bikes:
        if not bike.is_standby():
            if time_until_next_event_minutes is None or bike.time_to_destination() < time_until_next_event_minutes:
                time_until_next_event_minutes = bike.time_to_destination()
                bike_event = Event(EventType.Bike, time_until_next_event_minutes, bike)
    return bike_event


def print_state():
    print("STATUS:")
    for bike in bikes:
        if bike.is_standby():
            print(f"Bike {bike.id} standby at kitchen")
        else:
            state_str = "delivering order" if bike.state == CourierState.DeliveringOrder else "returning to kitchen"

            print(
                f"Bike {bike.id} {state_str} with {bike.distance_to_destination:.2f} meters / {bike.time_to_destination():.2f} minutes left")

    print("-----------------------------------------------------------------------------------------------------------")
