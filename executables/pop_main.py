import sys
import importlib
import numpy as np
from sim.simulation import Simulation
from evaluation.popMetrics import SimulationMetrics
from graphics.dataLoader3_1 import run_simulation

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <config_module>")
        sys.exit(1)

    config_name = sys.argv[1]
    config = importlib.import_module(config_name)

    sim_config = {
        "env": config.env,
        "initial_agents": config.initial_agents,
        "eta": config.eta,
        "c_s": config.c_s,
        "c_a": config.c_a,
        "sigma_s": config.sigma_s,
        "sigma_a": config.sigma_a,
        "alpha": config.alpha,
        "beta": config.beta,
        "delta": config.delta,
        "delta_0": config.delta_0,
        "K_b": config.K_b,
        "K_d": config.K_d
    }

    max_steps = 10000
    dt = 0.1
    max_acuity = 0.1
    max_speed = 0.1
    phenotype_step = 0.01

    metrics = SimulationMetrics()

    acuity = sim_config["initial_agents"]["acuity"]
    speed = sim_config["initial_agents"]["speed"] 
   
    sim = Simulation(sim_config)
    print(f"Running simulation with acuity={acuity}, speed={speed}...")
    _ = run_simulation(sim, metrics, steps=max_steps, dt=dt)

    metrics.save_to_csv(f"evaluation/simulation_results/pop_{acuity}_{speed}.csv")
