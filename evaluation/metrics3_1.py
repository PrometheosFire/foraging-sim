
import numpy as np
import pandas as pd

class SimulationMetrics:
    def __init__(self, rate):
        """Initialize metrics collector with empty DataFrames"""
        self.rate = rate  # Store the rate for later use
        self.agent_data = pd.DataFrame(columns=["energy", "speed", "acuity", "Rate"]).astype({
            "energy": float, "speed": float, "acuity": float, "Rate": float })
        
    def collect_agent(self, agent):
        """
        Record agent statistics
        Args:
            agent: Agent object
        """
        agent_data = {
            "energy": agent.energy,
            "speed": agent.speed,
            "acuity": agent.acuity,
            "Rate": self.rate
        }
        self.agent_data = pd.concat([self.agent_data, pd.DataFrame([agent_data])], ignore_index=True)

    def save_to_csv(self, filename):
        """
        Save collected metrics to a CSV file
        Args:
            filename: Output file path
        """
        self.agent_data.to_csv(filename, index=False)
        print(f"Metrics saved to {filename}")

    @classmethod
    def load_from_csv(cls, filename, rate):
        """
        Load metrics from a CSV file
        Args:
            filename: Input file path
        Returns:
            SimulationMetrics object with loaded data
        """
        metrics = cls(rate)
        metrics.agent_data = pd.read_csv(filename)
        return metrics