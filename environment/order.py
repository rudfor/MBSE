class Order:
    def __init__(self, destination, time_ordered, weight, distance, destination_node):
        self.destination = destination
        self.time_ordered = time_ordered
        self.weight = weight
        self.distance = distance
        self.destination_node = destination_node

    def __str__(self):
        return f"{self.distance} meters away at {self.destination} made at time {self.time_ordered:.2f}"


