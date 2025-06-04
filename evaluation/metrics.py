import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

class SimulationMetrics:
    def __init__(self, config):
        """Initialize metrics collector with empty DataFrames"""
        self.config = config
        self.agent_data = pd.DataFrame(columns=["step", "speed", "acuity", "energy"]).astype({
            "step": int, "speed": float, "acuity": float, "energy": float })
        self.resource_data = pd.DataFrame(columns=["step", "x", "y"]).astype({
            "step": int, "x": float, "y": float})
        self.current_step = 0
    
    def collect_agents(self, agent_list, step):
        """
        Record agent statistics for current step
        Args:
            agent_list: List of agent objects
        """
        step_data = []
        for agent in agent_list:
            step_data.append({
                "step": step,
                "speed": agent.speed,
                "acuity": agent.acuity,
                "energy": agent.energy
            })
        
        if step_data:  # Only concat if not empty
            new_data = pd.DataFrame(step_data, columns=self.agent_data.columns)
            self.agent_data = pd.concat([self.agent_data, new_data], ignore_index=True)
        self.current_step = step
    
    def collect_resources(self, resource_list):
        """
        Record resource positions for current step
        Args:
            resource_list: List of resource coordinates [(x1,y1), (x2,y2), ...]
        """
        resource_records = []
        for x, y in resource_list:
            resource_records.append({
                "step": self.current_step,
                "x": x,
                "y": y
            })
        if resource_records:  # Only concat if not empty
            new_data = pd.DataFrame(resource_records, columns=self.resource_data.columns)
            self.resource_data = pd.concat([self.resource_data, new_data], ignore_index=True)
    
    
    def get_means(self):
        """Compute mean speed, acuity and energy per step"""
        return self.agent_data.groupby("step")[["speed", "acuity", "energy"]].mean()
    
    def get_population_sizes(self):
        """Get population size per step"""
        return self.agent_data.groupby("step").size()
    
    def get_resource_counts(self):
        """Get number of resources per step"""
        return self.resource_data.groupby("step").size()
    
    def get_last_step_correlation(self):
        """Get Pearson correlation between speed and acuity in last step"""
        last_gen = self.get_last_step_agents()
        if len(last_gen) > 1:
            return pearsonr(last_gen["speed"], last_gen["acuity"])[0]
        return np.nan
    
    def get_last_step_agents(self):
        """Get agent data for the last step"""
        return self.agent_data[self.agent_data["step"] == self.current_step - 1]
    
    def get_last_step_resources(self):
        """Get resource data for the last step"""
        return self.resource_data[self.resource_data["step"] == self.current_step - 1]
    
    def plot_summary(self, show=True):
        """Generate all standard plots"""
        self.plot_means(show=show)
        self.plot_population(show=show)
        self.plot_resource_counts(show=show)
        self.plot_distributions(show=show)
    
    def plot_means(self, show=True):
        """Plot average values per step"""
        means = self.get_means()
        means.plot(title="Average values per step")
        plt.ylabel("Mean value")
        plt.xlabel("step")
        plt.grid(True)
        if show:
            plt.show()
    
    def plot_population(self, show=True):
        """Plot population size per step"""
        pop = self.get_population_sizes()
        pop.plot(title="Agent population per step")
        plt.ylabel("Number of agents")
        plt.xlabel("step")
        plt.grid(True)
        if show:
            plt.show()
    
    def plot_resource_counts(self, show=True):
        """Plot resource counts per step"""
        res_counts = self.get_resource_counts()
        res_counts.plot(title="Resource counts per step")
        plt.ylabel("Number of resources")
        plt.xlabel("step")
        plt.grid(True)
        if show:
            plt.show()
    
    def plot_distributions(self, show=True):
        """Plot phenotype distribution in last step"""
        last_gen = self.get_last_step_agents()
        if len(last_gen) > 1:
            sns.kdeplot(data=last_gen, x="speed", y="acuity", fill=True)
            plt.title("Phenotype distribution (last step)")
            plt.xlabel("Speed")
            plt.ylabel("Acuity")
            plt.grid(True)
            if show:
                plt.show()
        elif show:
            print("Not enough data to plot phenotype distribution.")
    
    def plot_resource_positions(self, step=-1, show=True):
        """
        Plot resource positions for specific step
        Args:
            step: step number (-1 for last step)
            show: Whether to immediately display the plot
        """
        if step == -1:
            gen = self.current_step - 1
        else:
            gen = step
            
        resources = self.resource_data[self.resource_data["step"] == gen]
        
        plt.figure(figsize=(8, 8))
        plt.scatter(resources["x"], resources["y"], c='red', alpha=0.5)
        plt.title(f"Resource positions (step {gen})")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.grid(True)
        plt.axis('equal')
        
        if show:
            plt.show()
    
    def save_to_csv(self, agent_filename="agent_metrics.csv", 
                   resource_filename="resource_metrics.csv"):
        """Save collected data to CSV files"""
        self.agent_data.to_csv(agent_filename, index=False)
        self.resource_data.to_csv(resource_filename, index=False)
    
    @classmethod
    def load_from_csv(cls, config, agent_filename="agent_metrics.csv",
                     resource_filename="resource_metrics.csv"):
        """Load previously saved metrics"""
        metrics = cls(config)
        metrics.agent_data = pd.read_csv(agent_filename)
        metrics.resource_data = pd.read_csv(resource_filename)
        metrics.current_step = metrics.agent_data["step"].max() + 1
        metrics.config = config
        return metrics