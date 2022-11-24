#!/usr/bin/env python
from simulator.simulator import run_simulator
from utility.argparser import args
import random

if __name__ == '__main__':
    if not args.RNDM:
        random.seed(2223)
    
    run_simulator()
