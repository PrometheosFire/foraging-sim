import time
import pandas as pd


def run_simulation(simulation, metrics, steps=1000, dt=0.1):


    start_time = time.time()
    print(f"Running simulation for {steps} steps (dt={dt})...")
    print(f"| {'Step':<6} | {'Agents':<7} | {'Resources':<9} | {'Time':<6} |")
    print("-" * 45)

    for step in range(steps):
        # Simulation step
        simulation.step(dt)

        # Progress reporting
        if step % 100 == 0 or step == steps - 1:
            # Collect data
            elapsed = time.time() - start_time
            print(f"| {step:>6} | {len(simulation.agents):>7} | {len(simulation.env.resources):>9} | {elapsed:>6.1f} |")
        
        metrics.collect_agents(simulation.agents, step)
        # Collect data
    

    return metrics
