import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def animate(simulation, steps=100, dt=0.1, interval=100):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, simulation.env.size)
    ax.set_ylim(0, simulation.env.size)
    ax.set_aspect('equal')
    ax.set_title("Simulation Animation")
    res_patches = []
    agent_patches = []

    def init():
        return []

    def update(frame):
        ax.clear()
        ax.set_xlim(0, simulation.env.size)
        ax.set_ylim(0, simulation.env.size)
        ax.set_aspect('equal')
        ax.set_title(f"Step {frame*dt:.2f} seconds")

        simulation.step(dt)

        # Draw resources
        for res in simulation.env.resources:
            r_patch = patches.Rectangle(res, 0.01, 0.01, color='red')
            ax.add_patch(r_patch)
            res_patches.append(r_patch)

        # Draw agents
        for agent in simulation.agents:
            a_patch = patches.Circle(agent.pos, radius=0.01, color='blue')
            ax.add_patch(a_patch)
            agent_patches.append(a_patch)

        return res_patches + agent_patches

    anim = FuncAnimation(fig, update, frames=steps, init_func=init,
                         blit=False, interval=interval, repeat=False)
    plt.show()
