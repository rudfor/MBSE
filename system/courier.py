class Courier:
    def __init__(self, position):
        self.position = position
        self.order = None

    def move(self):
        pass

    def order_delivered(self):
        return self.position == self.order.position
