# Configuration parameters
# Environment settings
env = {
    "size": 1.0,
    "resource_mode":"RATE", #RATE / CONSTANT
    "resource_energy": 4,
    "lambda_rate": 50,     # only relevant for RATE mode
    "resource_cap": 100,        # only relevant for CONSTANT mode
}



# Simulation parameters
eta = 2**-4
sigma_s = 0
sigma_a = 0


alpha = 4
beta = 1
delta = 1
delta_0 = 0.005
K_b = 10
K_d = 1

# Initial agent settings
initial_agents = {
        "n_agents": 50,
        "starting_energy": 10.0,
        "size": env["size"],
        "c_a": 4,
        "c_s": 160,
        "C": 1,
        "mode": "UNIFORM",         # SAME_COST / UNIFORM / DEFINED 
        "speed":0,
        "acuity":0
    }

