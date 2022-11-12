from simulator.map import Map
from simulator.config import KITCHEN_NODE_ID
from simulator.event import EventType, Event, from_courier
from system.bike import Bike
from system.courier import CourierState
#from system.drone import Drone
#from system.kitchen import Kitchen
from environment.order_generator import OrderGenerator
from system.drone import DefaultDrone, DroneType1, DroneType2, DroneType3
from utility.point import Point
from utility.argparser import args
from display.df_cost_time import *
from display.plot_avg_time import *

# Simulation configuration
TIME_LIMIT_MINUTES = 300

# Environment
MAP = Map()
ORDER_GENERATOR = OrderGenerator(MAP)

# System
KITCHEN_NODE = MAP.get_node(KITCHEN_NODE_ID)
KITCHEN_POSITION = Point(KITCHEN_NODE['x'], KITCHEN_NODE['y'])

num_bikes = args.NUM_BIKES
num_drones_default = args.NUM_DD
num_drones_type1 = args.NUM_DT1
num_drones_type2 = args.NUM_DT2
num_drones_type3 = args.NUM_DT3
num_drones = num_drones_type1 + num_drones_type2 + num_drones_type3 + num_drones_default

bikes = [Bike(KITCHEN_POSITION) for _ in range(0, num_bikes)]
drones_default = [DefaultDrone(KITCHEN_POSITION) for _ in range(0, num_drones_default)]
drones_type1 = [DroneType1(KITCHEN_POSITION) for _ in range(0, num_drones_type1)]
drones_type2 = [DroneType2(KITCHEN_POSITION) for _ in range(0, num_drones_type2)]
drones_type3 = [DroneType3(KITCHEN_POSITION) for _ in range(0, num_drones_type3)]

couriers = []
couriers.extend(bikes)
couriers.extend(drones_default)
couriers.extend(drones_type1)
couriers.extend(drones_type2)
couriers.extend(drones_type3)
data1 = []
data2 = []
# todo: refactor drone classes, make battery charge time correct,

def run_simulator():
    current_time_minutes = 0
    # Let's always start with an order, for testing purposes
    next_order = Event(EventType.Order, 0, None)
    orders = []

    # For plotting
    total_orders_delivered = 0
    avg_order_time_data = []
    total_delivery_time = 0

    print_simulation_configuration()

    #This is for the cost/time calculation
    data_drone = []
    data_bike = []
    bike_orders_delivered = 0
    drone_orders_delivered = 0
    bike_total_delivery_time = 0
    drone_total_delivery_time = 0

    avg_bike_time = 0
    avg_bike = []
    avg_drone_time = 0
    avg_drone = []

    bike_orders = []
    drone_orders = []
    bike_time = []
    drone_time =[]
    charged_total = 0

    # Main loop. Simulate a specified number of minutes.
    while current_time_minutes <= TIME_LIMIT_MINUTES:
        # Get next event
        next_event = get_next_event(next_order)

        # Increment and print current time
        current_time_minutes += next_event.event_time
        print(f"Time: {current_time_minutes:.2f} minutes")

        # Charge drones
        for courier in couriers:
            if not isinstance(courier, Bike) and courier.is_standby():
                #courier.battery = min(courier.battery_capacity, courier.battery + next_event.event_time)
                courier.charge(next_event.event_time)

        # Move all couriers (bikes)
        for courier in couriers:
            courier.move(next_event.event_time)

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

                if bike_event_str == "arrived at order destination":
                    bike_delivery_time = event_bike.time_to_destination()
                    bike_orders_delivered += 1 #if the graph should be showing cost/order --> need to be changed, if they can carry more than one order
                    bike_total_delivery_time += bike_delivery_time
                    avg_bike_time = bike_total_delivery_time / bike_orders_delivered
                    avg_bike.append((current_time_minutes, avg_bike_time))
                    data_bike.append((current_time_minutes, bike_total_delivery_time, bike_orders_delivered ))
                    bike_orders.append(bike_orders_delivered)
                    bike_time.append(bike_delivery_time)

            case EventType.Bike | EventType.Drone:
                event_courier = next_event.event_obj
                drone_event_str = "arrived at order destination" if next_event.event_obj.state == CourierState.ReturningToKitchen else "returned to kitchen"
                print(f"EVENT: {event_courier.courier_type()} {event_courier.id} {drone_event_str}")

                # Order delivered, update stats
                if next_event.event_obj.state == CourierState.ReturningToKitchen:
                    total_orders_delivered += 1
                    delivery_time = current_time_minutes - event_courier.order.time_ordered
                    total_delivery_time += delivery_time

                    avg_time = total_delivery_time / total_orders_delivered
                    avg_order_time_data.append((current_time_minutes, avg_time))


                if (next_event.event_obj.state == CourierState.ReturningToKitchen):
                    drone_delivery_time = courier.time_to_destination()
                    drone_orders_delivered += 1 #if the graph should be showing cost/order --> need to be changed, if they can carry more than one order
                    drone_total_delivery_time += drone_delivery_time

                    charged_total = abs((current_time_minutes - drone_delivery_time) - (current_time_minutes + drone_delivery_time))
                    avg_drone_time = drone_total_delivery_time / drone_orders_delivered
                    avg_drone.append((current_time_minutes, avg_drone_time))
                    data_drone.append((current_time_minutes, drone_total_delivery_time, drone_orders_delivered, charged_total))
                    drone_orders.append(drone_orders_delivered)
                    drone_time.append((event_courier.id, drone_delivery_time))

        accept_orders(orders)

        print_state()

        if current_time_minutes >= TIME_LIMIT_MINUTES:
            #number_of_deliveries(bike_orders, drone_orders)
            transit_time_distance(bike_time, drone_time)
            average_time_delivery(avg_bike,'bike')
            average_time_delivery(avg_drone,'drone')
            graph_plotting(bike_orders, bike_cost(data_bike), drone_orders, drone_cost(data_drone))

        if args.PLOT:
            MAP.plot_courier_paths(couriers)

    plot(avg_order_time_data)


def get_next_event(next_order):
    # Find time until next bike event (when bike arrives at order destination or back to kitchen)
    courier_event = next_courier_event()

    # Reduce time to next event to time of order, if order happens before any bike event

    # If no bike events or order happens before bike event
    if courier_event is None or next_order.event_time < courier_event.event_time:
        return next_order

    # If order happens after (there must be a bike event at this point, otherwise we would have returned an order event)
    next_order.event_time -= courier_event.event_time
    return courier_event


def accept_orders(orders):
    # Assign orders to standby couriers (bikes), if any
    # TODO: when drones, select drone based on order distance and drone battery life
    for courier in couriers:
        if orders and courier.is_standby():
            order = orders[0]
            if courier.take_order(orders[0]):
                del orders[0]
                print(f"ACTION: {courier.courier_type()} {courier.id} accepted order {order}")
            else:
                print(
                    f"ACTION: {courier.courier_type()} {courier.id} with battery {courier.battery:.2f} minutes / {courier.avg_speed * courier.battery:.2f} meters left could not accept order {order}")

    if orders:
        print(f"ACTION: No couriers to take the following {len(orders)} order(s):")
        for order in orders:
            print(order)


def print_simulation_configuration():
    print("Simulation configuration:")
    print(f"TIME_LIMIT_MINUTES: {TIME_LIMIT_MINUTES}")
    print(f"Kitchen at position ({KITCHEN_NODE['x']}, {KITCHEN_NODE['y']})")
    print(f"{num_bikes} bikes available")
    print(f"{num_drones} drones available")
    print("-----------------------------------------------------------------------------------------------------------")


def adjust_event_for_order(time_until_next_event_minutes, time_until_next_order_minutes):
    order_is_next_event = False
    if time_until_next_event_minutes is None or time_until_next_order_minutes < time_until_next_event_minutes:
        time_until_next_event_minutes = time_until_next_order_minutes
        order_is_next_event = True
    elif time_until_next_event_minutes is not None:
        time_until_next_order_minutes -= time_until_next_event_minutes
    return order_is_next_event, time_until_next_event_minutes


def next_courier_event():
    time_until_next_event_minutes = None
    courier_event = None
    for courier in couriers:
        if not courier.is_standby():
            if time_until_next_event_minutes is None or courier.time_to_destination() < time_until_next_event_minutes:
                time_until_next_event_minutes = courier.time_to_destination()
                courier_event = Event(from_courier(courier), time_until_next_event_minutes, courier)
    return courier_event


def print_state():
    print("STATUS:")
    for courier in couriers:
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
