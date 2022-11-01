class Order:
    def __init__(self, destination, time_ordered, weight, distance):
        self.destination = destination
        self.time_ordered = time_ordered
        self.weight = weight
        self.distance = distance

    def __str__(self):
        return f"Order to {self.destination} ordered at {self.time_ordered} minutes with distance {self.distance} meters"


