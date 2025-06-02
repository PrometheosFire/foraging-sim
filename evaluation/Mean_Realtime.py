import matplotlib.pyplot as plt
import numpy as np

class RealTimeMeanPlot:
    def __init__(self):
        plt.ion()  # Turn on interactive mode
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 4))
        self.fig.tight_layout(pad=2)
        self.time_data = []
        self.avg_speed_data = []
        self.avg_acuity_data = []

    def update(self, time, agents):
        if not agents:
            avg_speed = 0
            avg_acuity = 0
        else:
            avg_speed = np.mean([a.speed for a in agents])
            avg_acuity = np.mean([a.acuity for a in agents])

        self.time_data.append(time)
        self.avg_speed_data.append(avg_speed)
        self.avg_acuity_data.append(avg_acuity)

        self.ax1.clear()
        self.ax2.clear()
        self.ax1.plot(self.time_data, self.avg_speed_data, color='blue', label='Avg Speed')
        self.ax2.plot(self.time_data, self.avg_acuity_data, color='green', label='Avg Acuity')

        self.ax1.set_ylabel("Speed")
        self.ax2.set_ylabel("Acuity")
        self.ax2.set_xlabel("Time")
        self.ax1.legend()
        self.ax2.legend()
        plt.pause(0.001)

    def finalize(self):
        plt.ioff()
        plt.show()