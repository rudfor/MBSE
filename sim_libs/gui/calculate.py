import numpy as np
import random

class Calc:
    @staticmethod
    def avg_wait(raw_waits):
        waits = [ w for i in raw_waits.values() for w in i ]
        return round(np.mean(waits), 1) if len(waits) > 0 else 0

    @staticmethod
    def pick_shortest(lines):
        """
            Given a list of SimPy resources, determine the one with the shortest queue.
            Returns a tuple where the 0th element is the shortest line (a SimPy resource),
            and the 1st element is the line # (1-indexed)

            Note that the line order is shuffled so that the first queue is not disproportionally selected
        """
        shuffled = list(zip(range(len(lines)), lines)) # tuples of (i, line)
        random.shuffle(shuffled)
        shortest = shuffled[0][0]
        for i, line in shuffled:
            if len(line.queue) < len(lines[shortest].queue):
                shortest = i
                break
        return (lines[shortest], shortest + 1)