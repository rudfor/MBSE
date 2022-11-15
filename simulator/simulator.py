from simulator.map import Map
from simulator.config import KITCHEN_NODE_ID
from simulator.event import EventType, Event
from simulator.stats import Stats
from simulator.system import System
from system.courier import CourierState
from environment.order_generator import OrderGenerator
from utility.point import Point
from utility.argparser import args
from display.df_cost_time import *

# Simulation configuration
TIME_LIMIT_MINUTES = 300

# Environment
MAP = Map()
ORDER_GENERATOR = OrderGenerator(MAP)

# System
KITCHEN_NODE = MAP.get_node(KITCHEN_NODE_ID)
KITCHEN_POSITION = Point(KITCHEN_NODE['x'], KITCHEN_NODE['y'])
SYSTEM = System(KITCHEN_POSITION)

# Statistics tracking
STATS = Stats()


def run_simulator():
    current_time_minutes = 0
    # Let's always start with an order, for testing purposes
    next_order = Event(EventType.Order, 0, None)
    orders = []

    print_simulation_configuration(SYSTEM)

    # Main loop. Simulate a specified number of minutes.
    while current_time_minutes <= TIME_LIMIT_MINUTES:
        # Get next event
        next_event = get_next_event(SYSTEM, next_order)

        # Increment and print current time
        current_time_minutes += next_event.event_time
        print(f"Time: {current_time_minutes:.2f} minutes")

        # Charge drones
        for drone in SYSTEM.drones():
            if drone.is_standby():
                drone.charge(next_event.event_time)

        # Move all couriers
        for courier in SYSTEM.couriers:
            courier.move(next_event.event_time)

        # Perform operations depending on event type
        match next_event.event_type:
            case EventType.Order:
                # Generate order with random destination and append it to the orders queue
                order = ORDER_GENERATOR.generate_order(current_time_minutes)
                orders.append(order)
                print(f"EVENT: Incoming order {order}")

                next_order = Event(EventType.Order, ORDER_GENERATOR.generate_time_until_order(), None)

            case EventType.Bike | EventType.Drone:
                event_courier = next_event.event_obj
                bike_event_str = "arrived at order destination" if next_event.event_obj.state == CourierState.ReturningToKitchen else "returned to kitchen"
                print(f"EVENT: {event_courier.courier_type()} {event_courier.id} {bike_event_str}")

                # Order delivered, update stats
                if event_courier.state == CourierState.ReturningToKitchen:
                    STATS.update_avg_order_time(current_time_minutes, event_courier)
                    if next_event.event_type == EventType.Bike:
                        STATS.update_bike_stats(current_time_minutes, event_courier)
                    elif next_event.event_type == EventType.Drone:
                        STATS.update_drone_stats(current_time_minutes, event_courier)

        SYSTEM.accept_orders(orders)

        print_state(SYSTEM)

        if args.PLOT:
            MAP.plot_courier_paths(SYSTEM.couriers)

    if args.PLOT:
        STATS.plot_results()


def get_next_event(system, next_order):
    # Find time until next bike event (when bike arrives at order destination or back to kitchen)
    courier_event = system.next_courier_event()

    # Reduce time to next event to time of order, if order happens before any bike event

    # If no bike events or order happens before bike event
    if courier_event is None or next_order.event_time < courier_event.event_time:
        return next_order

    # If order happens after (there must be a bike event at this point, otherwise we would have returned an order event)
    next_order.event_time -= courier_event.event_time
    return courier_event


def adjust_event_for_order(time_until_next_event_minutes, time_until_next_order_minutes):
    order_is_next_event = False
    if time_until_next_event_minutes is None or time_until_next_order_minutes < time_until_next_event_minutes:
        time_until_next_event_minutes = time_until_next_order_minutes
        order_is_next_event = True
    elif time_until_next_event_minutes is not None:
        time_until_next_order_minutes -= time_until_next_event_minutes
    return order_is_next_event, time_until_next_event_minutes


def print_simulation_configuration(system):
    print("Simulation configuration:")
    print(f"TIME_LIMIT_MINUTES: {TIME_LIMIT_MINUTES}")
    print(f"Kitchen at position ({KITCHEN_NODE['x']}, {KITCHEN_NODE['y']})")
    print(f"{system.num_bikes} bikes available")
    print(f"{system.num_drones()} drones available")
    print("-----------------------------------------------------------------------------------------------------------")


def print_state(system):
    print("STATUS:")
    for courier in system.couriers:
        if courier.is_standby():
            if not isinstance(courier, Bike):
                print(
                    f"{courier.courier_type()} {courier.id} standby at kitchen. Battery time left: {courier.battery:.2f} minutes")
            else:
                print(
                    f"{courier.courier_type()} {courier.id} standby at kitchen")
        else:
            state_str = "delivering order" if courier.state == CourierState.DeliveringOrder else "returning to kitchen"

            if not isinstance(courier, Bike):
                print(
                    f"{courier.courier_type()} {courier.id} {state_str} with {courier.distance_to_destination:.2f} meters / {courier.time_to_destination():.2f} minutes left.  Battery time left: {courier.battery:.2f} minutes")
            else:
                print(
                    f"{courier.courier_type()} {courier.id} {state_str} with {courier.distance_to_destination:.2f} meters / {courier.time_to_destination():.2f} minutes left")

    print("-----------------------------------------------------------------------------------------------------------")
