import time

def run_simulation(simulation, metrics, F, Lamb, MCsimulation, max_gen, dt=0.1):

    steps = 0
    start_time = time.time()
    gi_max = 0
    print(f"Running simulation for {steps} steps (dt={dt})...")
    print(f"| {'Step':<6} | {'Generation':<6} | {'Agents':<7} | {'Resources':<9} | {'Time':<6} |")
    print("-" * 54)

    while gi_max < max_gen and simulation.agents:
        # Simulation step
        gi_max = simulation.step(dt)
        steps += 1

        # Progress reporting
        if steps % 100 == 0 or gi_max >= max_gen or not simulation.agents:
            # Collect data
            elapsed = time.time() - start_time
            print(f"| {steps:>6} | {gi_max:>6} | {len(simulation.agents):>7} | {len(simulation.env.resources):>9} | {elapsed:>6.1f} |")

        if steps % 100 == 0 or gi_max >= max_gen or not simulation.agents:
            metrics.collect_agents(simulation.agents, F, Lamb, MCsimulation, steps)
    
    return metrics
