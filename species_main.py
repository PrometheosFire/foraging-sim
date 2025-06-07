import sys
import importlib
import numpy as np
from sim.simulation import Simulation
from evaluation.metrics_species import SimulationMetrics
from graphics.dataLoader_species import run_simulation

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

    max_steps = 1000
    n_runs = 10
    dt = 0.1
    env_param = ((12.5, 16), (100, 2), (400, .5))  # (lambda_rate, resource_energy)
    metrics = SimulationMetrics()

    for lambda_rate, F in env_param:
        for i in range(n_runs):
            sim_config["env"]["lambda_rate"] = lambda_rate
            sim_config["env"]["resource_energy"] = F
            print(f"Running simulation {i} for lambda_rate: {lambda_rate}, resource_energy: {F}")
            sim = Simulation(sim_config)
            _ = run_simulation(sim, metrics, lambda_rate, F, steps=max_steps, dt=dt)

    metrics.save_to_csv(f"evaluation/simulation_results/speciesResults.csv")
