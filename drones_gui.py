#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Rudolf Anton Fortes
ported from author:
@author: kevin
"""

import itertools
from collections import defaultdict
import random
import numpy as np
import pandas as pd
import math
import time
import simpy
import json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import tkinter as tk
import sim_libs.gui.queue_graphics
import sim_libs.gui.status as status
from sim_libs.gui.calculate import Calc as calc
from sim_libs.gui.bus import BusLog as BusLog

from PIL import ImageTk

# -------------------------
#  CONFIGURATION
# -------------------------

BUS_ARRIVAL_MEAN = 3
BUS_OCCUPANCY_MEAN = 100
BUS_OCCUPANCY_STD = 30

PURCHASE_RATIO_MEAN = 0.4
PURCHASE_GROUP_SIZE_MEAN = 2.25
PURCHASE_GROUP_SIZE_STD = 0.50

TIME_TO_WALK_TO_SELLERS_MEAN = 1
TIME_TO_WALK_TO_SELLERS_STD = 0.25
TIME_TO_WALK_TO_SCANNERS_MEAN = 0.5
TIME_TO_WALK_TO_SCANNERS_STD = 0.1

SELLER_LINES = 10
SELLERS_PER_LINE = 1
SELLER_MEAN = 1
SELLER_STD = 0.2

SCANNER_LINES = 4
SCANNERS_PER_LINE = 1
SCANNER_MEAN = 1 / 20
SCANNER_STD = 0.01

# Let's pre-generate all the bus arrival times and their occupancies so that even if we
# change the configuration, we'll have consistent arrivals
random.seed(42)
ARRIVALS = [ random.expovariate(1 / BUS_ARRIVAL_MEAN) for _ in range(40) ]
#ARRIVALS = [ random.weibullvariate(1, BUS_ARRIVAL_MEAN) ]
ON_BOARD = [ int(random.gauss(BUS_OCCUPANCY_MEAN, BUS_OCCUPANCY_STD)) for _ in range(40) ]

# -------------------------
#  ANALYTICAL GLOBALS
# -------------------------

stat = status.Status()

# -------------------------
#  UI/ANIMATION 
# -------------------------

main = tk.Tk()
main.geometry("1300x750")
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=2)

main.rowconfigure(1, weight=1)

main.title("Drone vs Bike Simulation")
main.config(bg="#fff")
logo = tk.PhotoImage(file ="images/LogoStudent.png")
top_frame = tk.Frame(main)
tk.Label(top_frame, image = logo, bg = "#000007", height = 100, width = 1300)
top_frame.grid(column=0, row=0, columnspan=4, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")

order_frame = tk.Frame(main, width=300, height=450)

canvas_1 = tk.Canvas(order_frame, width = 300, height = 450, bg = "lightgray")
canvas_1.pack(side=tk.LEFT, expand = False)
vbar=tk.Scrollbar(order_frame, orient=tk.VERTICAL)

vbar.config(command=canvas_1.yview)
canvas_1.config(width=300, height=450)
canvas_1.config(yscrollcommand=vbar.set)

canvas_2 = tk.Canvas(main, width = 300, height = 450, bg = "lightblue")
#canvas_2.pack(side=tk.LEFT, expand = False, anchor=tk.E)
canvas_3 = tk.Canvas(main, width = 300, height = 450, bg = "lightgreen")
#canvas_3.pack(side=tk.LEFT, expand = False)
canvas_4 = tk.Canvas(main, width = 300, height = 450, bg = "green")
#canvas_4.pack(side=tk.LEFT, expand = False)

order_frame.grid(column=0, row=1, columnspan=1, rowspan=1, ipadx=20, ipady=20)
canvas_2.grid(column=1, row=1, columnspan=1, rowspan=1, ipadx=20, ipady=20)
canvas_3.grid(column=2, row=1, columnspan=1, rowspan=1, ipadx=20, ipady=20)
canvas_4.grid(column=2, row=1, columnspan=1, rowspan=1, ipadx=20, ipady=20)

#canvas4.pack(side=tk.TOP, expand = False)
#canvas = tk.Canvas(main, width = 1000, height = 450, bg = "white")
#canvas.pack(side=tk.TOP, expand = False)

f = plt.Figure(figsize=(2, 2), dpi=72)
a3 = f.add_subplot(121)
a3.plot()
a1 = f.add_subplot(222)
a1.plot()
a2 = f.add_subplot(224)
a2.plot()
data_plot = FigureCanvasTkAgg(f, master=main)
data_plot.get_tk_widget().config(height = 400)

#.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
data_plot.get_tk_widget().grid(column=0, row=2, columnspan=4, rowspan=1, ipadx=20, ipady=20)

def Sellers(tmp_canvas, x_top, y_top):
    return sim_libs.gui.queue_graphics.QueueGraphics("images/group.gif", 25, "Courier", SELLER_LINES, tmp_canvas, x_top, y_top)


def Scanners(tmp_canvas, x_top, y_top):
    return sim_libs.gui.queue_graphics.QueueGraphics("images/person-resized.gif", 18, "Delivered", SCANNER_LINES, tmp_canvas, x_top, y_top)


class ClockAndData:
    def __init__(self, canvas, x1, y1, x2, y2, time):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.train = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="#fff")
        self.time = self.canvas.create_text(self.x1 + 10, self.y1 + 10, text = "Time = "+str(round(time, 1))+"m", anchor = tk.NW)
        self.seller_wait = self.canvas.create_text(self.x1 + 10, self.y1 + 40, text = "Avg. Seller Wait  = "+str(calc.avg_wait(stat.seller_waits)), anchor = tk.NW)
        self.scan_wait = self.canvas.create_text(self.x1 + 10, self.y1 + 70, text = "Avg. Scanner Wait = "+str(calc.avg_wait(stat.scan_waits)), anchor = tk.NW)
        self.canvas.update()

    def tick(self, time):
        self.canvas.delete(self.time)
        self.canvas.delete(self.seller_wait)
        self.canvas.delete(self.scan_wait)

        self.time = self.canvas.create_text(self.x1 + 10, self.y1 + 10, text = "Time = "+str(round(time, 1))+"m", anchor = tk.NW)
        self.seller_wait = self.canvas.create_text(self.x1 + 10, self.y1 + 30, text = "Avg. Seller Wait  = "+str(calc.avg_wait(stat.seller_waits))+"m", anchor = tk.NW)
        self.scan_wait = self.canvas.create_text(self.x1 + 10, self.y1 + 50, text = "Avg. Scanner Wait = "+str(calc.avg_wait(stat.scan_waits))+"m", anchor = tk.NW)

        a1.cla()
        a1.set_xlabel("Time")
        a1.set_ylabel("Avg. Seller Wait (minutes)")
        a1.step([ t for (t, waits) in stat.seller_waits.items() ], [ np.mean(waits) for (t, waits) in stat.seller_waits.items() ])

        a2.cla()
        a2.set_xlabel("Time")
        a2.set_ylabel("Avg. Scanner Wait (minutes)")
        a2.step([ t for (t, waits) in stat.scan_waits.items() ], [ np.mean(waits) for (t, waits) in stat.scan_waits.items() ])

        a3.cla()
        a3.set_xlabel("Time")
        a3.set_ylabel("Arrivals")
        a3.bar([ t for (t, a) in stat.arrivals.items() ], [ a for (t, a) in stat.arrivals.items() ])

        data_plot.draw()
        self.canvas.update()

bus_log = BusLog(canvas_1, 5, 20)
sellers = Sellers(canvas_2, 5, 20)
scanners = Scanners(canvas_3, 5, 20)
clock = ClockAndData(canvas_4, 5, 20, 24, 80, 0)
#clock = sim_libs.gui.ClockAndData.ClockAndData(canvas, 1100, 260, 1290, 340, 0, data_plot, a1, a2, a3, avg_wait, seller_waits, scan_waits)

# -------------------------
#  SIMULATION
# -------------------------

def create_clock(env):
    """
        This generator is meant to be used as a SimPy event to update the clock
        and the data in the UI
    """
    while True:
#        yield env.timeout(0.1)
        yield env.timeout(1)
        clock.tick(env.now)


def bus_arrival(env, seller_lines, scanner_lines):
    """
        Simulate a bus arriving every BUS_ARRIVAL_MEAN minutes with 
        BUS_OCCUPANCY_MEAN people on board

        This is the top-level SimPy event for the simulation: all other events
        originate from a bus arriving
    """
    # Note that these unique IDs for busses and people are not required, but are included for eventual visualizations 
    next_bus_id = 0
    next_person_id = 0
    while True:
        # next_bus = random.expovariate(1 / BUS_ARRIVAL_MEAN)        
        # on_board = int(random.gauss(BUS_OCCUPANCY_MEAN, BUS_OCCUPANCY_STD))
        next_bus = ARRIVALS.pop()
        on_board = ON_BOARD.pop()

        # Wait for the bus
        bus_log.next_bus(next_bus)
        yield env.timeout(next_bus)
        bus_log.bus_arrived(on_board)

        # register_bus_arrival() below is for reporting purposes only
        people_ids = list(range(next_person_id, next_person_id + on_board))
        stat.register_bus_arrival(env.now, next_bus_id, people_ids)
        next_person_id += on_board
        next_bus_id += 1

        while len(people_ids) > 0:
            remaining = len(people_ids)
            group_size = min(round(random.gauss(PURCHASE_GROUP_SIZE_MEAN, PURCHASE_GROUP_SIZE_STD)), remaining)
            people_processed = people_ids[-group_size:] # Grab the last `group_size` elements
            people_ids = people_ids[:-group_size] # Reset people_ids to only those remaining

            # Randomly determine if this group is going to the sellers or straight to the scanners
            if random.random() > PURCHASE_RATIO_MEAN:
                env.process(scanning_customer(env, people_processed, scanner_lines, TIME_TO_WALK_TO_SELLERS_MEAN + TIME_TO_WALK_TO_SCANNERS_MEAN, TIME_TO_WALK_TO_SELLERS_STD + TIME_TO_WALK_TO_SCANNERS_STD))
            else:
                env.process(purchasing_customer(env, people_processed, seller_lines, scanner_lines))

def purchasing_customer(env, people_processed, seller_lines, scanner_lines):
    walk_begin = env.now
    yield env.timeout(random.gauss(TIME_TO_WALK_TO_SELLERS_MEAN, TIME_TO_WALK_TO_SELLERS_STD))
    walk_end = env.now

    queue_begin = env.now
    seller_line = calc.pick_shortest(seller_lines)
    with seller_line[0].request() as req:
        # Wait in line
        sellers.add_to_line(seller_line[1])
        yield req
        sellers.remove_from_line(seller_line[1])
        queue_end = env.now

        # Buy tickets
        sale_begin = env.now
        yield env.timeout(random.gauss(SELLER_MEAN, SELLER_STD))
        sale_end = env.now

        stat.register_group_moving_from_bus_to_seller(people_processed, walk_begin, walk_end, seller_line[1], queue_begin, queue_end, sale_begin, sale_end)
        
        env.process(scanning_customer(env, people_processed, scanner_lines, TIME_TO_WALK_TO_SCANNERS_MEAN, TIME_TO_WALK_TO_SCANNERS_STD))

def scanning_customer(env, people_processed, scanner_lines, walk_duration, walk_std):
    # Walk to the seller 
    walk_begin = env.now
    yield env.timeout(random.gauss(walk_duration, walk_std))
    walk_end = env.now

    # We assume that the visitor will always pick the shortest line
    queue_begin = env.now    
    scanner_line = calc.pick_shortest(scanner_lines)
    with scanner_line[0].request() as req:
        # Wait in line
        for _ in people_processed: scanners.add_to_line(scanner_line[1])
        yield req
        for _ in people_processed: scanners.remove_from_line(scanner_line[1])
        queue_end = env.now

        # Scan each person's tickets 
        for person in people_processed:
            scan_begin = env.now
            yield env.timeout(random.gauss(SCANNER_MEAN, SCANNER_STD)) # Scan their ticket
            scan_end = env.now
            stat.register_visitor_moving_to_scanner(person, walk_begin, walk_end, scanner_line[1], queue_begin, queue_end, scan_begin, scan_end)


env = simpy.rt.RealtimeEnvironment(factor = 0.1, strict = False)
#env = simpy.Environment()

seller_lines = [ simpy.Resource(env, capacity = SELLERS_PER_LINE) for _ in range(SELLER_LINES) ]
scanner_lines = [ simpy.Resource(env, capacity = SCANNERS_PER_LINE) for _ in range(SCANNER_LINES) ]

env.process(bus_arrival(env, seller_lines, scanner_lines))
env.process(create_clock(env))
env.run(until = 100)

main.mainloop()

with open('output/events.json', 'w') as outfile:
    json.dump({
        "sellerLines": SELLER_LINES,
        "scannerLines": SCANNER_LINES,
        "events": stat.event_log
    }, outfile)