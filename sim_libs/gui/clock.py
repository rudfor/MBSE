import simpy

class Clock:

    def create_clock(env):
        """
            This generator is meant to be used as a SimPy event to update the clock
            and the data in the UI
        """
        while True:
            # yield env.timeout(0.1)
            yield env.timeout(1)
            clock.tick(env.now)