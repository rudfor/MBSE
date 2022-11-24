from display.df_cost_time import number_of_deliveries, transit_time_distance, average_time_delivery, graph_plotting, \
    bike_cost, drone_cost
from display.plot_avg_time import plot


class Stats:
    def __init__(self):
        # For plotting
        self.total_orders_delivered = 0
        self.avg_order_time_data = []
        self.total_delivery_time = 0

        # This is for the cost/time calculation
        self.data_drone = []
        self.data_bike = []
        self.bike_orders_delivered = 0
        self.drone_orders_delivered = 0
        self.bike_total_delivery_time = 0
        self.drone_total_delivery_time = 0

        self.avg_bike_time = 0
        self.avg_bike = []
        self.avg_drone_time = 0
        self.avg_drone = []

        self.bike_orders = []
        self.drone_orders = []
        self.bike_time = []
        self.drone_time = []
        self.charged_total = 0

        self.orders_declined_by_drones_battery = []
        self.dronetype_orders_declined_by_drone = []
        self.orders_declined_by_drones_range = []
        self.total_orders_made = 0

        self.sim_time = None

    def update_bike_stats(self, current_time_minutes, event_bike, time_to_threshold):
        bike_delivery_time = event_bike.time_to_destination()
        self.bike_orders_delivered += 1  # if the graph should be showing cost/order --> need to be changed, if they can carry more than one order
        self.bike_total_delivery_time += bike_delivery_time
        avg_bike_time = self.bike_total_delivery_time / self.bike_orders_delivered
        self.avg_bike.append((current_time_minutes, avg_bike_time))
        self.data_bike.append((current_time_minutes, self.bike_total_delivery_time, self.bike_orders_delivered))
        self.bike_orders.append(self.bike_orders_delivered)
        self.bike_time.append((event_bike, bike_delivery_time, time_to_threshold))

    def update_avg_order_time(self, current_time_minutes, event_courier):
        self.total_orders_delivered += 1
        delivery_time = current_time_minutes - event_courier.order.time_ordered
        self.total_delivery_time += delivery_time
        avg_time = self.total_delivery_time / self.total_orders_delivered
        self.avg_order_time_data.append((current_time_minutes, avg_time))

    def update_drone_stats(self, current_time_minutes, event_drone, time_to_threshold):
        drone_delivery_time = event_drone.time_to_destination()
        self.drone_orders_delivered += 1  # if the graph should be showing cost/order --> need to be changed, if they can carry more than one order
        self.drone_total_delivery_time += drone_delivery_time
        charged_total = abs(
            (current_time_minutes - drone_delivery_time) - (current_time_minutes + drone_delivery_time))
        avg_drone_time = self.drone_total_delivery_time / self.drone_orders_delivered
        self.avg_drone.append((current_time_minutes, avg_drone_time, event_drone.id))
        self.data_drone.append(
            (current_time_minutes, self.drone_total_delivery_time, self.drone_orders_delivered, charged_total, event_drone.id))
        self.drone_orders.append((event_drone, self.drone_orders_delivered))
        self.drone_time.append((event_drone, drone_delivery_time, time_to_threshold))

    def plot_results(self):
        pass
        number_of_deliveries(self.bike_orders, self.drone_orders, self.orders_declined_by_drones_battery + self.orders_declined_by_drones_range)
        transit_time_distance(self.bike_time, self.drone_time)
        # average_time_delivery(self.avg_bike, 'bike')
        # average_time_delivery(self.avg_drone, 'drone')
        # graph_plotting(self.bike_orders, bike_cost(self.data_bike,self.sim_time), self.drone_orders, drone_cost(self.data_drone))
        # plot(self.avg_order_time_data)
