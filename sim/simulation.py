import numpy as np
from agents.agent import Agent
from agents.SlothAgent import SlothAgent
from agents.TurtleAgent import TurtleAgent
from env.environment import Environment
from env.spatial_grid import SpatialGrid
from agents.RaptorAgent import RaptorAgent

class Simulation:
    def __init__(self, config):
        self.env = Environment(**config['env'])
        self.config = config
        self.rng = np.random.default_rng()
        self.max_gen = 0
        self.time = 0.0
        self.currentID = 0
        self.agents = self.initialize_agents(**config['initial_agents'])

    def generate_id(self):
        """
        Generate a unique ID for an agent.
        """
        agent_id = self.currentID
        self.currentID += 1
        return agent_id

    def prob_birth(self, E, dt, agent_mult):
        """
        Compute probability of reproduction during dt, based on metabolic energy.
        """
        alpha = self.config['alpha']
        beta = self.config['beta']
        K_b = self.config['K_b'] * agent_mult
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
        new_gen = False
        
        self.env.spawn_resources(dt)
        
        i = 0
        ressources_consumed = {}
        for agent in self.agents:  # Copy to safely modify during iteration
            out = agent.move(dt, self.env.size, self.env.grid.nearby(agent.pos, agent.acuity))
            if out is not None:
                resource_idx = out[0]
                dist_diff = out[1]
                resource_pos = out[2]
                if resource_pos not in ressources_consumed or ressources_consumed[resource_pos][1] > dist_diff:
                    ressources_consumed[resource_pos] = (i, dist_diff)
                
            i += 1

        # Remove resources in descending order of indices to avoid shifting issues
        for pos, values in ressources_consumed.items():
            self.env.remove_resource(pos)
            self.agents[values[0]].energy += self.env.resource_energy
        
        survivors = []

        for agent in self.agents:
            # Reproduction
            if self.rng.random() < self.prob_birth(agent.energy, dt, agent.birth_mult):
                gen, babys = agent.reproduce(
                    self.config['sigma_s'],
                    self.config['sigma_a'],
                    self.generate_id()
                )
                survivors.extend(babys)
                self.max_gen = max(self.max_gen, gen)

            # Death
            if self.rng.random() < self.prob_death(agent.energy, dt):
                continue

            survivors.append(agent)
        
        self.agents = survivors
        self.time += dt
        return self.max_gen


    def initialize_agents(self, n_agents: int, starting_energy: float, size: float, c_a: float, c_s: float, C: float, mode: str, speed: float , acuity: float):
        agents = []
        for i in range(n_agents):
            pos = np.random.rand(2) * size
            species = [Agent, SlothAgent, TurtleAgent, RaptorAgent]
            if (mode == "SAME_COST"):
                speed = np.random.uniform(0, np.sqrt(C/c_s))
                acuity = get_acuity_from_speed(speed, c_a, c_s, C)
                AgentClass = Agent
            elif (mode == "UNIFORM") :
                speed = np.random.uniform(0, 0.2)
                acuity = np.random.uniform(0, 0.2)
                AgentClass = Agent
            elif (mode == "DEFINED"):
                speed = speed
                acuity = acuity
                AgentClass = Agent
            elif (mode == "SPECIES"):
                speed = np.random.uniform(0, 0.2)
                acuity = np.random.uniform(0, 0.2)
                AgentClass = species[i%4]
            else:
                raise ValueError("Invalid mode specified. Choose from 'SAME_COST', 'UNIFORM', 'DEFINED', or 'SPECIES'.")

            theta = np.random.uniform(0, 2 * np.pi)
            agents.append(AgentClass(pos=pos, speed=speed, acuity=acuity, energy=starting_energy, theta=theta, c_a=c_a, c_s=c_s, gen=0, id= self.generate_id()))
        return agents

def get_acuity_from_speed(speed: float, c_a:float, c_s:float, C: float):
    return (C - c_s*speed**2) / c_a

def torus_displacement(a, b, size):
    """Shortest displacement from a to b on a torus."""
    return (np.array(b) - np.array(a) + size / 2) % size - size / 2

def intercepts(start_pos, end_pos, resource_pos, size):
    to_resource = torus_displacement(start_pos, resource_pos, size)
    to_end = torus_displacement(start_pos, end_pos, size)
    dist_to_resource = np.linalg.norm(to_resource)
    dist_to_end = np.linalg.norm(to_end)
    return dist_to_resource <= dist_to_end

