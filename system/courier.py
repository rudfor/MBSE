from abc import abstractmethod
from enum import Enum


class CourierState(Enum):
    Standby = 1
    DeliveringOrder = 2
    ReturningToKitchen = 3


class Courier:
    id_counter = 0

    def __init__(self, position, distance_to_destination):
        self.position = position
        self.order = None
        self.distance_to_destination = distance_to_destination
        self.avg_speed = None
        self.state = CourierState.Standby
        self.id = Courier.id_counter
        Courier.id_counter += 1

    def move(self, delta_time_minutes):
        if not self.is_standby():
            self.distance_to_destination -= delta_time_minutes * self.avg_speed

            if self.has_arrived():
                self.update_arrival()

    def is_delivering(self):
        return self.order is not None

    def time_to_destination(self):
        return self.distance_to_destination / self.avg_speed

    def is_standby(self):
        return self.state == CourierState.Standby

    def update_arrival(self):
        if self.state == CourierState.DeliveringOrder:
            self.state = CourierState.ReturningToKitchen
            self.distance_to_destination = self.order.distance
        elif self.state == CourierState.ReturningToKitchen:
            self.state = CourierState.Standby
            self.distance_to_destination = 0

    def take_order(self, order):
        self.order = order
        self.distance_to_destination = self.order.distance
        self.state = CourierState.DeliveringOrder
        return True

    def has_arrived(self):
        return self.distance_to_destination <= 0

    @abstractmethod
    def status(self):
        pass

    @abstractmethod
    def courier_type(self):
        pass
