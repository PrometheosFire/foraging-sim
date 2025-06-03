# Configuration parameters
# Environment settings
env = {
    "size": 1.0,
    "lambda_rate": 400,
    "resource_energy": 0.5
}



# Simulation parameters
eta = 0.1
sigma_s = 0
sigma_a = 0

size = 1.0
lambda_rate = 100
resource_energy = 1.0
eta = 0.1
c_s = 160
c_a = 4

alpha = 4
beta = 1
delta = 1
delta_0 = 0.005
K_b = 10
K_d = 1

# Initial agent settings
initial_agents = {
        "n_agents": 1000,
        "starting_energy": 10.0,
        "size": env["size"],
        "c_a": c_a,
        "c_s": c_s,
        "C": 1,
        "mode": "SAME_COST"
    }

