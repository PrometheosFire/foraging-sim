from dataclasses import dataclass
import numpy as np

@dataclass(slots=True)
class Agent:
    pos: np.ndarray  # Position: shape (2,)
    speed: float     # Agent speed
    acuity: float    # Sensory range
    energy: float    # Metabolic energy
    theta: float     # Movement direction in radians

    c_a: float
    c_s: float


    def move(self, dt: float, domain_size, resources):
        resources = self.closest_food_in_range(resources, domain_size)
        if resources is None:
            self.run(dt, domain_size)
            self.maybe_tumble(eta=1.0, dt=dt)
            self.consume_energy(dt)
            return None
        
        resource_pos, resource_index, resource_dist = resources
        self.set_theta_to_resource(resource_pos, domain_size)
        self.run(dt, domain_size)
        self.consume_energy(dt)

        dist_diff = resource_dist - self.speed *dt
        if dist_diff <= 0:
            return resource_index, dist_diff
        else:
            return None

    def run(self, dt: float, domain_size: float = 1.0,  eta: float = 1.0):
        # Calculate displacement
        dx = self.speed * dt * np.array([np.cos(self.theta), np.sin(self.theta)])
        self.pos = (self.pos + dx) % domain_size  # Periodic boundary


    def consume_energy(self, dt: float):
        cost = (self.c_s * self.speed**2 + self.c_a * self.acuity) * dt
        self.energy -= cost

    def maybe_tumble(self, eta: float, dt: float):
        fr = self.speed / eta
        if np.random.rand() < 1 - np.exp(-fr * dt):
            self.theta = np.random.uniform(0, 2 * np.pi)

    def reproduce(self, sigma_s: float, sigma_a: float):
        child_speed = max(0, self.speed + np.random.normal(0, sigma_s))
        child_acuity = max(0, self.acuity + np.random.normal(0, sigma_a))
        child_energy = self.energy / 2
        self.energy /= 2
        return Agent(
            pos=self.pos.copy(),
            speed=child_speed,
            acuity=child_acuity,
            energy=child_energy,
            theta=np.random.uniform(0, 2 * np.pi),
            c_a=self.c_a,
            c_s=self.c_s
        )
    
    def closest_food_in_range(self, resources, size):
        if not resources:
            return None

        resources_array = np.array(resources)  # Shape: (N, 2)
        delta = np.abs(resources_array - self.pos)  # Shape: (N, 2)
        wrap_delta = np.minimum(delta, size - delta)  # Wraparound
        distances = np.linalg.norm(wrap_delta, axis=1)  # Euclidean

        in_range = np.where(distances <= self.acuity)[0]
        if in_range.size == 0:
            return None

        closest_distance = np.min(distances[in_range])
        closest_index = in_range[np.argmin(distances[in_range])]
        return resources[closest_index], closest_index, closest_distance
    
    def torus_distance(self, a, b, size):
        delta = np.abs(np.array(a) - np.array(b))
        wrap_delta = np.minimum(delta, np.array(size) - delta)
        return np.linalg.norm(wrap_delta)
    
    def set_theta_to_resource(self, resource, size):
        delta = np.array(resource) - np.array(self.pos)
        wrapped_delta = (delta + size / 2) % size - size / 2
        self.theta = np.arctan2(wrapped_delta[1], wrapped_delta[0])
        return 
