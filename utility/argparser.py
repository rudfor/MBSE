import argparse

parser = argparse.ArgumentParser(
    prog="MBSE Simulator",
    description=
"""Simulates whether bicycles, drones or a hybrid model are the most efficient for food delivery.

The configuration options (--drone-*) for the drones will apply to the DefaultDrone and replace initial values with the provided values.
DroneType1, DroneType2, and DroneType3 are all preconfigured drones with different configurations.""",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-p", "--plot", action="store_true", default=False, dest="PLOT", help="Turn on plotting (default: False)")
parser.add_argument("-b", "--bikes", type=int, default=3, dest="NUM_BIKES", help="Number of Bikes (default: 3)")
parser.add_argument("--defaultdrones", type=int, default=1, dest="NUM_DD", help="Number of DefaultDrone (default: 1)")
parser.add_argument("--dronetype1", type=int, default=0, dest="NUM_DT1", help="Number of DroneType1 (default: 0)")
parser.add_argument("--dronetype2", type=int, default=0, dest="NUM_DT2", help="Number of DroneType2 (default: 0)")
parser.add_argument("--dronetype3", type=int, default=0, dest="NUM_DT3", help="Number of DroneType3 (default: 0)")
parser.add_argument("--bike-hour-cost", type=int, default=150, dest="BIKE_HOUR_COST", help="default: 150 DKK")
parser.add_argument("--bike-avg-speed", type=int, default=180, dest="BIKE_AVG_SPEED", help="default: 180 m/min")
parser.add_argument("--drone-cost", type=int, default=40000, dest="DRONE_COST", help="default: 40000 DKK")
parser.add_argument("--drone-flight-time", type=int, default=50, dest="DRONE_FLIGHT_TIME", help="default: 50 min")
parser.add_argument("--drone-battery-capacity", type=int, default=50, dest="DRONE_BAT_CAP", help="default: 50")
parser.add_argument("--drone-range", type=int, default=4000, dest="DRONE_RANGE", help="default: 4000 m")
parser.add_argument("--drone-charge-time", type=int, default=60, dest="DRONE_CHARGE_TIME", help="default: 60 min")
parser.add_argument("--drone-avg-speed", type=int, default=6 / 2 * 60, dest="DRONE_AVG_SPEED", help="default: 3 m/s")
parser.add_argument("--drone-weight-limit", type=int, default=8, dest="DRONE_WEIGHT_LIMIT", help="default: 8 kg")
parser.add_argument("-r", "--random", action="store_true", default=False, dest="RNDM", help="Choose a random seed (default: False)")
parser.add_argument("-t", "--time", type=int, default=300, dest="TIME", help="Timeframe in minutes (default: 300)")
parser.add_argument("-s", "--seed", type=int, default=2223, dest="SEED", help="Choose a custom seed (default: 2223)")
parser.add_argument("--breakdown-rate", type=float, default=0.01, dest="BREAKDOWN_RATE", help="Rate of bike breakdown per order delivery")
parser.add_argument("--interarrival-time", type=float, default=10, dest="BASE_ORDER_INTERARRIVAL_TIME", help="Order interarrival time (default: 30 min)")
parser.add_argument("--log", action="store_true", default=False, dest="LOG", help="(default: False)")

args = parser.parse_args()