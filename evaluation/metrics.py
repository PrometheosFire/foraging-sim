import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

def collect_statistics(agent_list, generation):
    data = []
    for agent in agent_list:            # For each agent in the generation
        data.append({
            "generation": generation,
            "speed": agent.speed,       # Extracts agent's speed
            "acuity": agent.acuity,     # Extracts agent's sensory range
            "energy": agent.energy,     # Extracts agent's metabolic energy
            "alive": agent.energy > 0   # An agent is considered 'alive' if energy > 0
        })
    return pd.DataFrame(data)


def compute_means(df):
    # Compute average values of speed, acuity, and energy for each generation
    return df.groupby("generation")[["speed", "acuity", "energy"]].mean()


def population_size(df):
    # Compute population size (number of alive agents) in each generation
    return df[df["alive"]].groupby("generation").size()


def correlation(df):
    # Last generation (maximum generation value)
    last_gen = df[df["generation"] == df["generation"].max()]
    # Compute Pearson correlation between speed and acuity
    corr, _ = pearsonr(last_gen["speed"], last_gen["acuity"])
    return corr


def plot_means(df):
    means = compute_means(df)
    means.plot(title="Average values per generation")
    plt.ylabel("Mean value")
    plt.xlabel("Generation")
    plt.grid(True)
    plt.show()


def plot_population(df):
    pop = population_size(df)
    pop.plot(title="Population size per generation")
    plt.ylabel("Number of agents")
    plt.xlabel("Generation")
    plt.grid(True)
    plt.show()


def plot_distributions(df):
    # Plots the distribution of phenotypes (speed vs acuity) in the last generation
    last_gen = df[df["generation"] == df["generation"].max()]
    sns.kdeplot(data=last_gen, x="speed", y="acuity", fill=True)
    plt.title("Phenotype distribution (last generation)")
    plt.xlabel("Speed")
    plt.ylabel("Acuity")
    plt.grid(True)
    plt.show()