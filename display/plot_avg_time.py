import matplotlib.pyplot as plt


# data = [(1,10), (2,10), (4, 12)]
def plot(data):
    time_slots = [i[0] for i in data]
    avg_order_time = [i[1] for i in data]

    # plot the graph
    plt.plot(time_slots, avg_order_time, 'b', label='Average order delivery time over time')
    # plt.plot(offset_hour, drone_total_output, 'r', label='Drone labor productivity')
    plt.xlabel('Hours', fontsize=10)
    plt.ylabel('Average order delivery time (minutes)', fontsize=10)
    plt.legend()
    plt.show()
