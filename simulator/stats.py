from display.plotting import number_of_deliveries, delivery_time_intervals, delivery_threshold, \
    average_time_delivery, system_cost
from display.plotting import drones_performance, number_of_deliveries, delivery_time_intervals, delivery_threshold


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
        # Delivery time intervals
        order_delivered_on_time = 0 <= event_bike.last_order_delivered.time_to_threshold(current_time_minutes)
        order_delivery_time = current_time_minutes - event_bike.last_order_delivered.time_ordered
        self.bike_time.append((event_bike, order_delivery_time, order_delivered_on_time, current_time_minutes))

        # Avg. delivery time
        self.bike_total_delivery_time += order_delivery_time
        self.bike_orders_delivered.append((event_bike.last_order_delivered, current_time_minutes))
        avg_bike_delivery_time = self.bike_total_delivery_time / len(self.bike_orders_delivered)
        self.avg_bike_delivery_times.append((current_time_minutes, avg_bike_delivery_time))

    def update_drone_stats(self, current_time_minutes, event_drone):
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
        number_of_deliveries(self.bike_orders_delivered, self.drone_orders_delivered,
                             self.orders_declined_by_drones_battery, self.orders_declined_by_drones_range)
        delivery_time_intervals(self.bike_time, self.drone_time)
        delivery_threshold(self.bike_time, self.drone_time)
        if self.drone_time:
            drones_performance(self.drone_time)
        average_time_delivery(self.avg_bike_delivery_times, self.avg_drone_delivery_times, self.order_interarrival_time)
        system_cost(self.bike_orders_delivered, self.drone_orders_delivered)
