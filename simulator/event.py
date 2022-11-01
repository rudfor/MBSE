from enum import Enum


class Event:
    def __init__(self, event_type, event_time, event_obj):
        self.event_type = event_type
        self.event_time = event_time
        self.event_obj = event_obj


class EventType(Enum):
    Order = 1
    Bike = 2
