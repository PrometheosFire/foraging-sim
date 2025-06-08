import time
import pandas as pd
import os
from evaluation.metrics import SimulationMetrics  # Your metrics class
import keyboard

def run_simulation(config, simulation, steps=1000, dt=0.1, save_prefix="evaluation/simulation_results/"):
    """
    Run simulation without visualization and save metrics data
    Args:
        simulation: Simulation object (must have step(), agents, and env.resources)
        steps: Number of steps to run
        dt: Time step size
        save_prefix: Prefix for output CSV files
    Returns:
        metrics: SimulationMetrics object with collected data
    """
    metrics = SimulationMetrics(config)
    start_time = time.time()
    elapsed = 0.0
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_prefix), exist_ok=True)
    
    step = 1
    inf = False
    if steps <= 0:
        print("Warning:Running indefinitely.")
        inf = True
    print("Press 'Q' to stop the simulation early.")

    print(f"Running simulation for {steps} steps (dt={dt})...")
    print(f"| {'Step':<6} | {'Agents':<7} | {'Resources':<9} | {'Time':<6} |")
    print("-" * 45)

    while (inf or step < steps + 1) and simulation.agents:
        if inf and keyboard.is_pressed('q'):
            print("\nQ pressed, exiting simulation loop.")
            break

        # Simulation step
        simulation.step(dt)
        
        # Progress reporting
        if step % 100 == 0 or step == steps - 1:
            # Collect data
            metrics.collect_agents(simulation.agents, step)
            elapsed = time.time() - start_time
            print(f"| {step:>6} | {len(simulation.agents):>7} | {len(simulation.env.resources):>9} | {elapsed:>6.1f} |")
        step += 1
    
    metrics.collect_resources(simulation.env.resources)
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    metrics.save_to_csv(
        f"{save_prefix}_agents_{timestamp}.csv",
        f"{save_prefix}_resources_{timestamp}.csv"
    )


    
    print(f"\nSimulation completed in {elapsed:.1f} seconds")
    print(f"Final agents: {len(simulation.agents)}, resources: {len(simulation.env.resources)}")
    print(f"Data saved to {save_prefix}_[agents|resources]_{timestamp}.csv")
    
    return metrics