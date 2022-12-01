"""
The function calculate the labor productivity ie. cost/time -> the formular used is: Total output / total input 

Input: ID, time and range. Where ID is used to compare the two systems with each order. Time is how long each order took and range is the distance from the resturan to the customer.
Range might not be used.

Output will be a plot to give an easy overview how the two systems compares to each other. Where the x-axis is time in hours over a periode of 1 or more hours
and y-axis is the labor productivity for that periode.

"""
# For the data
import matplotlib.pyplot as plt
import numpy as np

from utility.constants import PROFIT_PER_ORDER
# getting the class
from system.drone import DroneType1, DroneType2, DroneType3, DefaultDrone
from utility.argparser import args


def get_sim_time(data):
    return data


# Number of deleveries for both bikes and drones - also how many they missed
# Plottet against each other to show who took the most orders

# input: list of all orders for both bikes and drones also missed deliveries
def number_of_deliveries(
        bike_orders_delivered,
        drone_orders_delivered,
        orders_declined_by_drones_battery,
        orders_declined_by_drones_range,
):
    dronetype1_orders_delivered = [
        order
        for drone, order, _ in drone_orders_delivered
        if isinstance(drone, DroneType1)
    ]
    dronetype2_orders_delivered = [
        order
        for drone, order, _ in drone_orders_delivered
        if isinstance(drone, DroneType2)
    ]
    dronetype3_orders_delivered = [
        order
        for drone, order, _ in drone_orders_delivered
        if isinstance(drone, DroneType3)
    ]
    defaultdrone_orders_delivered = [
        order
        for drone, order, _ in drone_orders_delivered
        if isinstance(drone, DefaultDrone)
    ]

    dronetype1_orders_declined_battery = [
        order
        for drone, order in orders_declined_by_drones_battery
        if isinstance(drone, DroneType1)
    ]
    dronetype2_orders_declined_battery = [
        order
        for drone, order in orders_declined_by_drones_battery
        if isinstance(drone, DroneType2)
    ]
    dronetype3_orders_declined_battery = [
        order
        for drone, order in orders_declined_by_drones_battery
        if isinstance(drone, DroneType3)
    ]
    defaultdrone_orders_declined_battery = [
        order
        for drone, order in orders_declined_by_drones_battery
        if isinstance(drone, DefaultDrone)
    ]

    dronetype1_orders_declined_range = [
        order
        for drone, order in orders_declined_by_drones_range
        if isinstance(drone, DroneType1)
    ]
    dronetype2_orders_declined_range = [
        order
        for drone, order in orders_declined_by_drones_range
        if isinstance(drone, DroneType2)
    ]
    dronetype3_orders_declined_range = [
        order
        for drone, order in orders_declined_by_drones_range
        if isinstance(drone, DroneType3)
    ]
    defaultdrone_orders_declined_range = [
        order
        for drone, order in orders_declined_by_drones_range
        if isinstance(drone, DefaultDrone)
    ]

    num_orders_total = len(bike_orders_delivered) + len(drone_orders_delivered)

    # cprint(f"Total order: {num_orders_total}")

    data = [('Declined by drones due to battery', len(orders_declined_by_drones_battery) / num_orders_total * 100),
            ('Declined by drones due to range', len(orders_declined_by_drones_range) / num_orders_total * 100),
            ('Delivered by DroneType1', len(dronetype1_orders_delivered) / num_orders_total * 100),
            ('Delivered by DroneType2', len(dronetype2_orders_delivered) / num_orders_total * 100),
            ('Delivered by DroneType3', len(dronetype3_orders_delivered) / num_orders_total * 100),
            ('Delivered by DefaultDrone', len(defaultdrone_orders_delivered) / num_orders_total * 100),
            ('Delivered by drones', len(drone_orders_delivered) / num_orders_total * 100),
            ('Delivered by bikes', len(bike_orders_delivered) / num_orders_total * 100)]
    labels = [label for label, _ in data]
    orders_data = [n for _, n in data]

    fig, ax = plt.subplots()
    plt.xlabel("Number of orders (%)")
    plt.xlim([0, 100])
    plt.title("Order delivery", fontsize=14, fontweight="bold")
    bars = ax.barh(labels, orders_data)
    # ax.bar_label(bars)
    ax.margins(x=0.3)
    fig.tight_layout()

    rects = ax.patches
    for rect in rects:
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2
        space = 5
        label = "{:.2f}%".format(x_value)
        plt.annotate(
            label,
            (x_value, y_value),
            xytext=(space, 0),  # Horizontally shift label by `space`
            textcoords="offset points",
            va='center')
    
    plt.show()


def delivery_time_intervals(bike, drone):
    num_bike_orders = len(bike)
    num_bike_orders_0_15 = len([t[1] for t in bike if 0.0 <= t[1] < 15.0])
    num_bike_orders_15_30 = len([t[1] for t in bike if 15.0 <= t[1] < 30.0])
    num_bike_orders_30_45 = len([t[1] for t in bike if 30.0 <= t[1] < 45.0])
    num_bike_orders_45_60 = len([t[1] for t in bike if 45.0 <= t[1] <= 60.0])
    num_bike_orders_over_60 = len([t[1] for t in bike if t[1] > 60.0])

    num_drone_orders = len(drone)
    num_drone_orders_0_15 = len([t[1] for t in drone if 0.0 <= t[1] < 15.0])
    num_drone_orders_15_30 = len([t[1] for t in drone if 15.0 <= t[1] < 30.0])
    num_drone_orders_30_45 = len([t[1] for t in drone if 30.0 <= t[1] < 45.0])
    num_drone_orders_45_60 = len([t[1] for t in drone if 45.0 <= t[1] < 60.0])
    num_drones_orders_over_60 = len([t[1] for t in drone if t[1] > 60.0])

    labels = "0-15 min", "15-30 min", "30-45 min", "45-60 min", ">60 min"

    bike_orders_percent = [
        round(num_bike_orders_0_15 / num_bike_orders * 100, 2) if num_bike_orders > 0 else 0,
        round(num_bike_orders_15_30 / num_bike_orders * 100, 2) if num_bike_orders > 0 else 0,
        round(num_bike_orders_30_45 / num_bike_orders * 100, 2) if num_bike_orders > 0 else 0,
        round(num_bike_orders_45_60 / num_bike_orders * 100, 2) if num_bike_orders > 0 else 0,
        round(num_bike_orders_over_60 / num_bike_orders * 100, 2) if num_bike_orders > 0 else 0,
    ]

    drone_orders_percent = [
        round(num_drone_orders_0_15 / num_drone_orders * 100, 2) if num_drone_orders > 0 else 0,
        round(num_drone_orders_15_30 / num_drone_orders * 100, 2) if num_drone_orders > 0 else 0,
        round(num_drone_orders_30_45 / num_drone_orders * 100, 2) if num_drone_orders > 0 else 0,
        round(num_drone_orders_45_60 / num_drone_orders * 100, 2) if num_drone_orders > 0 else 0,
        round(num_drones_orders_over_60 / num_drone_orders * 100, 2) if num_drone_orders > 0 else 0,
    ]

    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width / 2, bike_orders_percent, width, label="Bikes")
    rects2 = ax.bar(x + width / 2, drone_orders_percent, width, label="All drone types")

    ax.set_ylabel("Number of orders (%)")
    ax.set_title("Orders delivered within time intervals", fontsize=14, fontweight="bold")
    ax.set_xticks(x, labels)
    ax.legend(fontsize=10)
    ax.bar_label(rects1, fmt='%.2f%%', fontsize=7.5)
    ax.bar_label(rects2, fmt='%.2f%%', fontsize=7.5)

    fig.tight_layout()
    plt.show()


def delivery_threshold(bike, drone):
    num_bike_orders_delivered = len(bike)
    num_bike_orders_delivered_on_time = len([t for t in bike if t[2] >= 0])
    num_bike_orders_delivered_late = len([t for t in bike if t[2] < 0])

    bike_on_time_percent = (
        round(num_bike_orders_delivered_on_time / num_bike_orders_delivered * 100)
        if num_bike_orders_delivered > 0
        else 0
    )
    bike_not_ontime_percent = (
        round(num_bike_orders_delivered_late / num_bike_orders_delivered * 100)
        if num_bike_orders_delivered > 0
        else 0
    )

    num_drone_orders_delivered = len(drone)
    num_drone_orders_delivered_on_time = len([t for t in drone if t[2] >= 0])
    num_drone_orders_delivered_late = len([t for t in drone if t[2] < 0])

    drone_on_time_percent = (
        round(num_drone_orders_delivered_on_time / num_drone_orders_delivered * 100)
        if num_drone_orders_delivered > 0
        else 0
    )
    drone_not_ontime_percent = (
        round(num_drone_orders_delivered_late / num_drone_orders_delivered * 100)
        if num_drone_orders_delivered > 0
        else 0
    )

    labels = (
        "Bike on-time deliveries",
        "Bike late deliveries",
        "Drone on-time deliveries",
        "Drone late deliveries",
    )
    sizes = (
        bike_on_time_percent,
        bike_not_ontime_percent,
        drone_on_time_percent,
        drone_not_ontime_percent,
    )

    fig, ax = plt.subplots()
    ax.set_title("On-time delivery performance", pad=25, fontweight="bold", fontsize=14)
    ax.pie(sizes, autopct="%1.2f%%", shadow=True, startangle=90)
    ax.axis("equal")
    plt.legend(labels)

    plt.show()


def drones_performance(drone_orders):
    num_dronetype1_orders_delivered = len(
        [drone for drone, _, _ in drone_orders if isinstance(drone, DroneType1)]
    )

    num_dronetype1_orders_delivered_on_time = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DroneType1) and time_to_threshold >= 0
        ]
    )
    num_dronetype1_orders_delivered_late = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DroneType1) and time_to_threshold < 0
        ]
    )

    num_dronetype2_orders_delivered = len(
        [drone for drone, _, _ in drone_orders if isinstance(drone, DroneType2)]
    )

    num_dronetype2_orders_delivered_on_time = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DroneType2) and time_to_threshold >= 0
        ]
    )
    num_dronetype2_orders_delivered_late = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DroneType2) and time_to_threshold < 0
        ]
    )

    num_dronetype3_orders_delivered = len(
        [drone for drone, _, _ in drone_orders if isinstance(drone, DroneType3)]
    )

    num_dronetype3_orders_delivered_on_time = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DroneType3) and time_to_threshold >= 0
        ]
    )
    num_dronetype3_orders_delivered_late = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DroneType3) and time_to_threshold < 0
        ]
    )

    num_defaultdrone_orders_delivered = len(
        [drone for drone, _, _ in drone_orders if isinstance(drone, DefaultDrone)]
    )

    num_defaultdrone_orders_delivered_on_time = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DefaultDrone) and time_to_threshold >= 0
        ]
    )
    num_defaultdrone_orders_delivered_late = len(
        [
            drone
            for drone, _, time_to_threshold in drone_orders
            if isinstance(drone, DefaultDrone) and time_to_threshold < 0
        ]
    )

    on_time_orders_percent = [
        round(
            num_dronetype1_orders_delivered_on_time
            / num_dronetype1_orders_delivered
            * 100
        )
        if num_dronetype1_orders_delivered > 0
        else 0,
        round(
            num_dronetype2_orders_delivered_on_time
            / num_dronetype2_orders_delivered
            * 100
        )
        if num_dronetype2_orders_delivered > 0
        else 0,
        round(
            num_dronetype3_orders_delivered_on_time
            / num_dronetype3_orders_delivered
            * 100
        )
        if num_dronetype3_orders_delivered > 0
        else 0,
        round(
            num_defaultdrone_orders_delivered_on_time
            / num_defaultdrone_orders_delivered
            * 100
        )
        if num_defaultdrone_orders_delivered > 0
        else 0,
    ]

    late_orders_percent = [
        round(
            num_dronetype1_orders_delivered_late / num_dronetype1_orders_delivered * 100
        )
        if num_dronetype1_orders_delivered > 0
        else 0,
        round(
            num_dronetype2_orders_delivered_late / num_dronetype2_orders_delivered * 100
        )
        if num_dronetype2_orders_delivered > 0
        else 0,
        round(
            num_dronetype3_orders_delivered_late / num_dronetype3_orders_delivered * 100
        )
        if num_dronetype3_orders_delivered > 0
        else 0,
        round(
            num_defaultdrone_orders_delivered_late
            / num_defaultdrone_orders_delivered
            * 100
        )
        if num_defaultdrone_orders_delivered > 0
        else 0,
    ]

    labels = "DroneType1", "DroneType2", "DroneType3", "DefaultDrone"
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()

    rects1 = ax.bar(
        x - width / 2, on_time_orders_percent, width, label="On-time deliveries"
    )
    rects2 = ax.bar(x + width / 2, late_orders_percent, width, label="Late deliveries")

    ax.set_ylabel("%")
    ax.set_title(
        "On-time delivery performance per drone type", fontsize=14, fontweight="bold"
    )
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1)
    ax.bar_label(rects2)

    fig.tight_layout()
    plt.show()


def average_time_delivery(bike_data, drone_data, order_interarrival_time):
    # plot the graph
    plt.style.use('ggplot')
    # plt.title(f'Average time for delivering {plot} \n', fontsize=14, fontweight='bold')
    plt.plot([time for time, _ in bike_data], [avg for _, avg in bike_data], 'r-', label='Avg. bike delivery time')
    plt.plot([time for time, _ in drone_data], [avg for _, avg in drone_data], 'b-', label='Avg. drone delivery time')
    plt.plot([time for time, _ in order_interarrival_time],
             [interarrival_time for _, interarrival_time in order_interarrival_time], 'g--',
             label='Order interarrival time')
    plt.xlabel('Elapsed time (minutes)', fontsize=10)
    plt.ylabel('Time (minutes)', fontsize=10)
    plt.title("Average delivery time", fontsize=14, fontweight="bold")
    plt.legend()
    plt.show()


# Function to make a dataframe for panda and plot the result - input: bike time, bike cost, drone time and drone cost
def system_cost(bike_orders_delivered, drone_orders_delivered):
    bike_costs_total = args.NUM_BIKES * args.BIKE_HOUR_COST / 60 * args.TIME

    drone_nums = [args.NUM_DD, args.NUM_DT1, args.NUM_DT2, args.NUM_DT3]
    drone_costs = [DefaultDrone.cost, DroneType1.cost, DroneType2.cost, DroneType3.cost]
    drone_costs_total = sum([num * cost for num, cost in zip(drone_nums, drone_costs)])

    bike_times = [t for _, t in bike_orders_delivered]
    drone_times = [t for _, _, t in drone_orders_delivered]
    bs = [(t, PROFIT_PER_ORDER * (i + 1) - bike_costs_total) for i, t in enumerate(bike_times)]
    ds = [(t, PROFIT_PER_ORDER * (i + 1) - drone_costs_total) for i, t in enumerate(drone_times)]

    plt.title("Net profit by bikes and drones over time \n", fontsize=14, fontweight="bold")
    plt.plot(*zip(*bs), label="Net profit of bikes")
    plt.plot(*zip(*ds), label="Net profit of drones")
    plt.xlabel("Time elapsed (min)", fontsize=10)
    plt.autoscale()
    plt.ylabel("Net profit (DKK)", fontsize=10)
    plt.legend()
    plt.show()
