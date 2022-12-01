from display.df_cost_time import number_of_deliveries, delivery_time_intervals, delivery_threshold, \
    average_time_delivery, system_cost
from display.df_cost_time import drones_performance, number_of_deliveries, delivery_time_intervals, delivery_threshold
from utility.argparser import args


class Stats:
    def __init__(self):
        # For plotting
        self.total_orders_delivered = 0
        self.avg_order_time_data = []
        self.total_delivery_time = 0

        # This is for the cost/time calculation
        self.data_drone = []
        self.data_bike = []
        self.bike_orders_delivered = []
        self.drone_orders_delivered = []
        self.bike_total_delivery_time = 0
        self.drone_total_delivery_time = 0

        self.avg_bike_time = 0
        self.avg_bike_delivery_times = []
        self.avg_drone_time = 0
        self.avg_drone_delivery_times = []

        self.bike_orders = []
        self.drone_orders = []
        self.bike_time = []
        self.drone_time = []
        self.charged_total = 0

        self.orders_declined_by_drones_battery = []
        self.dronetype_orders_declined_by_drone = []
        self.orders_declined_by_drones_range = []
        self.total_orders_made = 0

        self.order_interarrival_time = []

        self.sim_time = None

    def update_bike_stats(self, current_time_minutes, event_bike):
        # bike_delivery_time = event_bike.time_to_destination()
        # self.bike_total_delivery_time += bike_delivery_time
        # avg_bike_time = self.bike_total_delivery_time / self.bike_orders_delivered
        # self.avg_bike.append((current_time_minutes, avg_bike_time))
        # self.data_bike.append((current_time_minutes, self.bike_total_delivery_time, self.bike_orders_delivered))
        # self.bike_orders.append(self.bike_orders_delivered)

        # Delivery time intervals
        order_delivered_on_time = 0 <= event_bike.last_order_delivered.time_to_threshold(current_time_minutes)
        order_delivery_time = current_time_minutes - event_bike.last_order_delivered.time_ordered
        self.bike_time.append((event_bike, order_delivery_time, order_delivered_on_time, current_time_minutes))

        # Avg. delivery time
        self.bike_total_delivery_time += order_delivery_time
        self.bike_orders_delivered.append((event_bike.last_order_delivered, current_time_minutes))
        avg_bike_delivery_time = self.bike_total_delivery_time / len(self.bike_orders_delivered)
        self.avg_bike_delivery_times.append((current_time_minutes, avg_bike_delivery_time))

    # def update_avg_order_time(self, current_time_minutes, event_courier):
    #     self.total_orders_delivered += 1
    #     delivery_time = current_time_minutes - event_courier.order.time_ordered
    #     self.total_delivery_time += delivery_time
    #     avg_time = self.total_delivery_time / self.total_orders_delivered
    #     self.avg_order_time_data.append((current_time_minutes, avg_time))

    def update_drone_stats(self, current_time_minutes, event_drone):
        # drone_delivery_time = event_drone.time_to_destination()
        # self.drone_orders_delivered += 1  # if the graph should be showing cost/order --> need to be changed, if they can carry more than one order
        # self.drone_total_delivery_time += drone_delivery_time
        # charged_total = abs(
        #     (current_time_minutes - drone_delivery_time) - (current_time_minutes + drone_delivery_time))
        # avg_drone_time = self.drone_total_delivery_time / self.drone_orders_delivered
        # self.avg_drone.append((current_time_minutes, avg_drone_time, event_drone.id))
        # self.data_drone.append(
        #     (current_time_minutes, self.drone_total_delivery_time, self.drone_orders_delivered, charged_total, event_drone.id))
        # self.drone_orders.append((event_drone, self.drone_orders_delivered))

        # Delivery time intervals
        time_to_threshold = event_drone.order.time_to_threshold(current_time_minutes)
        order_delivery_time = current_time_minutes - event_drone.order.time_ordered
        self.drone_time.append((event_drone, order_delivery_time, time_to_threshold))

        # Avg. delivery time
        self.drone_total_delivery_time += order_delivery_time
        self.drone_orders_delivered.append((event_drone, event_drone.order, current_time_minutes))
        avg_drone_delivery_time = self.drone_total_delivery_time / len(self.drone_orders_delivered)
        self.avg_drone_delivery_times.append((current_time_minutes, avg_drone_delivery_time))

    def plot_results(self):
        pass
        number_of_deliveries(self.bike_orders_delivered, self.drone_orders_delivered,
                             self.orders_declined_by_drones_battery, self.orders_declined_by_drones_range)
        delivery_time_intervals(self.bike_time, self.drone_time)
        delivery_threshold(self.bike_time, self.drone_time)
        drones_performance(self.drone_time)
        average_time_delivery(self.avg_bike_delivery_times, self.avg_drone_delivery_times, self.order_interarrival_time)
        #system_cost(self.bike_orders, bike_cost(self.data_bike, self.sim_time), self.drone_orders, drone_cost(self.data_drone))
        system_cost(self.bike_orders_delivered, self.drone_orders_delivered)
