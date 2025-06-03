import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class RealTimeMeanPlot:
    def __init__(self, max_data_points=1000):
        plt.ion()  # Interactive mode
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
        self.fig.tight_layout(pad=2)
        
        # Use deque for efficient rolling window
        self.max_data_points = max_data_points
        self.time_data = deque(maxlen=max_data_points)
        self.avg_speed_data = deque(maxlen=max_data_points)
        self.avg_acuity_data = deque(maxlen=max_data_points)
        
        # Initialize plots
        self.speed_line, = self.ax1.plot([], [], 'b-', label='Avg Speed')
        self.acuity_line, = self.ax2.plot([], [], 'g-', label='Avg Acuity')
        
        self.ax1.set_ylabel("Speed")
        self.ax2.set_ylabel("Acuity")
        self.ax2.set_xlabel("Time")
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax1.legend()
        self.ax2.legend()

    def update(self, time, agents):
        # Vectorized calculation for better performance
        if agents:
            speeds = np.fromiter((a.speed for a in agents), dtype=float)
            acuities = np.fromiter((a.acuity for a in agents), dtype=float)
            avg_speed = np.mean(speeds)
            avg_acuity = np.mean(acuities)
        else:
            avg_speed = 0
            avg_acuity = 0

        # Append new data
        self.time_data.append(time)
        self.avg_speed_data.append(avg_speed)
        self.avg_acuity_data.append(avg_acuity)
        
        # Update plot data (faster than clearing axes)
        self.speed_line.set_data(self.time_data, self.avg_speed_data)
        self.acuity_line.set_data(self.time_data, self.avg_acuity_data)
        
        # Auto-scale if not at max capacity
        if len(self.time_data) < self.max_data_points:
            self.ax1.relim()
            self.ax2.relim()
            self.ax1.autoscale_view()
            self.ax2.autoscale_view()
        
        # Efficient redraw
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def finalize(self):
        plt.ioff()
        plt.close(self.fig)