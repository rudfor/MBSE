import sim_libs.gui.queue_graphics


class SimEnv:

    @staticmethod
    def sellers(canvas, config, x_top, y_top):
        return sim_libs.gui.queue_graphics.QueueGraphics("images/group.gif", 25, "Courier", config.SELLER_LINES, canvas, x_top, y_top)

    @staticmethod
    def scanners(canvas, config, x_top, y_top):
        return sim_libs.gui.queue_graphics.QueueGraphics("images/person-resized.gif", 18, "Delivered", config.SCANNER_LINES, canvas, x_top, y_top)
