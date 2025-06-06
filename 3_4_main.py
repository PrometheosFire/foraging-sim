import sys
import importlib
import time
from sim.simulation import Simulation
from evaluation.metrics3_4 import SimulationMetrics
from graphics.dataLoader3_4 import run_simulation

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

    dt = 0.1

    MC_start = 0
    MC_simulations = 1
    env_param = ((50, 4, 400), (200, 1, 100), (800, .25, 50))  # (lambda_rate, resource_energy, max_gen)
    #max_gens = (20000, 500, 500)

    metrics = SimulationMetrics()
    start_time = time.time()
    for lambda_rate, F, max_gen in env_param:
        sim_config["env"]["lambda_rate"] = lambda_rate
        sim_config["env"]["resource_energy"] = F
        print(f"Running simulations for lambda_rate: {lambda_rate}, resource_energy: {F} max_gen: {max_gen}")

        env_time = time.time()
        for i in range(MC_start, MC_start+MC_simulations):
                sim = Simulation(sim_config)
                print(f"Running simulation {i+1}/{MC_simulations} with Max genetation={max_gen} for lambda_rate: {lambda_rate}, resource_energy: {F}")
                _ = run_simulation(sim, metrics, F, lambda_rate, i, max_gen=max_gen, dt=dt)

        env_time = time.time() - env_time
        print(f"Time taken for all simulations with lambda_rate: {lambda_rate} : {env_time:.2f} seconds")
   
    end_time = time.time()
    print(f"Total time taken for {MC_simulations * len(env_param)} simulations: {end_time - start_time:.2f} seconds")
    metrics.save_to_csv(f"evaluation/simulation_results/3_4_envParam{len(env_param)}_simulations{MC_start}-{MC_start + MC_simulations}.csv")
