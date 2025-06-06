# Configuration parameters
# Environment settings
env = {
    "size": 1.0,
    "resource_mode":"CONSTANT", #RATE / CONSTANT
    "resource_energy": 4,
    "lambda_rate": 200,     # only relevant for RATE mode
    "resource_cap":10      # only relevant for CONSTANT mode
}



# Simulation parameters
eta = 2**-4
sigma_s = 0
sigma_a = 0

size = 1.0
c_s = 160
c_a = 4

alpha = 4
beta = 1
delta = 0
delta_0 = 0
K_b = 10
K_d = 1

# Initial agent settings
initial_agents = {
        "n_agents": 1,
        "starting_energy": 0,
        "size": env["size"],
        "c_a": c_a,
        "c_s": c_s,
        "C": 1,
        "mode": "DEFINED",
        "speed": 0.1,
        "acuity": 0.1
    }
