import argparse

parser = argparse.ArgumentParser(
    prog="MBSE Simulator",
    description="Simulates whether bicycles, drones or a hybrid model are the most efficient for food delivery."
)
parser.add_argument("--plot", action="store_true", default=False, dest="PLOT", help="Turn on plotting (default: False)")
parser.add_argument("--bike-hour-cost", type=int, default=150, dest="BIKE_HOUR_COST", help="default: 150 DKK")
parser.add_argument("--bike-avg-speed", type=int, default=180, dest="BIKE_AVG_SPEED", help="default: 180 m/min")
parser.add_argument("--drone-cost", type=int, default=40000, dest="DRONE_COST", help="default: 40000 DKK")
parser.add_argument("--drone-flight-time", type=int, default=50, dest="DRONE_FLIGHT_TIME", help="default: 50 min")
parser.add_argument("--drone-battery-capacity", type=int, default=50, dest="DRONE_BAT_CAP", help="default: 50")
parser.add_argument("--drone-range", type=int, default=4000, dest="DRONE_RANGE", help="default: 4000 m")
parser.add_argument("--drone-charge-time", type=int, default=60, dest="DRONE_CHARGE_TIME", help="default: 60 min")
parser.add_argument("--drone-avg-speed", type=int, default=15, dest="DRONE_AVG_SPEED", help="default: 15 m/s")
parser.add_argument("--drone-weight-limit", type=int, default=8, dest="DRONE_WEIGHT_LIMIT", help="default: 8 kg")

args = parser.parse_args()