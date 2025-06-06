# Configuration parameters
# Environment settings
env = {
    "size": 1.0,
    "resource_mode":"RATE", #RATE / CONSTANT
    "resource_energy": 4,
    "lambda_rate": 50,     # only relevant for RATE mode
    "resource_cap": 0      # only relevant for CONSTANT mode
}


# Simulation parameters
eta = 2**-4
sigma_s = 3.75e-4
sigma_a = 3.75e-4

size = 1.0
c_s = 160
c_a = 4

alpha = 4
beta = 1
delta = 1
delta_0 = 5e-3
K_b = 10
K_d = 1

# Initial agent settings
initial_agents = {
        "n_agents": 10000,
        "starting_energy": 10,
        "size": env["size"],
        "c_a": c_a,
        "c_s": c_s,
        "C": 0,                 # only relevant for SAME_COST mode
        "mode": "UNIFORM",          # SAME_COST / UNIFORM / DEFINED 
        "speed": 0,                 # only relevant for DEFINED mode
        "acuity": 0                 # only relevant for DEFINED mode    
    }
