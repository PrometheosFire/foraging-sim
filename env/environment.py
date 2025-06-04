import numpy as np

class Environment:
    def __init__(self, size=1.0, lambda_rate=100, resource_energy=1.0, resource_mode="RATE", resource_cap=0):
        self.size = size
        self.lambda_rate = lambda_rate
        self.resource_energy = resource_energy
        self.resources = []
        self.resource_mode = resource_mode
        self.resource_cap = resource_cap

    def spawn_resources(self, dt):
        if self.resource_mode == "RATE":
            to_spawn = np.random.poisson(self.lambda_rate * dt)
        elif self.resource_mode == "CONSTANT":
            to_spawn = self.resource_cap-len(self.resources)
        else:
            to_spawn = 0

        if to_spawn > 0:
            new_positions = np.random.rand(to_spawn, 2) * self.size
            self.resources.extend(new_positions.tolist())

    def spawn_resources_constant(self, resource_limit):
        to_spawn = resource_limit-len(self.resources)
        if to_spawn > 0:
            new_positions = np.random.rand(to_spawn, 2)*self.size
            self.resources.extend(new_positions.tolist())
    
    

    def apply_periodic_boundary(self, pos):
        return np.mod(pos, self.size)

    def remove_resource(self, index):
        del self.resources[index]
