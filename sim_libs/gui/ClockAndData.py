import tkinter as tk


class ClockAndData:
    def __init__(self, canvas, x1, y1, x2, y2, time, data_plot, a1, a2, a3, avg_wait, seller_waits, scan_waits):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.train = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="#fff")
        self.time = canvas.create_text(self.x1 + 10, self.y1 + 10, text="Time = " + str(round(time, 1)) + "m",
                                       anchor=tk.NW)
        self.seller_wait = canvas.create_text(self.x1 + 10, self.y1 + 40,
                                              text="Avg. Seller Wait  = " + str(avg_wait(seller_waits)), anchor=tk.NW)
        self.scan_wait = canvas.create_text(self.x1 + 10, self.y1 + 70,
                                            text="Avg. Scanner Wait = " + str(avg_wait(scan_waits)), anchor=tk.NW)
        self.canvas.update()

    def tick(self, time):
        self.canvas.delete(self.time)
        self.canvas.delete(self.seller_wait)
        self.canvas.delete(self.scan_wait)

        self.time = self.canvas.create_text(self.x1 + 10, self.y1 + 10, text="Time = " + str(round(time, 1)) + "m",
                                       anchor=tk.NW)
        self.seller_wait = self.canvas.create_text(self.x1 + 10, self.y1 + 30,
                                              text="Avg. Seller Wait  = " + str(avg_wait(seller_waits)) + "m",
                                              anchor=tk.NW)
        self.scan_wait = self.canvas.create_text(self.x1 + 10, self.y1 + 50,
                                            text="Avg. Scanner Wait = " + str(avg_wait(scan_waits)) + "m", anchor=tk.NW)

        a1.cla()
        a1.set_xlabel("Time")
        a1.set_ylabel("Avg. Seller Wait (minutes)")
        a1.step([t for (t, waits) in seller_waits.items()], [np.mean(waits) for (t, waits) in seller_waits.items()])

        a2.cla()
        a2.set_xlabel("Time")
        a2.set_ylabel("Avg. Scanner Wait (minutes)")
        a2.step([t for (t, waits) in scan_waits.items()], [np.mean(waits) for (t, waits) in scan_waits.items()])

        a3.cla()
        a3.set_xlabel("Time")
        a3.set_ylabel("Arrivals")
        a3.bar([t for (t, a) in arrivals.items()], [a for (t, a) in arrivals.items()])

        data_plot.draw()
        self.canvas.update()