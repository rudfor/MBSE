#!/usr/bin/env python
import sim_libs
import simpy

if __name__ == '__main__':
    env = simpy.Environment()
    res = simpy.Resource(env, capacity=1)
    drone = env.process(sim_libs.resource_drone(env, res))
    procs = [env.process(sim_libs.drone(res)), env.process(sim_libs.drone(res))]
    env.run(40)
    #sim_libs.simulator.Simulator(1)
    #simulator.RUN()
    #run_simulator()
