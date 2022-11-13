import tkinter as tk
from collections import defaultdict


class QueueGraphics:
    text_height = 30
    icon_top_margin = -8

    def __init__(self, icon_file, icon_width, queue_name, num_lines, canvas, x_top, y_top):
        self.icon_file = icon_file
        self.icon_width = icon_width
        self.queue_name = queue_name
        self.num_lines = num_lines
        self.canvas = canvas
        self.x_top = x_top
        self.y_top = y_top

        self.image = tk.PhotoImage(file=self.icon_file)
        self.icons = defaultdict(lambda: [])
        for i in range(num_lines):
            canvas.create_text(x_top, y_top + (i * self.text_height), anchor=tk.NW, text=f"{queue_name} #{i + 1}")
        self.canvas.update()

    def add_to_line(self, seller_number):
        count = len(self.icons[seller_number])
        x = self.x_top + 60 + (count * self.icon_width)
        y = self.y_top + ((seller_number - 1) * self.text_height) + self.icon_top_margin
        self.icons[seller_number].append(
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.image)
        )
        self.canvas.update()

    def remove_from_line(self, seller_number):
        if len(self.icons[seller_number]) == 0: return
        to_del = self.icons[seller_number].pop()
        self.canvas.delete(to_del)
        self.canvas.update()