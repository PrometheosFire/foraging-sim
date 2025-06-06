import numpy as np
import pandas as pd

class SimulationMetrics:
    def __init__(self):
        """Initialize metrics collector with empty DataFrames"""
        self.agent_data = pd.DataFrame(columns=["F", "Lamb", "Simulation", "speed", "acuity"]).astype({
            "F" : float, "Lamb": float, "Simulation": int, "speed": float, "acuity": float })
    
    def collect_agents(self, agent_list, F, Lamb, MCsimulation):
        """
        Record agent statistics for current step
        Args:
            agent_list: List of agent objects
        """
        step_data = []
        for agent in agent_list:
            step_data.append({
                "F": F,
                "Lamb": Lamb,
                "Simulation": MCsimulation,
                "speed": agent.speed,
                "acuity": agent.acuity,
            })
        if step_data:  # Only concat if not empty
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
    def load_from_csv(cls, filename):
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