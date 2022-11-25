"""
The function calculate the labor productivity ie. cost/time -> the formular used is: Total output / total input 

Input: ID, time and range. Where ID is used to compare the two systems with each order. Time is how long each order took and range is the distance from the resturan to the customer.
Range might not be used.

Output will be a plot to give an easy overview how the two systems compares to each other. Where the x-axis is time in hours over a periode of 1 or more hours
and y-axis is the labor productivity for that periode.

"""
# For the data
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import date
import numpy as np

# getting the class
from system.bike import Bike
from system.drone import DroneType1, DroneType2, DroneType3, DefaultDrone
from utility.argparser import args


def get_sim_time(data):
    return data


# Number of deleveries for both bikes and drones - also how many they missed
# Plottet against each other to show who took the most orders

# input: list of all orders for both bikes and drones also missed deliveries
def number_of_deliveries(bike_orders_delivered, drone_orders_delivered, orders_declined_by_drones_battery,
                         orders_declined_by_drones_range):
    dronetype1_orders_delivered = [order for drone, order in drone_orders_delivered if isinstance(drone, DroneType1)]
    dronetype2_orders_delivered = [order for drone, order in drone_orders_delivered if isinstance(drone, DroneType2)]
    dronetype3_orders_delivered = [order for drone, order in drone_orders_delivered if isinstance(drone, DroneType3)]
    defaultdrone_orders_delivered = [order for drone, order in drone_orders_delivered if
                                     isinstance(drone, DefaultDrone)]

    dronetype1_orders_declined_battery = [order for drone, order in orders_declined_by_drones_battery if
                                          isinstance(drone, DroneType1)]
    dronetype2_orders_declined_battery = [order for drone, order in orders_declined_by_drones_battery if
                                          isinstance(drone, DroneType2)]
    dronetype3_orders_declined_battery = [order for drone, order in orders_declined_by_drones_battery if
                                          isinstance(drone, DroneType3)]
    defaultdrone_orders_declined_battery = [order for drone, order in orders_declined_by_drones_battery if
                                            isinstance(drone, DefaultDrone)]

    dronetype1_orders_declined_range = [order for drone, order in orders_declined_by_drones_range if
                                        isinstance(drone, DroneType1)]
    dronetype2_orders_declined_range = [order for drone, order in orders_declined_by_drones_range if
                                        isinstance(drone, DroneType2)]
    dronetype3_orders_declined_range = [order for drone, order in orders_declined_by_drones_range if
                                        isinstance(drone, DroneType3)]
    defaultdrone_orders_declined_range = [order for drone, order in orders_declined_by_drones_range if
                                          isinstance(drone, DefaultDrone)]

    num_orders_total = len(bike_orders_delivered) + len(drone_orders_delivered)

    print(f'Total order: {num_orders_total}')

    label = ['Orders delivered by bike', 'Orders delivered by DroneType1', 'Orders delivered by DroneType2',
             'Orders delivered by DroneType3', 'Orders delivered by DefaultDrone', 'Total drone orders delivered',
             'Orders declined by drones due to battery', 'Orders declined by drones due to range',
             'Total orders delivered']
    data_orders = [len(bike_orders_delivered), len(dronetype1_orders_delivered), len(dronetype2_orders_delivered),
                   len(dronetype3_orders_delivered), len(defaultdrone_orders_delivered), len(drone_orders_delivered),
                   len(orders_declined_by_drones_battery), len(orders_declined_by_drones_range), num_orders_total]

    fig, ax = plt.subplots()

    ax.set_xticklabels(label, rotation=45)
    bars = ax.bar(label, data_orders, width=0.5)
    ax.bar_label(bars)

    fig.tight_layout()

    plt.show()


# The travel time from the delivery have been picked up at the kitchen to the dropped-off at the customer
# Splitting the orders into distance and compare them that way - then it can be visualised what's the best option
# for close and long distance instead.
# maybe just a bar chart, showing which type took the closed, medium and longest away
def delivery_time_intervals(bike, drone):
    num_bike_orders_0_15 = len([t[1] for t in bike if 0.0 <= t[1] < 15.0])
    num_bike_orders_15_30 = len([t[1] for t in bike if 15.0 <= t[1] < 30.0])
    num_bike_orders_30_45 = len([t[1] for t in bike if 30.0 <= t[1] < 45.0])
    num_bike_orders_45_60 = len([t[1] for t in bike if 45.0 <= t[1] <= 60.0])
    num_bike_orders_over_60 = len([t[1] for t in bike if t[1] > 60.0])

    num_drone_orders_0_15 = len([t[1] for t in drone if 0.0 <= t[1] < 15.0])
    num_drone_orders_15_30 = len([t[1] for t in drone if 15.0 <= t[1] < 30.0])
    num_drone_orders_30_45 = len([t[1] for t in drone if 30.0 <= t[1] < 45.0])
    num_drone_orders_45_60 = len([t[1] for t in drone if 45.0 <= t[1] < 60.0])
    num_drones_orders_over_60 = len([t[1] for t in drone if t[1] > 60.0])

    bike_orders = [num_bike_orders_0_15, num_bike_orders_15_30, num_bike_orders_30_45, num_bike_orders_45_60,
                   num_bike_orders_over_60]
    drone_orders = [num_drone_orders_0_15, num_drone_orders_15_30, num_drone_orders_30_45, num_drone_orders_45_60,
                    num_drones_orders_over_60]

    label = ['0-15 min', '15-30 min', '30-45 min', '45-60 min', '>60 min']
    x = np.arange(len(label))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width / 2, bike_orders, width, label='Bikes')
    rects2 = ax.bar(x + width / 2, drone_orders, width, label='Drones')

    ax.set_ylabel('Number of orders')
    ax.set_title('Delivery time intervals', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(label, rotation=45)
    ax.legend()
    ax.bar_label(rects1)
    ax.bar_label(rects2)

    fig.tight_layout()
    plt.show()

    # # Who takes the short, medium and long route
    # label = ['Range 1000m', 'Range 2000m', 'Range 3000m', 'Range 4000m', 'Range 5000m']

    # b1 = df_bike.value_counts(subset='Range')[1000] if 1000 in df_bike.values else 0
    # b2 = df_bike.value_counts(subset='Range')[2000] if 2000 in df_bike.values else 0
    # b3 = df_bike.value_counts(subset='Range')[3000] if 3000 in df_bike.values else 0
    # b4 = df_bike.value_counts(subset='Range')[4000] if 4000 in df_bike.values else 0
    # b5 = df_bike.value_counts(subset='Range')[5000] if 5000 in df_bike.values else 0

    # d1 = df_drone.value_counts(subset='Range')[1000] if 1000 in df_drone.values else 0
    # d2 = df_drone.value_counts(subset='Range')[2000] if 2000 in df_drone.values else 0
    # d3 = df_drone.value_counts(subset='Range')[3000] if 3000 in df_drone.values else 0
    # d4 = df_drone.value_counts(subset='Range')[4000] if 4000 in df_drone.values else 0
    # d5 = df_drone.value_counts(subset='Range')[5000] if 5000 in df_drone.values else 0

    # range_bike_count = [b1, b2, b3, b4, b5]
    # range_drone_count = [d1, d2, d3, d4, d5]

    # x = np.arange(len(label))  # the label locations
    # width = 0.35  # the width of the bars
    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width / 2, range_bike_count, width, label='Range for bikes')
    # rects2 = ax.bar(x + width / 2, range_drone_count, width, label='Range for drones')
    # # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Type')
    # ax.set_title('Distance', fontsize=14, fontweight='bold')
    # ax.set_xticks(x)
    # ax.set_xticklabels(label, rotation=45)
    # ax.legend()

    # autolabel(rects1, ax)
    # autolabel(rects2, ax)

    # fig.tight_layout()


def delivery_threshold(bike, drone):
    num_bike_orders_delivered = len(bike)
    num_bike_orders_delivered_late = len([t for t in bike if t[2] < 0])
    bike_on_time_percent = round(((
                                              num_bike_orders_delivered - num_bike_orders_delivered_late) / num_bike_orders_delivered) * 100) if num_bike_orders_delivered > 0 else 0
    bike_not_ontime_percent = round(
        (num_bike_orders_delivered_late / num_bike_orders_delivered) * 100) if num_bike_orders_delivered > 0 else 0

    num_drone_orders_delivered = len(drone)
    num_drone_orders_delivered_late = len([t for t in drone if t[2] < 0])
    drone_on_time_percent = round(((
                                               num_drone_orders_delivered - num_drone_orders_delivered_late) / num_drone_orders_delivered) * 100) if num_drone_orders_delivered > 0 else 0
    drone_not_ontime_percent = round(
        (num_drone_orders_delivered_late / num_drone_orders_delivered) * 100) if num_drone_orders_delivered > 0 else 0

    labels = "Bike on-time deliveries", "Bike late deliveries", "Drone on-time deliveries", "Drone late deliveries"
    sizes = (bike_on_time_percent, bike_not_ontime_percent, drone_on_time_percent, drone_not_ontime_percent)

    fig, ax = plt.subplots()
    ax.set_title("Delivery threshold performance")
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
    ax.axis("equal")

    plt.show()


def average_time_delivery(data, plot):
    time_slots = [i[0] for i in data]
    avg_order_time = [i[1] for i in data]

    if len(time_slots) == 0:
        time_slots = [0]
        avg_order_time = [0]

    # plot the graph
    plt.style.use('ggplot')
    plt.title(f'Average time for delivering {plot} \n', fontsize=14, fontweight='bold')
    plt.plot(time_slots, avg_order_time, 'b*-', label='Average order delivery time over time')
    plt.xlabel('Hours', fontsize=10)
    plt.ylabel('Average order delivery time(minutes) for ', fontsize=10)
    plt.legend()
    plt.savefig(f"Average time for {plot}.jpg")
    plt.show()


def bike_cost(data, time):
    """
    # Function Average cost of delivery for the cost of delivery for bike
    # (Driver cost(monthly wage)*numbers of employees + Fuel_cost*miles + Vehicle cost*number_of_vehicle) / total numbers of deliveries for a given interval
    # - input: timestamp(x-axe), total order time, orders in total

    :param data:
    :return:
    """
    bike = Bike(1)
    employees = args.NUM_BIKES
    delivery_wage = (
                            bike.cost_hour / 60) * time * employees  # TIME_LIMIT_MINUTES #wage in minutes; wage in minutes*time of simulation*number of employees
    bike_total_orders = [i[2] for i in data]
    time_bike = [i[1] for i in data]
    cost_bike = [i[1] * delivery_wage for i in data]
    # bike_total_output = [cost_bike[i]/bike_total_orders[i] for i in range(0,len(data))]
    bike_total_output = [delivery_wage / bike_total_orders[i] for i in range(0, len(data))]
    return bike_total_output


def drone_cost(data):
    """
    Function Average cost of delivery for drone - input
     (Driver cost(monthly wage)*numbers of employees + Fuel_cost*miles + Vehicle cost*number_of_vehicle) / total numbers of deliveries for a given interval
     - input: timestamp(x-axe), total order time, orders in total
    """

    drone_orders_1 = [i for i in data if i[4] == 4]
    drone_orders_2 = [i for i in data if i[4] == 5]
    drone_orders_3 = [i for i in data if i[4] == 6]

    drone1 = DroneType1(1)
    drone2 = DroneType2(1)
    drone3 = DroneType3(1)
    time_drone = [i[1] for i in data]
    drone_total_orders = [i[2] for i in data]
    drone_start_cost_1 = drone1.cost * 5 if len(drone_orders_1) > 0 else 0  # drone cost*number of drones
    drone_start_cost_2 = drone2.cost * 0 if len(drone_orders_2) > 0 else 0  # drone cost*number of drones
    drone_start_cost_3 = drone3.cost * 0 if len(drone_orders_3) > 0 else 0  # drone cost*number of drones
    drone_start_cost = drone_start_cost_1 + drone_start_cost_2 + drone_start_cost_3
    price_current = float(1.5)
    cost_drone = [i[3] * price_current for i in data]  # price for charging the drone
    # print(f'validating Cost_drone {cost_drone}')
    if len(cost_drone) > 0:
        cost_drone[0] = 0
    drone_total_output = [(cost_drone[j] + drone_start_cost) / drone_total_orders[j] for j in range(0, len(data))]
    # print(f'Drone output: {drone_total_output}')
    return drone_total_output


# Function to make a dataframe for panda and plot the result - input: bike time, bike cost, drone time and drone cost
def graph_plotting(bike_order, bike, drone_order, drone):
    bike_timestamp = [i for i in bike_order]
    drone_timestamp = [i[1] for i in drone_order]
    bike_data = [i for i in bike]
    drone_data = [i for i in drone]

    data_bike = list(zip(bike_order, bike))
    data_drone = list(zip(drone_timestamp, drone))

    df_bike = pd.DataFrame(data_bike, columns=['Order', 'Cost'])
    df_drone = pd.DataFrame(data_drone, columns=['Order', 'Cost'])

    df = pd.DataFrame(data_bike, columns=['Order', 'Cost'])
    # plot the graph
    plt.title('Cost/Order for bike compared to drone\n', fontsize=14, fontweight='bold')
    plt.plot(bike_timestamp, bike_data, 'b', label='Bicycle cost')
    plt.plot(drone_timestamp, drone_data, 'r', label='Drone cost')
    plt.xlabel('Orders', fontsize=10)
    plt.yscale("log")
    plt.autoscale()
    plt.ylabel('Cost', fontsize=10)
    plt.legend()
    # plt.savefig("Cost_Order.jpg")
    plt.show()

    # title = 'Bikes and drones'
    # today = date.today()
    # path = os.path.join(os.path.dirname(__file__), '..', 'excel')
    # isExist = os.path.exists(path)
    # if not isExist:
    #     # Create a new directory because it does not exist
    #     os.makedirs(path)
    #     print(f'The new directory {path} is created!')
    # # path = 'D:\\Documents\\GitHub\MBSE\\'
    # file_name = f'{title}-{today}.xlsx'
    # save_file_name = os.path.join(path, file_name)
    # print(f'Name and location for file: {save_file_name}')
    #
    # print(f'Saving the file')
    # if df.empty == True:
    #     print(f'The file is empty')
    # else:
    #     print(f'Saving...')
    #     df.to_excel(save_file_name)
    #
    # print(f'Done')
