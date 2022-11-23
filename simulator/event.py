from enum import Enum

from system.bike import Bike
from system.courier import Courier
from system.drone import Drone


class Event:
    def __init__(self, event_type, event_time, event_obj):
        self.event_type = event_type
        self.event_time = event_time
        self.event_obj = event_obj


def from_courier(courier):
    if isinstance(courier, Bike):
        return EventType.Bike
    elif isinstance(courier, Drone):
        return EventType.Drone


class EventType(Enum):
    Order = 1
    Bike = 2
    Drone = 3
