"""
The function calculate the labor productivity ie. cost/time -> the formular used is: Total output / total input 

Input: ID, time and range. Where ID is used to compare the two systems with each order. Time is how long each order took and range is the distance from the resturan to the customer.
Range might not be used.

Output will be a plot to give an easy overview how the two systems compares to each other. Where the x-axis is time in hours over a periode of 1 or more hours
and y-axis is the labor productivity for that periode.

"""
#For the data
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import date

#getting the class
from system.bike import Bike
from system.drone import DroneType1, DroneType2, DroneType3

#Number of deleveries for both bikes and drones - also how many they missed
# Plottet against each other to show who took the most orders
def number_of_deliveries(bike, drone): # input: list of all orders for both bikes and drones also missed deliveries
    bike_orders = [i for i in bike]
    missed_bike_orders = []
    drone_orders = [i for i in drone]
    missed_drone_orders = []

    #change if they can take more than one delivery
    if len(bike_orders) > 0:
        last_bike = bike_orders.pop()
    else:
        print(f'No bikes assigned')
        last_bike=0

    if len(drone_orders) > 0:
        last_drone = drone_orders.pop()
    else:
        print(f'No bikes assigned')
        last_drone=0

    data = list(zip(bike_orders, drone_orders))
    df = pd.DataFrame(data, columns=['Bike orders', 'Drone Orders'])
    
   # Choose the width of each bar and their positions
    width = [0.1, 0.1]
    x_pos = [0,0.3]

    print(df)

    plt.title('Number of deliveries for bike compared to drone\n',fontsize = 14, fontweight ='bold')
    x_name = ['Bicycle order', 'Drone order']
    data_list = [last_bike, last_drone]
    plt.bar(x_pos, data_list, width=width)
    plt.xticks(x_pos, x_name)
    plt.show()

# The number or percentage of deliveries that have been delivered on-time compared to deliveries that haven't been on-time
def On_time_delivery(data):
    bike_on_time = []
    bike_not_time = []
    drone_on_time = []
    drone_not_time = []

    #not sure what data to get yet - maybe just plot a bar chart showing them against each order
    # Or ordinary graph showing that it might not be on time in rush hour, and thereby showing
    # a hybrid is the right solution --> just an asumption

#The travel time from the delivery have been picked up at the kitchen to the dropped-off at the customer
def transit_time_distance(bike, drone):# Input: bike_time, drone_time, -> simulator give the time it takes for each to reach distination
    bike1 = Bike(1)
    drone1 = DroneType1(1)
    drone2 = DroneType2(1)
    drone3 = DroneType3(1)

    bike_transit_time = [i for i in bike]
    bike_transit_distance = [i*bike1.avg_speed for i in bike]
    drone_transit_time = [i[1] for i in drone]
    drone_transit_distance = [i[1]*drone1.avg_speed if i[0]==1 else i[1]*drone2.avg_speed if i[0]==2 else i[1]*drone3.avg_speed for i in drone]

    data = list(zip( bike_transit_time, bike_transit_distance, drone_transit_time, drone_transit_distance))
    df = pd.DataFrame(data, columns=['Bike transit time','Bike distance', 'Drone transit time', 'Drone distance'])
    print(df)

    #plot the graph
    plt.title('Transit time to distance for bike compared to drone\n',fontsize = 14, fontweight ='bold')
    plt.plot(bike_transit_distance, bike_transit_time, 'b*', label='Bike transit')
    plt.plot(drone_transit_distance, drone_transit_time, 'r*', label='Drone transit')
    plt.xlabel('distance', fontsize=10)
    plt.ylabel('Time', fontsize=10)
    plt.xticks(bike_transit_distance, bike_transit_distance, rotation=90)
    plt.legend()
    plt.show()

    #maybe go for an ordinary graph to start with - see if I need to change it
    # Maybe a plot for showing distance vs. time
    

def average_time_delivery(data,plot):
    time_slots = [i[0] for i in data]
    avg_order_time = [i[1] for i in data]
    
    #plot the graph
    plt.title(f'Average time for delivering {plot} \n',fontsize = 14, fontweight ='bold')
    plt.plot(time_slots, avg_order_time, 'b', label='Average order delivery time over time')
    plt.xlabel('Hours', fontsize=10)
    plt.ylabel('Average order delivery time(minutes) for ', fontsize=10)
    plt.legend()
    plt.show()


def bike_cost(data):
    """
    # Function Average cost of delivery for the cost of delivery for bike
    # (Driver cost + Fuel cost + Vehicle cost) / total numbers of deliveries
    # - input: timestamp(x-axe), total order time, orders in total

    :param data:
    :return:
    """
    bike = Bike(1)
    delivery_wage = bike.cost_hour/60 #wage in minutes
    bike_total_orders = [i[2] for i in data]
    time_bike = [i[1] for i in data]
    cost_bike = [i[1]*delivery_wage for i in data]
    bike_total_output = [cost_bike[i]/bike_total_orders[i] for i in range(0,len(data))]
    return bike_total_output


def drone_cost(data):
    """
    Function for the cost of delivery for drone - input
     (Driver cost + Fuel cost + Vehicle cost) / total numbers of deliveries
     - input: timestamp(x-axe), total order time, orders in total
    """
    drone1 = DroneType1(1)
    drone2 = DroneType2(1)
    drone3 = DroneType3(1)
    time_drone = [i[1] for i in data]
    drone_total_orders = [i[2] for i in data]
    drone_start_cost = drone1.cost + drone2.cost + drone3.cost
    price_current = float(1.5)
    cost_drone = [i[3]*price_current for i in data] #price for charging the drone
    print(f'validating Cost_drone {cost_drone}')
    if len(cost_drone) > 0:
        cost_drone[0] = 0
    drone_total_output = [((cost_drone[j] + drone_start_cost )/drone_total_orders[j]) for j in range(0,len(data))]
    return drone_total_output

#Function to make a dataframe for panda and plot the result - input: bike time, bike cost, drone time and drone cost
def graph_plotting(bike_order, bike, drone_order, drone):
    bike_timestamp = bike_order
    drone_timestamp = drone_order
    bike_data = bike
    drone_data = drone

    data = list(zip(bike_timestamp, bike_data, drone_timestamp, drone_data))
    df = pd.DataFrame(data, columns=['Bike orders', 'Bike cost', 'Drone orders', 'Drone cost'])
    print(df)

    #plot the graph
    plt.title('Cost/Order for bike compared to drone\n',fontsize = 14, fontweight ='bold')
    plt.plot(bike_timestamp, bike_data, 'b', label='Bicycle cost')
    plt.plot(drone_timestamp, drone_data, 'r', label='Drone cost')
    plt.xlabel('Orders', fontsize=10)
    plt.ylabel('Cost', fontsize=10)
    plt.legend()
    plt.show()

    title = 'Bikes and drones'
    today = date.today()
    path = os.path.join(os.path.dirname(__file__), '..', 'excel')
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print(f'The new directory {path} is created!')
    #path = 'D:\\Documents\\GitHub\MBSE\\'
    file_name = f'{title}-{today}.xlsx'
    save_file_name = os.path.join(path, file_name)
    print(f'Name and location for file: {save_file_name}')
    
    print(f'Saving the file')
    if df.empty == True:
        print(f'The file is empty')
    else:
        print(f'Saving...')
        df.to_excel(save_file_name)

    print(f'Done')
