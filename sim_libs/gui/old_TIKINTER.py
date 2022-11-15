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

root = tk.Tk()
root.geometry("600x400")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

root.rowconfigure(1, weight=1)
logo = tk.PhotoImage(file ="images/LogoStudent.png")

#rectangle_1 = tk.Label(root, text="Rectangle 1", bg="green", fg="white")
title_bar = tk.Label(root, image = logo, bg = "#000007", height = 65, width = 1300)
title_bar.grid(column=0, row=0, columnspan=3, ipadx=20, ipady=20, sticky="NSEW")

# Title Label
canvas_order_log = tk.Label(root, text = "ScrolledText Widget Example", font = ("Times New Roman", 15), background = 'green', foreground = "white")
canvas_order_log.grid(column = 0, row = 1)

rectangle_2 = tk.Label(root, text="Rectangle 2", bg="red", fg="white")
rectangle_2.grid(column=0, row=2, ipadx=10, ipady=10, sticky="NSEW")

rectangle_3 = tk.Label(root, text="Rectangle 3", bg="blue", fg="white")
rectangle_3.grid(column=1, row=2, ipadx=10, ipady=10, sticky="NSEW")

#bus_log = BusLog(canvas_order_log, 5, 20)
#sellers = Sellers(canvas, 340, 20)
#scanners = Scanners(canvas, 770, 20)
#clock = ClockAndData(canvas, 1100, 260, 1290, 340, 0)


root.mainloop()