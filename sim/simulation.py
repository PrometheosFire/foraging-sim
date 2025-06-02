import numpy as np
from agents.agent import Agent
from env.environment import Environment

class Simulation:
    def __init__(self, config):
        self.env = Environment(**config['env'])
        self.agents = [Agent(**params) for params in config['initial_agents']]
        self.config = config
        self.time = 0.0
        self.rng = np.random.default_rng()

    def prob_birth(self, E, dt):
        """
        Compute probability of reproduction during dt, based on metabolic energy.
        """
        alpha = self.config['alpha']
        beta = self.config['beta']
        K_b = self.config['K_b']
        E = np.maximum(E, 1e-12)
        rate = beta * (E ** alpha) / (E ** alpha + K_b ** alpha)
        return 1 - np.exp(-rate * dt)
    
    def prob_death(self, E, dt):
        """
        Compute probability of death during dt, based on metabolic energy.
        """
        alpha = self.config['alpha']
        delta = self.config['delta']
        delta_0 = self.config['delta_0']
        K_d = self.config['K_d']
        E = np.maximum(E, 1e-12)
        rate =  delta_0 + delta * (K_d ** alpha) / (E ** alpha + K_d ** alpha)
        return 1 - np.exp(-rate * dt)

    def step(self, dt):
        self.env.spawn_resources(dt)
        
        i = 0
        ressources_consumed = {}
        for agent in self.agents:  # Copy to safely modify during iteration
            out = agent.move(dt, self.env.size, self.env.resources)
            if out is not None:
                resource_idx = out[0]
                dist_diff = out[1]
                if resource_idx not in ressources_consumed or ressources_consumed[resource_idx][1] > dist_diff:
                    ressources_consumed[resource_idx] = (i, dist_diff)
                
            i += 1

        # Remove resources in descending order of indices to avoid shifting issues
        for index, values in sorted(ressources_consumed.items(), key=lambda x: x[0], reverse=True):
            self.env.remove_resource(index)
            self.agents[values[0]].energy += self.env.resource_energy
        
        survivors = []

        for agent in self.agents[:]:
            # Reproduction
            if self.rng.random() < self.prob_birth(agent.energy, dt):
                survivors.append(agent.reproduce(
                    self.config['sigma_s'],
                    self.config['sigma_a']
                ))

            # Death
            if self.rng.random() < self.prob_death(agent.energy, dt):
                continue

            survivors.append(agent)
        
        self.agents = survivors

        """
        for agent in self.agents[:]:  # Copy to safely modify during iteration
            closest_resource = agent.closest_food_in_range(self.env.resources, self.env.size)

            starting_pos = agent.pos.copy()

            if closest_resource != None:
                closest_resource_pos = closest_resource[0]
                closest_resource_idx = closest_resource[1]
                agent.set_theta_to_resource(closest_resource_pos,self.env.size)
            else:
                agent.maybe_tumble(self.config['eta'], dt)
            
            agent.move(dt, self.env.size)
            agent.consume_energy(self.config['c_s'], self.config['c_a'], dt)
            
            ending_pos = agent.pos

            # Resource consumption
            if closest_resource != None and intercepts(starting_pos, ending_pos, closest_resource_pos, self.env.size):
                agent.energy += self.env.resource_energy
                self.env.remove_resource(closest_resource_idx)
        

            # Reproduction
            if agent.energy > self.config['E_birth_threshold']:
                self.agents.append(agent.reproduce(
                    self.config['sigma_s'],
                    self.config['sigma_a']
                ))

            # Death
            if agent.energy <= 0:
                self.agents.remove(agent)
        """

        self.time += dt

def torus_displacement(a, b, size):
    """Shortest displacement from a to b on a torus."""
    return (np.array(b) - np.array(a) + size / 2) % size - size / 2

def intercepts(start_pos, end_pos, resource_pos, size):
    to_resource = torus_displacement(start_pos, resource_pos, size)
    to_end = torus_displacement(start_pos, end_pos, size)
    dist_to_resource = np.linalg.norm(to_resource)
    dist_to_end = np.linalg.norm(to_end)
    return dist_to_resource <= dist_to_end
