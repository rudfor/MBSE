"""
The function calculate the labor productivity ie. cost/time -> the formular used is: Total output / total input 

Input: ID, time and range. Where ID is used to compare the two systems with each order. Time is how long each order took and range is the distance from the resturan to the customer.
Range might not be used.

Output will be a plot to give an easy overview how the two systems compares to each other. Where the x-axis is time in hours over a periode of 1 or more hours
and y-axis is the labor productivity for that periode.

"""
import random
import matplotlib.pyplot as plt
import datetime


#For test
n = 24*7

#read data from simulator - how to separate the two systems
#Nedunder skal erstattes med data fra simulatoren
bicycle_order_revenue = [random.randrange(25, 50, 1) for i in range(n)]
drone_order_revenue = [random.randrange(25, 50, 1) for i in range(n)]

#figure out the time, when I know the format
virt_hour = [i for i in range(n)]

#print(f'x = {virt_hour}\nbicycle = {bicycle_order_revenue}\n drone = {drone_order_revenue}')
#fix cost for the systems
interval_hours = 5 #the interval for each revenue
delivery_wage = 10*interval_hours
drone_maintain = 5*interval_hours

#Calculate the sum over a given interval and provide a new list
bicyle_sum_revenue = []
drone_sum_revenue = []
lower = 0
upper = interval_hours
max = n

for i in range(lower, n, interval_hours):
    bicyle_sum_revenue.append(sum(bicycle_order_revenue[lower:upper]))
    drone_sum_revenue.append(sum(drone_order_revenue[lower:upper]))
    #print(f'i: {i}  lower: {lower} -> upper: {upper} --> bicycle: {bicycle_order_revenue[lower:upper]}')
    lower = upper
    upper = upper + interval_hours    
    

offset_hour = [i for i in range(len(bicyle_sum_revenue))]

#print(f'bicycle_sum= {bicyle_sum_revenue}\n drone_sum={drone_sum_revenue}\n length={len(bicyle_sum_revenue)}')
  
#calculate labor productivity for both systems
bicycle_total_output = [((bicyle_sum_revenue[i] - delivery_wage)/interval_hours) for i in offset_hour]
drone_total_output = [((drone_sum_revenue[j] - drone_maintain)/interval_hours) for j in offset_hour]

#collect x- and y-values for the graph - done with revenue
#plot the graph
plt.plot(offset_hour, bicycle_total_output, 'b', label='Bicycle labor productivity')
plt.plot(offset_hour, drone_total_output, 'r', label='Drone labor productivity')
plt.xlabel('Hours', fontsize=10)
plt.ylabel('Labor productivity', fontsize=10)
plt.legend()
plt.show()




