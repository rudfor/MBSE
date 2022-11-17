#!/usr/bin/env python
from simulator.simulator import run_simulator
from utility.argparser import args
import random
import sim_libs as sim_lib

if __name__ == '__main__':

    if not args.RNDM:
        random.seed(args.SEED)
    
    run_simulator()
