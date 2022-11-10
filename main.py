from simulator.simulator import run_simulator
from utility.argparser import args
import random
# import test1 as ox
# This is a sample Python script.

if __name__ == '__main__':
    if not args.RNDM:
        random.seed(2223)
    
    run_simulator()
