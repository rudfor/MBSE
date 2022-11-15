from simulator.event import Event, from_courier
from system.bike import Bike
from system.drone import DefaultDrone, DroneType1, DroneType2, DroneType3, Drone
from utility.argparser import args


class System:
    def __init__(self, kitchen_position):
        self.num_bikes = args.NUM_BIKES
        self.num_drones_default = args.NUM_DD
        self.num_drones_type1 = args.NUM_DT1
        self.num_drones_type2 = args.NUM_DT2
        self.num_drones_type3 = args.NUM_DT3

        self.bikes = [Bike(kitchen_position) for _ in range(0, self.num_bikes)]
        self.drones_default = [DefaultDrone(kitchen_position) for _ in range(0, self.num_drones_default)]
        self.drones_type1 = [DroneType1(kitchen_position) for _ in range(0, self.num_drones_type1)]
        self.drones_type2 = [DroneType2(kitchen_position) for _ in range(0, self.num_drones_type2)]
        self.drones_type3 = [DroneType3(kitchen_position) for _ in range(0, self.num_drones_type3)]

        couriers = []
        couriers.extend(self.bikes)
        couriers.extend(self.drones_default)
        couriers.extend(self.drones_type1)
        couriers.extend(self.drones_type2)
        couriers.extend(self.drones_type3)
        self.couriers = couriers

    def num_drones(self):
        return self.num_drones_type1 + self.num_drones_type2 + self.num_drones_type3 + self.num_drones_default

    def bikes(self):
        return [c for c in self.couriers if isinstance(c, Bike)]

    def drones(self):
        return [c for c in self.couriers if isinstance(c, Drone)]

    def next_courier_event(self):
        time_until_next_event_minutes = None
        courier_event = None
        for courier in self.couriers:
            if not courier.is_standby():
                if time_until_next_event_minutes is None or courier.time_to_destination() < time_until_next_event_minutes:
                    time_until_next_event_minutes = courier.time_to_destination()
                    courier_event = Event(from_courier(courier), time_until_next_event_minutes, courier)
        return courier_event
