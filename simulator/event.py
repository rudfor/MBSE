from enum import Enum

from system.bike import Bike
from system.courier import Courier
from system.drone import DroneType1, DroneType2, DroneType3


class Event:
    def __init__(self, event_type, event_time, event_obj):
        self.event_type = event_type
        self.event_time = event_time
        self.event_obj = event_obj


def from_courier(courier):
    if isinstance(courier, Bike):
        return EventType.Bike
    elif isinstance(courier, DroneType1) or isinstance(courier, DroneType2) or isinstance(courier, DroneType3):
        return EventType.Drone


class EventType(Enum):
    Order = 1
    Bike = 2
    Drone = 3
