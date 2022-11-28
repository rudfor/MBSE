import sys

from simulator.map import Map
from simulator.config import KITCHEN_NODE_ID
from simulator.event import EventType, Event
from simulator.stats import Stats
from simulator.system import System
from system.bike import Bike
from system.courier import CourierState
from environment.order_generator import OrderGenerator
from system.drone import Drone
from utility.point import Point
from utility.argparser import args
import random

MINUTES_IN_DAY = 24 * 60

# Simulation configuration
TIME_LIMIT_MINUTES = args.TIME

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
STATS.sim_time = TIME_LIMIT_MINUTES


def day_no(current_time_minutes):
    return int(current_time_minutes) // MINUTES_IN_DAY


def get_traffic_factor(current_time_minutes):
    daystr, hour, minutes = get_clock(current_time_minutes)
    # No extra traffic in weekend
    if daystr == "saturday" or daystr == "sunday":
        return 1
    # morning traffic 07:00 - 09:00
    if 7 <= hour <= 9:
        return random.uniform(0.8, 0.9)
    # afternoon traffic 15:00 - 17:00
    if 15 <= hour <= 17:
        return random.uniform(0.8, 0.9)

    return 1


def get_clock(current_time_minutes):
    # 0 .. < 24*60
    offset = current_time_minutes % MINUTES_IN_DAY
    # 0 .. <= 23
    hour = int(offset / 60)
    # 0 .. < 60
    minutes = int(offset % 60)

    day_offset = int((current_time_minutes % (MINUTES_IN_DAY * 7)) / MINUTES_IN_DAY)
    day = ""
    if day_offset == 0:
        day = "monday"
    elif day_offset == 1:
        day = "tuesday"
    elif day_offset == 2:
        day = "wednesday"
    elif day_offset == 3:
        day = "thursday"
    elif day_offset == 4:
        day = "friday"
    elif day_offset == 5:
        day = "saturday"
    elif day_offset == 6:
        day = "sunday"

    return day, hour, minutes


def get_rain_interval():
    # It rains ~183 days / year in Leiden
    rain_stat = 183 / 365
    rain_t1 = random.uniform(0, MINUTES_IN_DAY)
    rain_t2 = random.uniform(0, MINUTES_IN_DAY)
    if random.random() < rain_stat:
        return min(rain_t1, rain_t2), max(rain_t1, rain_t2)
    return None


def get_order_factor(current_time_minutes):
    day, hour, _ = get_clock(current_time_minutes)

    order_factor = 1

    if day in ("friday", "saturday", "sunday"):
        order_factor -= .2
    if 12 <= hour < 14 or 18 <= hour < 20:
        order_factor -= .2

    return order_factor


# Assume simulator starts monday 00:00
def run_simulator():
    current_time_minutes = 0
    rain_interval = None
    day = -1

    # Let's always start with an order, for testing purposes
    next_order = Event(EventType.Order,
                       ORDER_GENERATOR.generate_time_until_order(get_order_factor(current_time_minutes)), None)
    STATS.total_orders_made += 1

    print_simulation_configuration()

    # Main loop. Simulate a specified number of minutes.
    while current_time_minutes <= TIME_LIMIT_MINUTES:
        # Print time info
        daystr, hour, minutes = get_clock(current_time_minutes)
        print(f"Time: {current_time_minutes:.2f} min. Clock: {daystr}, {hour}: {minutes}")

        traffic_factor = get_traffic_factor(current_time_minutes)
        weather_factor, day, rain_interval = get_weather_factor(current_time_minutes, day, rain_interval)
        order_factor = get_order_factor(current_time_minutes)

        traffic_status = "Ordinary" if traffic_factor == 1 else "Busy"
        print(f"TRAFFIC: {traffic_status} ({traffic_factor})")

        weather_status = "Regular" if weather_factor == 1 else "Rainy"
        print(f"WEATHER: {weather_status} ({weather_factor}) [{rain_interval}]")

        if .8 <= order_factor < 1:
            order_status = "Busy"
        elif .6 <= order_factor < .8:
            order_status = "Rush hour"
        else:
            order_status = "Regular"
        print(f"ORDERS: {order_status} ({order_factor})")

        # Adjust courier speed for traffic and weather
        for courier in SYSTEM.couriers:
            courier.set_speed(weather_factor, traffic_factor)

        print_state()

        if args.PLOT:
            MAP.plot_courier_paths(SYSTEM.couriers)

        # Get next event
        next_event = get_next_event(SYSTEM, next_order)

        # Increment and print current time
        current_time_minutes += next_event.event_time

        # Charge drones
        for drone in SYSTEM.drones():
            if drone.is_standby():
                drone.charge(next_event.event_time)

        # Move all couriers
        for courier in SYSTEM.couriers:
            courier.move(next_event.event_time, traffic_factor, weather_factor)

        # Perform operations depending on event type
        match next_event.event_type:
            case EventType.Order:
                # Generate order with random destination and append it to the orders queue
                order = ORDER_GENERATOR.generate_order(current_time_minutes)
                orders.append(order)
                print(f"EVENT: Incoming order {order}")

                next_order = Event(EventType.Order, ORDER_GENERATOR.generate_time_until_order(order_factor), None)

                STATS.total_orders_made += 1

            case EventType.Bike | EventType.Drone:
                event_courier = next_event.event_obj
                courier_event_str = "arrived at order destination" \
                    if next_event.event_obj.state == CourierState.ReturningToKitchen else "returned to kitchen"

                print(f"EVENT: {event_courier.courier_type()} {event_courier.id} {courier_event_str}")

                # Order delivered, update stats
                if not event_courier.is_standby() :
                    STATS.total_orders_delivered += 1
                    #STATS.update_avg_order_time(current_time_minutes, event_courier)
                    STATS.order_interarrival_time.append((current_time_minutes, args.BASE_ORDER_INTERARRIVAL_TIME * order_factor))
                    if next_event.event_type == EventType.Bike:
                        STATS.update_bike_stats(current_time_minutes, event_courier)
                    elif next_event.event_type == EventType.Drone:
                        STATS.update_drone_stats(current_time_minutes, event_courier)

        accept_orders(current_time_minutes)

    print_results()
    print()

    STATS.plot_results()


def get_weather_factor(current_time_minutes, day, rain_interval):
    if day_no(current_time_minutes) > day:
        day += 1
        rain_interval = get_rain_interval()
        # print(rain_interval)
    if rain_interval and rain_interval[0] <= current_time_minutes % MINUTES_IN_DAY <= rain_interval[1]:
        weather_factor = random.uniform(0.8, 0.9)
    else:
        weather_factor = 1
    return weather_factor, day, rain_interval


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


# Assign orders to standby couriers.
def accept_orders(current_time):
    if not orders:
        return

    # We should attempt to assign the orders to the drones first, such that orders far away are reserved for bikes.
    # Drones are also faster, so if both a bike and a drone can take an order, we choose the drone (for now).

    # Sort orders by ascending delivery time threshold
    orders_copy = orders.copy()
    orders_copy.sort(key=lambda o: o.time_to_threshold(current_time))
    # Collect standby bikes
    bikes_copy = SYSTEM.bikes.copy()
    bikes_copy = [b for b in bikes_copy if b.is_standby()]
    # Collect standby drones
    drones_copy = SYSTEM.drones().copy()
    drones_copy = [d for d in drones_copy if d.is_standby()]
    # Assign orders to couriers, starting with the most urgent order.
    # Prioritize drones wrt. battery range limit.
    orders_taken = []
    # Try to assign orders to drones
    for most_urgent_order in orders_copy:
        order_flag = False
        within_range = False
        if not drones_copy:
            break
        # Try to assign the order to a drone
        for drone in drones_copy:
            if drone.within_range(most_urgent_order):
                within_range = True
                if drone.take_order(most_urgent_order):
                    order_flag = True
                    # drones_copy.remove(drone)
                    orders_taken.append(most_urgent_order)
                    orders.remove(most_urgent_order)
                    print(f"ACTION: {drone.courier_type()} {drone.id} accepted order {most_urgent_order}, "
                          f"time to threshold: {most_urgent_order.time_to_threshold(current_time):.2f} min")
                    break
                # else:
                #     if most_urgent_order.id not in STATS.orders_declined_by_drones_battery:
                #         STATS.orders_declined_by_drones_battery.append(most_urgent_order.id)

        if not within_range:
            if (None, most_urgent_order.id) not in STATS.orders_declined_by_drones_range:
                STATS.orders_declined_by_drones_range.append((None, most_urgent_order.id))
        elif not order_flag:
            if (None, most_urgent_order.id) not in STATS.orders_declined_by_drones_battery:
                STATS.orders_declined_by_drones_battery.append((None, most_urgent_order.id))

            print(
                f"ACTION: {drone.courier_type()} {drone.id} with battery {drone.battery:.2f} minutes"
                f"/ {drone.avg_speed * drone.battery:.2f} meters left could not accept order {most_urgent_order}")

    # Remove orders taken by drones
    for o in orders_taken:
        orders_copy.remove(o)

    # Assign remaining orders to bikes
    if orders_copy:
        for bike in bikes_copy:
            if not orders_copy:
                break
            # Keep assigning orders to bike until full
            while bike.can_carry_more_orders() and orders_copy:
                most_urgent_order = orders_copy.pop(0)
                bike.hold_order(most_urgent_order)
                orders.remove(most_urgent_order)
                print(f"ACTION: {bike.courier_type()} {bike.id} holds order {most_urgent_order}, "
                      f"time to threshold: {most_urgent_order.time_to_threshold(current_time):.2f} min")

            break

    # Calculate delivery routes for bikes with orders
    for bike in bikes_copy:
        if bike.holds_orders():
            bikes_copy.remove(bike)

            shortest_route, shortest_route_distances = MAP.shortest_route_for_delivery(
                [o.destination_node for o in bike.orders])

            print(f"ACTION: {bike.courier_type()} {bike.id} accepted orders:")
            for order in bike.orders:
                print(order)

            # Start the delivery
            bike.take_orders(shortest_route, shortest_route_distances)

    if orders:
        print(f"ACTION: No couriers to take the following {len(orders)} order(s):")
        for order in orders:
            # print(order)
            print(str(order) + f", time to threshold: {order.time_to_threshold(current_time):.2f} min")


def print_results():
    print("Simulation results:")
    print(f"# orders made: {STATS.total_orders_made}")
    print(f"# orders in end queue: {len(orders)}")
    print(f"# orders delivered: {STATS.total_orders_delivered}")
    print(f"# bike orders delivered: {len(STATS.bike_orders_delivered)}")
    print(f"# drone orders delivered: {len(STATS.drone_orders_delivered)}")
    print(f"# orders declined by drones due to insufficient battery: "
          f"{len(STATS.orders_declined_by_drones_battery)}")
    print(f"# orders declined by drones due to distance: "
          f"{len(STATS.orders_declined_by_drones_range)}")
    try:
        print(f"Avg. bike delivery time: {STATS.avg_bike_delivery_times[-1][1]} min")
        print(f"Avg. drone delivery time: {STATS.avg_drone_delivery_times[-1][1]} min")
    except IndexError:
        pass


def print_simulation_configuration():
    print("Simulation configuration:")
    print(f"TIME_LIMIT_MINUTES: {TIME_LIMIT_MINUTES}")
    print(f"Kitchen at position ({KITCHEN_NODE['x']}, {KITCHEN_NODE['y']})")
    print(f"{SYSTEM.num_bikes} bikes available")
    print(f"{SYSTEM.num_drones()} drones available")
    print("-----------------------------------------------------------------------------------------------------------")


def print_state():
    print("STATUS:")
    for courier in SYSTEM.couriers:
        print(courier.status())
    print("-----------------------------------------------------------------------------------------------------------")
