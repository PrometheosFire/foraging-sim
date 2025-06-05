import numpy as np
import pandas as pd

class SimulationMetrics:
    def __init__(self):
        """Initialize metrics collector with empty DataFrames"""
        self.agent_data = pd.DataFrame(columns=["speed", "acuity", "population"]).astype({
            "speed": float, "acuity": float, "population": int })
    
    def collect_agents(self, agent_list):
        """
        Record agent statistics for current step
        Args:
            agent_list: List of agent objects
        """
        
        agent_data = {
            "speed": agent_list[0].speed,
            "acuity": agent_list[0].acuity,
            "population": len(agent_list)
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
        metrics = cls()
        metrics.agent_data = pd.read_csv(filename)
        return metrics