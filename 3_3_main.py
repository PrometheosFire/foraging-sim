import sys
import importlib
import time
from sim.simulation import Simulation
from evaluation.metrics3_3 import SimulationMetrics
from graphics.dataLoader3_3 import run_simulation

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

    max_steps = 2000
    dt = 0.1

    MC_simulations = 10
    env_param = ((12.5, 16),)
    metabolic_cost = (2**-6,)
    metrics = SimulationMetrics()
    start_time = time.time()
    for param in env_param:
        lambda_rate = param[0]
        F = param[1]
        sim_config["env"]["lambda_rate"] = lambda_rate
        sim_config["env"]["resource_energy"] = F
        print(f"Running simulations for lambda_rate: {lambda_rate}, resource_energy: {F}")

        env_time = time.time()
        for c in metabolic_cost:
            sim_config["initial_agents"]["C"] = c
            print(f"Running simulations for metabolic cost: {c} for lambda_rate: {param[0]}, resource_energy: {param[1]}")

            cost_time = time.time()
            for i in range(MC_simulations):
                sim = Simulation(sim_config)
                print(f"Running simulation {i+1}/{MC_simulations} with C={c} for lambda_rate: {param[0]}, resource_energy: {param[1]}")
                _ = run_simulation(sim, metrics, F, lambda_rate, i, steps=max_steps, dt=dt)

            cost_time = time.time() - cost_time
            print(f"Time taken for {MC_simulations} simulations with C={c} : {cost_time:.2f} seconds")

        env_time = time.time() - env_time
        print(f"Time taken for all simulations with lambda_rate: {lambda_rate} : {env_time:.2f} seconds")


    end_time = time.time()
    print(f"Total time taken for {MC_simulations * len(env_param) * len(metabolic_cost)} simulations: {end_time - start_time:.2f} seconds")
       

    metrics.save_to_csv(f"evaluation/simulation_results/3_3_envParam{len(env_param)}_cost{len(metabolic_cost)}_simulations{MC_simulations}.csv")
