class Kitchen:
    def __init__(self, position):
        self.position = position
        self.orders = []

    def receive_orders(self, orders):
        self.orders.extend(orders)

    def pickup_order(self, courier):
        if len(self.orders) > 0:
            courier.order = self.orders[0]
            self.orders.remove(courier.order)
            return True
        return False

    def courier_present(self, courier):
        return courier.position == self.position
