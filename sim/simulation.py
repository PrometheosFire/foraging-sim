import numpy as np
from agents.agent import Agent
from env.environment import Environment

class Simulation:
    def __init__(self, config):
        self.env = Environment(**config['env'])
        self.agents = [Agent(**params) for params in config['initial_agents']]
        self.config = config
        self.time = 0.0

    def step(self, dt):
        self.env.spawn_resources(dt)

        for agent in self.agents[:]:  # Copy to safely modify during iteration
            closest_resource = agent.closest_food_in_range(self.env.resources, self.env.size)

            if closest_resource != None:
                closest_resource_pos = closest_resource[0]
                closest_resource_idx = closest_resource[1]
                agent.set_theta_to_resource(closest_resource_pos,self.env.size)
            else:
                agent.maybe_tumble(self.config['eta'], dt)
            
            agent.move(dt, self.env.size)
            agent.consume_energy(self.config['c_s'], self.config['c_a'], dt)

            # Resource consumption
            if closest_resource != None and np.linalg.norm(agent.pos - closest_resource_pos) < 0.01:
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

        self.time += dt
