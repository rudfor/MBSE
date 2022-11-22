#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Rudolf Anton Fortes
ported from author:
@author: kevin
"""
import simpy
import json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import tkinter as tk
import sim_libs.gui.status as status
from sim_libs.gui.bus import BusLog as BusLog
from sim_libs.gui.orders import OrdersLog as OrdersLog
from sim_libs.gui.orders import Orders as Orders
from sim_libs.gui.config import Config as Config
from sim_libs.gui.clock_and_data import ClockAndData as ClockAndData
from sim_libs.gui.sim_env import SimEnv as SimEnv
from sim_libs.gui.bus import Bus as Bus


#from PIL import ImageTk

# -------------------------
#  CONFIGURATION
# -------------------------

config=Config(seed=42)

# -------------------------
#  ANALYTICAL GLOBALS
# -------------------------

stat = status.Status()

# -------------------------
#  UI/ANIMATION 
# -------------------------

main = tk.Tk()
main.geometry("1300x750")
main.columnconfigure(0, weight=5)
main.columnconfigure(1, weight=2)
main.columnconfigure(2, weight=2)
main.columnconfigure(3, weight=2)
main.columnconfigure(4, weight=2)

main.rowconfigure(0, weight=1)
main.rowconfigure(1, weight=1)
main.rowconfigure(2, weight=1)
main.rowconfigure(3, weight=1)
logo = tk.PhotoImage(file ="images/LogoStudent.png")

main.title("Drone vs Bike Simulation")
main.config(bg="#fff")
#rectangle_1 = tk.Label(root, text="Rectangle 1", bg="green", fg="white")
title_bar = tk.Label(main, image = logo, bg = "#000007", height = 65, width = 1300)
title_bar.grid(column=0, row=0, columnspan=5, ipadx=20, ipady=20, sticky="NSEW")
#top_frame = tk.Frame(main)
#tk.Label(top_frame, image = logo, bg = "#000007", height = 100, width = 1300)
#top_frame.grid(column=0, row=0, columnspan=4, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")
# SETUP SCROLLBAR:
order_frame = tk.Frame(main, bg='lightgray', bd=2, relief=tk.FLAT, width = 200, height=800)
order_frame.grid(column=0, rowspan=3, row=1, sticky=tk.NW)

canvas_01 = tk.Canvas(order_frame, bg="lightblue")
canvas_01.grid(column=1, row=0)
vsbar = tk.Scrollbar(order_frame, orient=tk.VERTICAL, command=canvas_01.yview)
vsbar.grid(row=0, column=0, sticky=tk.NS)

bbox = canvas_01.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

# Define the scrollable region as entire canvas with only the desired
# number of rows and columns displayed.
#w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
#dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
canvas_01.configure(scrollregion=bbox, width=200, height=800)

canvas_01.configure(yscrollcommand=vsbar.set)

canvas_02 = tk.Canvas(main, width = 300, height = 450, bg = "lightgreen")
canvas_02.grid(column=2, row=1, columnspan=1, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")
canvas_03 = tk.Canvas(main, width = 300, height = 450, bg = "lightgray")
canvas_03.grid(column=3, row=1, columnspan=1, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")

order_frame = tk.Frame(main, width=300, height=450)

canvas_1 = tk.Canvas(order_frame, width = 300, height = 450, bg = "lightgray")
canvas_1.pack(side=tk.LEFT, expand = False)
vbar=tk.Scrollbar(canvas_1, orient=tk.VERTICAL)
vbar.config(command=canvas_1.yview)
#canvas_1.config(width=300, height=450)
canvas_1.config(yscrollcommand=vbar.set)
canvas_2 = tk.Canvas(main, width = 300, height = 450, bg = "lightblue")
canvas_3 = tk.Canvas(main, width = 300, height = 450, bg = "lightgreen")
canvas_4 = tk.Canvas(main, width = 300, height = 450, bg = "green")

order_frame.grid(column=1, row=2, columnspan=1, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")
canvas_2.grid(column=2, row=2, columnspan=1, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")
canvas_3.grid(column=3, row=2, columnspan=1, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")
canvas_4.grid(column=4, row=2, columnspan=1, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")

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
data_plot.get_tk_widget().grid(column=1, row=3, columnspan=4, rowspan=1, ipadx=20, ipady=20, sticky="NSEW")

order_log = OrdersLog(canvas_01, 5, 20)
sellers2 = SimEnv.sellers(canvas_02, config, 5, 20)
scanners2 = SimEnv.scanners(canvas_03, config, 5, 20)


bus_log = BusLog(canvas_1, 5, 20)
sellers = SimEnv.sellers(canvas_2, config, 5, 20)
scanners = SimEnv.scanners(canvas_3, config, 5, 20)
clock = ClockAndData(canvas_4, stat, 5, 20, 24, 80, 0)
# clock2 = ClockAndData2(canvas_4, 5, 20, 24, 80, 0)
# clock = sim_libs.gui.ClockAndData.ClockAndData(canvas, 1100, 260, 1290, 340, 0, data_plot, a1, a2, a3, avg_wait, seller_waits, scan_waits)

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
        clock.tick(env.now, stat, a1, a2, a3, data_plot)


env = simpy.rt.RealtimeEnvironment(factor = 0.1, strict = False)
#env = simpy.Environment()

seller_lines = [ simpy.Resource(env, capacity = config.SELLERS_PER_LINE) for _ in range(config.SELLER_LINES) ]
scanner_lines = [ simpy.Resource(env, capacity = config.SCANNERS_PER_LINE) for _ in range(config.SCANNER_LINES) ]

env.process(Bus.bus_arrival(env, stat, config, bus_log, sellers, scanners, seller_lines, scanner_lines))
#env.process(bus_arrival(env, seller_lines, scanner_lines))
env.process(Orders.order_arrival(env, stat, config, order_log, sellers2, scanners2, seller_lines, scanner_lines))
env.process(create_clock(env))
env.run(until = 100)

main.mainloop()

with open('output/events.json', 'w') as outfile:
    json.dump({
        "sellerLines": config.SELLER_LINES,
        "scannerLines": config.SCANNER_LINES,
        "events": stat.event_log
    }, outfile)