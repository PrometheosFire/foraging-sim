# Entrypoint for simulation
from sim.simulation import Simulation

if __name__ == "__main__":
    print("Starting simulation...")
    sim = Simulation()
    sim.run()  # Placeholder
