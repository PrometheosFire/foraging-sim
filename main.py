from sim.simulation import Simulation
from graphics.visualizer import animate
from graphics.pygame_visualizer import run_pygame
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
    "alpha": config.alpha,
    "beta": config.beta,
    "delta": config.delta,
    "delta_0": config.delta_0,
    "K_b": config.K_b,
    "K_d": config.K_d
}

    sim = Simulation(sim_config)
    #animate(sim, steps=2000, dt=0.1, interval=1)
    run_pygame(sim, steps=10000, dt=0.1)