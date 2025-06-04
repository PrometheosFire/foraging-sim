import sys
import importlib
import numpy as np
from sim.simulation import Simulation
from evaluation.metrics3_1 import SimulationMetrics
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

    max_steps = 100
    dt = 0.1
    max_acuity = 0.2
    max_speed = 0.2
    phenotype_step = 0.01

    rate = sim_config["env"]["resource_cap"]

    metrics = SimulationMetrics(rate)

    for acuity in np.arange(0, max_acuity, phenotype_step):
            for speed in np.arange(0, max_speed, phenotype_step):
                sim_config["initial_agents"]["acuity"] = acuity
                sim_config["initial_agents"]["speed"] = speed
                sim = Simulation(sim_config)
                _ = run_simulation(sim, metrics, steps=max_steps, dt=dt)

    metrics.save_to_csv(f"evaluation/simulation_results/3_1Rate{rate}.csv")
