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
import seaborn as sns
import numpy as np

# getting the class
from system.bike import Bike
from system.drone import DroneType1, DroneType2, DroneType3, DefaultDrone
from utility.argparser import args


def get_sim_time(data):
    return data


# Number of deleveries for both bikes and drones - also how many they missed
# Plottet against each other to show who took the most orders
def number_of_deliveries(bike, drone, declined):  # input: list of all orders for both bikes and drones also missed deliveries
    bike_orders = [i for i in bike]
    missed_bike_orders = []
    drone_orders_1 = [i[1] for i in drone if isinstance(i[0], DroneType1)]
    drone_orders_2 = [i[1] for i in drone if isinstance(i[0], DroneType2)]
    drone_orders_3 = [i[1] for i in drone if isinstance(i[0], DroneType3)]
    drone_orders_default = [i[1] for i in drone if isinstance(i[0], DefaultDrone)]
    drone_orders_total = len(drone_orders_1) + len(drone_orders_2) + len(drone_orders_3) + len(drone_orders_default)
    print(f"drone orders default {drone_orders_default}")
    # declined = [i[2] for i in drone]

    # drone_decline_orders_1 = [i[2] for i in drone if i[0]==4]
    # drone_decline_orders_2 = [i[2] for i in drone if i[0]==5]
    # drone_decline_orders_3 = [i[2] for i in drone if i[0]==6]

    # print(f'Decline drones: {drone_decline_orders_1}::{drone_decline_orders_2}::{drone_decline_orders_3}')

    # change if they can take more than one delivery - then it should be sum()
    if len(bike_orders) > 0:
        last_bike = len(bike_orders)
    else:
        print(f'No bikes assigned')
        last_bike = 0

    if len(drone_orders_1) > 0:
        last_drone_1 = len(drone_orders_1)
    else:
        print(f'Drone type 1 not assigned')
        last_drone_1 = 0

    if len(drone_orders_2) > 0:
        last_drone_2 = len(drone_orders_2)
    else:
        print(f'Drone type 2 not assigned')
        last_drone_2 = 0

    if len(drone_orders_3) > 0:
        last_drone_3 = len(drone_orders_3)
    else:
        print(f'Drone type 3 not assigned')
        last_drone_3 = 0

    if len(drone_orders_default) > 0:
        last_drone_default = len(drone_orders_default)
    else:
        print(f'DefaultDrone not assigned')
        last_drone_default = 0

    #drone_total_order = last_drone_1 + last_drone_2 + last_drone_3 + last_drone_default
    declined_orders = len(declined)
    # declined_orders = len(declined) - 1 if len(declined) > 0 else 0

    """ if len(drone_decline_orders_1) > 0:
        decline_last_drone_1 = -abs(drone_orders_1.pop())
    else:
        print(f'Drone type 1 no declined orders')
        decline_last_drone_1=0

    if len(drone_decline_orders_2) > 0:
        decline_last_drone_2 = -abs(drone_orders_2.pop())
    else:
        print(f'Drone type 2 no declined orders')
        decline_last_drone_2=0
    
    if len(drone_decline_orders_3) > 0:
        decline_last_drone_3 = -abs(drone_orders_3.pop())
    else:
        print(f'Drone type 3 no declined orders')
        decline_last_drone_3=0

    drone_decline_total_order = decline_last_drone_1 + decline_last_drone_2 + decline_last_drone_3 """

    orders_in_total = last_bike + drone_orders_total

    print(f'Total order: {orders_in_total}')
    bike_percent = round((last_bike / orders_in_total) * 100) if last_bike > 0 else 0
    drone_1_percent = round((last_drone_1 / orders_in_total) * 100) if last_drone_1 > 0 else 0
    drone_2_percent = round((last_drone_2 / orders_in_total) * 100) if last_drone_2 > 0 else 0
    drone_3_percent = round((last_drone_3 / orders_in_total) * 100) if last_drone_3 > 0 else 0
    drone_default_percent = round((last_drone_default / orders_in_total) * 100) if last_drone_default > 0 else 0

    drone_percent = drone_1_percent + drone_2_percent + drone_3_percent + drone_default_percent
    orders_percent = bike_percent + drone_1_percent + drone_2_percent + drone_3_percent + drone_default_percent
    declined_orders_percent = round((declined_orders / drone_orders_total) * 100) if declined_orders > 0 else 0

    label = ['Bike', 'DroneType1', 'DroneType2', 'DroneType3', 'DefaultDrone', 'Drone total', 'Orders declined by drones', 'Total']
    data_orders = [last_bike, last_drone_1, last_drone_2, last_drone_3, last_drone_default, drone_orders_total,
                   declined_orders, orders_in_total]
    data_percent = [bike_percent, drone_1_percent, drone_2_percent, drone_3_percent, drone_default_percent,
                    drone_percent, declined_orders_percent, orders_percent]

    data = list(zip(data_orders, data_percent))
    df = pd.DataFrame(data, columns=['Orders', 'Percent'], index=label)
    print(df)

    x = np.arange(len(label))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, data_orders, width, label='Number of orders')
    rects2 = ax.bar(x + width / 2, data_percent, width, label='Orders in percent')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Type')
    ax.set_title('Number of deliveries', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(label, rotation=45)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    #plt.savefig("Number of deliveries.jpg")
    plt.show()


# The travel time from the delivery have been picked up at the kitchen to the dropped-off at the customer
# Splitting the orders into distance and compare them that way - then it can be visualised what's the best option
# for close and long distance instead.
# maybe just a bar chart, showing which type took the closed, medium and longest away
def transit_time_distance(bike,
                          drone):  # Input: bike_time, drone_time, -> simulator give the time it takes for each to reach distination
    bike1 = Bike(1)
    drone1 = DroneType1(1)
    drone2 = DroneType2(1)
    drone3 = DroneType3(1)

    bike_transit_time = [i for i in bike]
    bike_transit_distance = [i * bike1.avg_speed for i in bike]
    range_bike = [
        i * 0 + 1000 if i <= 1000 else i * 0 + 2000 if i > 1000 and i <= 2000 else i * 0 + 3000 if i > 2000 and i <= 3000 else i * 0 + 4000 if i > 3000 and i <= 4000 else i * 0 + 5000
        for i in bike_transit_distance]

    drone_transit_time = [i[1] for i in drone]
    drone_transit_distance = [
        i[1] * drone1.avg_speed if i[0] == 4 else i[1] * drone2.avg_speed if i[0] == 5 else i[1] * drone3.avg_speed for
        i in drone]
    drone_range = [
        i * 0 + 1000 if i <= 1000 else i * 0 + 2000 if i > 1000 and i <= 2000 else i * 0 + 3000 if i > 2000 and i <= 3000 else i * 0 + 4000 if i > 3000 and i <= 4000 else i * 0 + 5000
        for i in drone_transit_distance]
    bike_type = ['Bike' for i in range(0, len(bike_transit_distance))]
    drone_type = ['Drone 1' if i[0] == 4 else 'Drone 2' if i[0] == 5 else 'Drone 3' for i in drone]

    # On time delivery
    treshold = 10
    bike_on_time = [True if i < treshold else False for i in bike]
    on_time_bike = bike_on_time.count(True)
    drone_on_time = [True if i[1] < treshold else False for i in drone]
    on_time_drone = drone_on_time.count(True)
    bike_orders = len(bike_on_time)
    drone_orders = len(drone_on_time)

    bike_on_time_percent = round((on_time_bike / bike_orders) * 100) if bike_orders > 0 else 0
    bike_not_ontime_percent = round(((bike_orders - on_time_bike) / bike_orders) * 100) if bike_orders > 0 else 0
    drone_on_time_percent = round((on_time_drone / drone_orders) * 100) if drone_orders > 0 else 0
    drone_not_ontime_percent = round(((drone_orders - on_time_drone) / drone_orders) * 100) if drone_orders > 0 else 0

    data_bike = list(zip(bike_transit_time, bike_transit_distance, range_bike, bike_type, bike_on_time))
    df_bike = pd.DataFrame(data_bike, columns=['Transit time', 'Distance', 'Range', 'Type', 'On time'])

    data_drone = list(zip(drone_transit_time, drone_transit_distance, drone_range, drone_type, drone_on_time))
    df_drone = pd.DataFrame(data_drone, columns=['Transit time', 'Distance', 'Range', 'Type', 'On time'])

    frames = [df_bike, df_drone]
    result = pd.concat(frames)
    print(result)

    # print(f'Ontime: {bike_on_time_percent}::{drone_on_time_percent}\nNot ontime: {bike_not_ontime_percent}::{drone_not_ontime_percent}')
    success_rate = [bike_on_time_percent, bike_not_ontime_percent]
    not_success_rate = [drone_on_time_percent, drone_not_ontime_percent]

    label = ['On-time', 'Not on-time']
    x = np.arange(len(label))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, success_rate, width, label='Bikes')
    rects2 = ax.bar(x + width / 2, not_success_rate, width, label='Drones')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Type')
    ax.set_title('On time delivery', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(label, rotation=45)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.savefig("On time delivery.jpg")
    plt.show()

    # Who takes the short, medium and long route
    label = ['Range 1000m', 'Range 2000m', 'Range 3000m', 'Range 4000m', 'Range 5000m']

    b1 = df_bike.value_counts(subset='Range')[1000] if 1000 in df_bike.values else 0
    b2 = df_bike.value_counts(subset='Range')[2000] if 2000 in df_bike.values else 0
    b3 = df_bike.value_counts(subset='Range')[3000] if 3000 in df_bike.values else 0
    b4 = df_bike.value_counts(subset='Range')[4000] if 4000 in df_bike.values else 0
    b5 = df_bike.value_counts(subset='Range')[5000] if 5000 in df_bike.values else 0

    d1 = df_drone.value_counts(subset='Range')[1000] if 1000 in df_drone.values else 0
    d2 = df_drone.value_counts(subset='Range')[2000] if 2000 in df_drone.values else 0
    d3 = df_drone.value_counts(subset='Range')[3000] if 3000 in df_drone.values else 0
    d4 = df_drone.value_counts(subset='Range')[4000] if 4000 in df_drone.values else 0
    d5 = df_drone.value_counts(subset='Range')[5000] if 5000 in df_drone.values else 0

    range_bike_count = [b1, b2, b3, b4, b5]
    range_drone_count = [d1, d2, d3, d4, d5]

    x = np.arange(len(label))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, range_bike_count, width, label='Range for bikes')
    rects2 = ax.bar(x + width / 2, range_drone_count, width, label='Range for drones')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Type')
    ax.set_title('Distance', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(label, rotation=45)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.savefig("Range_distance.jpg")
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
    #plt.savefig("Cost_Order.jpg")
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
