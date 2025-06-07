
import numpy as np
import pandas as pd

class SimulationMetrics:
    def __init__(self):
        """Initialize metrics collector with empty DataFrames"""
        self.agent_data = pd.DataFrame(columns=["Lamb", "F","species", "speed", "acuity",]).astype({
            "Lamb": float, "F": float, "species": str, "speed": float, "acuity": float})
        
    def collect_agents(self, agent_list, lamb, F):
        """
        Record agent statistics
        Args:
            agent: Agent object
        """
        step_data = []
        for agent in agent_list:
            agent_data = {
                "Lamb" : lamb,
                "F" : F,
                "species": agent.__class__.__name__,
                "speed": agent.speed,
                "acuity": agent.acuity,
            }
            step_data.append(agent_data)
        
        if step_data:
            new_data = pd.DataFrame(step_data, columns=self.agent_data.columns)
            self.agent_data = pd.concat([self.agent_data, new_data], ignore_index=True)

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