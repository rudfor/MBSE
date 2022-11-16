from simulator.map import Map
from simulator.config import KITCHEN_NODE_ID
from simulator.event import EventType, Event
from simulator.stats import Stats
from simulator.system import System
from system.courier import CourierState
from environment.order_generator import OrderGenerator
from system.drone import Drone
from utility.point import Point
from utility.argparser import args
from display.df_cost_time import *

# Simulation configuration
TIME_LIMIT_MINUTES = 800

# Environment
MAP = Map()
ORDER_GENERATOR = OrderGenerator(MAP)

# System
KITCHEN_NODE = MAP.get_node(KITCHEN_NODE_ID)
KITCHEN_POSITION = Point(KITCHEN_NODE['x'], KITCHEN_NODE['y'])
SYSTEM = System(KITCHEN_POSITION)
orders = []

# Statistics tracking
STATS = Stats()


def run_simulator():
    current_time_minutes = 0

    # Let's always start with an order, for testing purposes
    next_order = Event(EventType.Order, 0, None)
    STATS.total_orders_made += 1

    print_simulation_configuration()

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

                STATS.total_orders_made += 1

            case EventType.Bike | EventType.Drone:
                event_courier = next_event.event_obj
                bike_event_str = "arrived at order destination" \
                    if next_event.event_obj.state == CourierState.ReturningToKitchen else "returned to kitchen"

                print(f"EVENT: {event_courier.courier_type()} {event_courier.id} {bike_event_str}")

                # Order delivered, update stats
                if event_courier.state == CourierState.ReturningToKitchen:
                    STATS.update_avg_order_time(current_time_minutes, event_courier)
                    if next_event.event_type == EventType.Bike:
                        STATS.update_bike_stats(current_time_minutes, event_courier)
                    elif next_event.event_type == EventType.Drone:
                        STATS.update_drone_stats(current_time_minutes, event_courier)

        accept_orders()

        print_state()

        if args.PLOT:
            MAP.plot_courier_paths(SYSTEM.couriers)

    print_results()
    print()

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


def accept_orders():
    # Assign orders to standby couriers, if any
    # TODO: when drones, select drone based on order distance and drone battery life
    for bike in SYSTEM.bikes:
        if orders and bike.is_standby():
            order = orders[0]
            if bike.take_order(orders[0]):
                del orders[0]
                print(f"ACTION: {bike.courier_type()} {bike.id} accepted order {order}")

    for drone in SYSTEM.drones():
        if orders and drone.is_standby():
            order = orders[0]
            if drone.take_order(orders[0]):
                del orders[0]
                print(f"ACTION: {drone.courier_type()} {drone.id} accepted order {order}")
            else:
                if order.id not in STATS.orders_declined_by_drones:
                    STATS.orders_declined_by_drones.append(order.id)

                print(
                    f"ACTION: {drone.courier_type()} {drone.id} with battery {drone.battery:.2f} minutes"
                    f"/ {drone.avg_speed * drone.battery:.2f} meters left could not accept order {order}")

    if orders:
        print(f"ACTION: No couriers to take the following {len(orders)} order(s):")
        for order in orders:
            print(order)


def print_results():
    print("Simulation results:")
    print(f"# orders made: {STATS.total_orders_made}")
    print(f"# orders in end queue: {len(orders)}")
    print(f"# orders delivered: {STATS.total_orders_delivered}")
    print(f"# bike orders delivered: {STATS.bike_orders_delivered}")
    print(f"# drone orders delivered: {STATS.drone_orders_delivered}")
    print(f"# orders declined by drones due to insufficient battery: "
          f"{len(STATS.orders_declined_by_drones)}")
    print(f"Avg. bike delivery time: {STATS.avg_bike[-1][1]} minutes")
    print(f"Avg. drone delivery time: {STATS.avg_drone[-1][1]} minutes")


def print_simulation_configuration():
    print("Simulation configuration:")
    print(f"TIME_LIMIT_MINUTES: {TIME_LIMIT_MINUTES}")
    print(f"Kitchen at position ({KITCHEN_NODE['x']}, {KITCHEN_NODE['y']})")
    print(f"{SYSTEM.num_bikes} bikes available")
    print(f"{SYSTEM.num_drones()} drones available")
    print("-----------------------------------------------------------------------------------------------------------")


def print_state():
    print("STATUS:")

    for bike in SYSTEM.bikes:
        if bike.is_standby():
            print(f"{bike.courier_type()} {bike.id} standby at kitchen")
        else:
            state_str = "delivering order" if bike.state == CourierState.DeliveringOrder else "returning to kitchen"
            print(
                f"{bike.courier_type()} {bike.id} {state_str} with {bike.distance_to_destination:.2f} meters"
                f"/ {bike.time_to_destination():.2f} minutes left")

    for drone in SYSTEM.drones():
        if drone.is_standby():
            print(f"{drone.courier_type()} {drone.id} standby at kitchen."
                  f"Battery time left: {drone.battery:.2f} minutes")
        else:
            state_str = "delivering order" if drone.state == CourierState.DeliveringOrder else "returning to kitchen"
            print(f"{drone.courier_type()} {drone.id} {state_str} with {drone.distance_to_destination:.2f} meters"
                  f"/ {drone.time_to_destination():.2f} minutes left.  Battery time left: {drone.battery:.2f} minutes")

    print("-----------------------------------------------------------------------------------------------------------")
