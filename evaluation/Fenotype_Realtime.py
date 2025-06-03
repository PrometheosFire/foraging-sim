import pygame
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

class DualPlot:
    def __init__(self, width=400, height=600):
        # Create figure with two subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(width/100, height/100),
                                                      gridspec_kw={'height_ratios': [2, 1]})
        self.canvas = FigureCanvasAgg(self.fig)
        
        # Configure scatter plot (top)
        self.ax1.set_xlabel('Speed', fontsize=8)
        self.ax1.set_ylabel('Acuity', fontsize=8)
        self.scatter = self.ax1.scatter([], [], s=10, alpha=0.6, edgecolors='none')
        self.ax1.grid(True, alpha=0.3)
        self.max_speed = 0.1
        self.max_acuity = 0.1
        
        # Configure population plot (bottom)
        self.ax2.set_xlabel('Time (seconds)', fontsize=8)
        self.ax2.set_ylabel('Population', fontsize=8)
        self.pop_line, = self.ax2.plot([], [], 'g-', linewidth=2)
        self.ax2.grid(True, alpha=0.3)
        self.time_data = []
        self.pop_data = []
        self.time_window = 100  # Show last 100 seconds
        
        # Set equal aspect ratio for phenotype plot
        self.ax1.set_aspect('auto')  # We'll handle scaling manually
        self.fig.tight_layout(pad=3.0)

    def update(self, time, agents):
        # Update scatter plot with proportional scaling
        speeds = np.array([a.speed for a in agents]) if agents else np.array([])
        acuities = np.array([a.acuity for a in agents]) if agents else np.array([])
        
        if len(speeds) > 0:
            # Get 95th percentile to avoid outliers dominating scale
            self.max_speed = max(0.1, np.percentile(speeds, 95) * 1.1)
            self.max_acuity = max(0.1, np.percentile(acuities, 95) * 1.1)
            
            # Make axes proportional
            max_dim = max(self.max_speed, self.max_acuity)
            self.ax1.set_xlim(0, max_dim)
            self.ax1.set_ylim(0, max_dim)
            self.scatter.set_offsets(np.column_stack((speeds, acuities)))
        
        # Update population plot with dynamic Y scaling
        population = len(agents)
        self.time_data.append(time)
        self.pop_data.append(population)
        
        # Trim data to time window
        while len(self.time_data) > 1 and (time - self.time_data[0]) > self.time_window:
            self.time_data.pop(0)
            self.pop_data.pop(0)
        
        # Calculate Y-axis limits with buffer
        current_max_pop = max(self.pop_data[-100:]) if self.pop_data else 1
        #y_buffer = max(5, current_max_pop * 0.1)  # At least 5 units buffer
        y_max = current_max_pop*2
        
        self.pop_line.set_data(self.time_data, self.pop_data)
        self.ax2.set_xlim(max(0, time - self.time_window), max(time, self.time_window))
        self.ax2.set_ylim(0, y_max)
        
        # Render to Pygame surface
        self.canvas.draw()
        buf = self.canvas.buffer_rgba()
        return pygame.image.frombuffer(buf, self.canvas.get_width_height(), 'RGBA')