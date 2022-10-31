class Courier:
    def __init__(self, position):
        self.position = position
        self.order = None

    def move(self, delta_time_minutes):
        pass

    def order_delivered(self):
        return self.position == self.order.position

    def is_delivering(self):
        return self.order is not None
