import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Converts a list of agents into a DataFrame with relevant attributes
def get_dataframe(agent_list, generation):
    """
    Extracts agent statistics into a DataFrame for a given generation.
    Assumes agents have attributes: speed, acuity, energy, pos.
    An agent is considered 'alive' if energy > 0.
    """
    data = []
    for agent in agent_list:
        data.append({
            "generation": generation,
            "speed": agent.speed,
            "acuity": agent.acuity,
            "energy": agent.energy,
            "alive": agent.energy > 0
        })
    return pd.DataFrame(data)


# Computes average values of speed, acuity, and energy over generations
def compute_means(df):
    """
    Returns average speed, acuity, and energy for each generation.
    """
    return df.groupby("generation")[["speed", "acuity", "energy"]].mean()


# Calculates population size (number of alive agents) per generation
def population_size(df):
    """
    Returns the number of alive agents in each generation.
    """
    return df[df["alive"]].groupby("generation").size()


# Calculates the Pearson correlation between speed and acuity in the final generation
def correlation(df):
    """
    Returns Pearson correlation between speed and acuity in the last generation.
    """
    last_gen = df[df["generation"] == df["generation"].max()]
    corr, _ = pearsonr(last_gen["speed"], last_gen["acuity"])
    return corr


# Plots average values over generations
def plot_means(df):
    """
    Plots mean speed, acuity, and energy over time.
    """
    means = compute_means(df)
    means.plot(title="Average values per generation")
    plt.ylabel("Mean value")
    plt.xlabel("Generation")
    plt.grid(True)
    plt.show()


# Plots population size over generations
def plot_population(df):
    """
    Plots the number of alive agents per generation.
    """
    pop = population_size(df)
    pop.plot(title="Population size per generation")
    plt.ylabel("Number of agents")
    plt.xlabel("Generation")
    plt.grid(True)
    plt.show()


# Plots the distribution of phenotypes (speed vs acuity) in the final generation
def plot_distributions(df):
    """
    Creates a density plot of speed vs acuity for the final generation.
    """
    last_gen = df[df["generation"] == df["generation"].max()]
    sns.kdeplot(data=last_gen, x="speed", y="acuity", fill=True)
    plt.title("Phenotype distribution (last generation)")
    plt.xlabel("Speed")
    plt.ylabel("Acuity")
    plt.grid(True)
    plt.show()


# Placeholder function if needed externally (optional)
def collect_statistics():
    """
    Placeholder for future use.
    """
    return {}