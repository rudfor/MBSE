from collections import defaultdict
import tkinter as tk


class BusLog:
    TEXT_HEIGHT = 20

    def __init__(self, canvas, x_top, y_top):
        self.canvas = canvas
        self.x_top = x_top
        self.y_top = y_top
        self.bus_count = 0

    def next_bus(self, minutes):
        x = self.x_top
        y = self.y_top + (self.bus_count * self.TEXT_HEIGHT)
        self.canvas.create_text(x, y, anchor=tk.SW, text=f"Order in {round(minutes, 1)} m")
        # self.bus_count = self.bus_count + 1
        self.canvas.update()
        self.canvas.yview_moveto( y )

    def bus_arrived(self, people):
        x = self.x_top + 135
        y = self.y_top + (self.bus_count * self.TEXT_HEIGHT)
        self.canvas.create_text(x, y, anchor=tk.SW, text=f"Order for {people} people", fill="green")
        self.bus_count = self.bus_count + 1
        self.canvas.update()
        self.canvas.yview_moveto( y )
