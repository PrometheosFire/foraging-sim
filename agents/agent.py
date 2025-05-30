from dataclasses import dataclass
import numpy as np

@dataclass(slots=True)
class Agent:
    pos: np.ndarray  # Position: shape (2,)
    speed: float     # Agent speed
    acuity: float    # Sensory range
    energy: float    # Metabolic energy
    theta: float     # Movement direction in radians

    def move(self, dt: float, domain_size: float = 1.0):
        # Calculate displacement
        dx = self.speed * dt * np.array([np.cos(self.theta), np.sin(self.theta)])
        self.pos = (self.pos + dx) % domain_size  # Periodic boundary

    def consume_energy(self, c_s: float, c_a: float, dt: float):
        cost = (c_s * self.speed**2 + c_a * self.acuity) * dt
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
            theta=np.random.uniform(0, 2 * np.pi)
        )
