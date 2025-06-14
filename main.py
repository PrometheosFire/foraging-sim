import sys
import importlib
from sim.simulation import Simulation
from runners.pygame_visualizer import run_pygame

if __name__ == "__main__":
    if len(sys.argv) < 2:
        config_name = "Configs.base"
    else:
        config_name = sys.argv[1]

    config = importlib.import_module(config_name)

    sim_config = {
        "env": config.env,
        "initial_agents": config.initial_agents,
        "eta": config.eta,
        "sigma_s": config.sigma_s,
        "sigma_a": config.sigma_a,
        "alpha": config.alpha,
        "beta": config.beta,
        "delta": config.delta,
        "delta_0": config.delta_0,
        "K_b": config.K_b,
        "K_d": config.K_d
    }

    sim = Simulation(sim_config)
    # animate(sim, steps=2000, dt=0.1, interval=1)
    run_pygame(sim, steps=10000, initial_dt=0.1)
    #_ = run_simulation(sim_config, sim, steps=-1, dt=0.1)
