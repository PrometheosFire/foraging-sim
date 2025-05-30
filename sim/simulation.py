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
            agent.maybe_tumble(self.config['eta'], dt)
            agent.move(dt, self.env.size)
            agent.consume_energy(self.config['c_s'], self.config['c_a'], dt)

            # Resource consumption
            consumed = False
            for i, res in enumerate(self.env.resources):
                if np.linalg.norm(agent.pos - res) < agent.acuity:
                    agent.energy += self.env.resource_energy
                    self.env.remove_resource(i)
                    consumed = True
                    break  # only consume one resource per step

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
