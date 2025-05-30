from sim.simulation import Simulation
from graphics.visualizer import animate
import config # or define config inline

if __name__ == "__main__":
    sim_config = {
    "env": config.env,
    "initial_agents": config.initial_agents,
    "eta": config.eta,
    "c_s": config.c_s,
    "c_a": config.c_a,
    "sigma_s": config.sigma_s,
    "sigma_a": config.sigma_a,
    "E_birth_threshold": config.E_birth_threshold
}

    sim = Simulation(sim_config)
    animate(sim, steps=200, dt=0.1, interval=10)