import numpy as np

class Environment:
    def __init__(self, size=1.0, lambda_rate=100, resource_energy=1.0):
        self.size = size
        self.lambda_rate = lambda_rate
        self.resource_energy = resource_energy
        self.resources = []

    def spawn_resources(self, dt):
        n_new = np.random.poisson(self.lambda_rate * dt)
        if n_new > 0:
            new_positions = np.random.rand(n_new, 2) * self.size
            self.resources.extend(new_positions.tolist())

    def apply_periodic_boundary(self, pos):
        return np.mod(pos, self.size)

    def remove_resource(self, index):
        del self.resources[index]
