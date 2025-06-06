import pygame
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from collections import defaultdict

class DualPlot:
    def __init__(self, width=400, height=600):
        # Create figure with two subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(width/100, height/100),
                                                      gridspec_kw={'height_ratios': [2, 1]})
        self.canvas = FigureCanvasAgg(self.fig)

        # Configure scatter plot (top)
        self.ax1.set_xlabel('Speed', fontsize=8)
        self.ax1.set_ylabel('Acuity', fontsize=8)
        self.ax1.set_facecolor("#414141")
        self.scatter = self.ax1.scatter([], [], s=10, alpha=0.6, edgecolors='none')
        self.ax1.grid(True, alpha=0.3)
        self.max_speed = 0.2
        self.max_acuity = 0.2

        # Configure population plot (bottom)
        self.ax2.set_xlabel('Time (seconds)', fontsize=8)
        self.ax2.set_ylabel('Population', fontsize=8)
        self.ax2.set_facecolor("#414141")
        self.ax2.grid(True, alpha=0.3)
        self.time_window = 100  # Show last 100 seconds

        # Species color map
        self.species_colors = {
            'Agent': "#0000FF",
            'SlothAgent': "#FFFF00",
            'TurtleAgent': "#00FF00",
            'RaptorAgent': "#FF0000",
        }

        # Data storage for population over time per species
        self.species_data = defaultdict(lambda: {
            "time": [],
            "population": [],
            "line": None
        })

        # Initialize lines for each species
        for species, color in self.species_colors.items():
            line, = self.ax2.plot([], [], color=color, label=species, linewidth=1.5)
            self.species_data[species]["line"] = line

        self.ax2.legend(fontsize=6)
        self.fig.tight_layout(pad=3.0)

        # Set equal aspect ratio for phenotype plot
        self.ax1.set_aspect('auto')

    def update(self, time, agents):
        # ---------------- Scatter Plot ---------------- #
        speeds = np.array([a.speed for a in agents]) if agents else np.array([])
        acuities = np.array([a.acuity for a in agents]) if agents else np.array([])

        if len(speeds) > 0:
            colors = [
                self.species_colors.get(type(agent).__name__, 'gray')
                for agent in agents
            ]
            self.ax1.set_xlim(0, self.max_speed)
            self.ax1.set_ylim(0, self.max_acuity)
            self.scatter.remove()
            self.scatter = self.ax1.scatter(speeds, acuities, c=colors, s=10, alpha=0.6, edgecolors='none')

        # ---------------- Population Plot ---------------- #
        # Count species
        pop_counts = defaultdict(int)
        for agent in agents:
            species = type(agent).__name__
            pop_counts[species] += 1

        # Update each species line
        for species, data in self.species_data.items():
            data["time"].append(time)
            data["population"].append(pop_counts.get(species, 0))  # 0 if no members

            # Trim to time window
            while data["time"] and (time - data["time"][0]) > self.time_window:
                data["time"].pop(0)
                data["population"].pop(0)

            # Update line data
            data["line"].set_data(data["time"], data["population"])

        # Dynamic scaling
        self.ax2.set_xlim(max(0, time - self.time_window), max(time, self.time_window))
        max_pop = max(
            (max(data["population"]) for data in self.species_data.values() if data["population"]),
            default=1
        )
        self.ax2.set_ylim(0, max_pop * 1.2)

        # Render to Pygame surface
        self.canvas.draw()
        buf = self.canvas.buffer_rgba()
        return pygame.image.frombuffer(buf, self.canvas.get_width_height(), 'RGBA')
