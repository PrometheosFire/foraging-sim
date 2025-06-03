import pygame
import numpy as np
from evaluation.Fenotype_Realtime import DualPlot

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def run_pygame(simulation, steps=1000, dt=0.1, scale=600):
    pygame.init()
    font = pygame.font.SysFont("Arial", 16)
    size_px = int(simulation.env.size * scale)
    
    # Create wider window to fit scatter plot
    screen = pygame.display.set_mode((size_px + 400, max(size_px, 600)))
    clock = pygame.time.Clock()
    
    # Initialize scatter plot
    scatter_plot = DualPlot()

    # Create a surface for text backgrounds
    text_bg = pygame.Surface((100, 50), pygame.SRCALPHA)  # Semi-transparent
    text_bg.fill((0, 0, 0, int(0.75*256)))  # Black with 50% opacity
    
    running = True
    step = 0

    while running and step < steps:
        screen.fill(WHITE)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulation step
        simulation.step(dt)

        # Draw environment (original visualization)
        for res in simulation.env.resources:
            pos_px = (int(res[0] * scale), int(res[1] * scale))
            pygame.draw.rect(screen, RED, (*pos_px, 4, 4))

        for agent in simulation.agents:
            pos_px = (int(agent.pos[0] * scale), int(agent.pos[1] * scale))
            pygame.draw.circle(screen, BLUE, pos_px, 3)

        # Update scatter plot
        plot_surface = scatter_plot.update(simulation.time, simulation.agents)
        if plot_surface:
            screen.blit(plot_surface, (size_px, 0))  # Draw plot on right side

        # Draw text background before text
        screen.blit(text_bg, (5, 5))  # Position slightly offset from text

        # Labels with better contrast
        time_label = font.render(f"Time: {simulation.time:.2f}", True, (255, 255, 255))  # White text
        count_label = font.render(f"Agents: {len(simulation.agents)}", True, (255, 255, 255))
        screen.blit(time_label, (10, 10))
        screen.blit(count_label, (10, 30))

        pygame.display.flip()
        clock.tick(60)
        step += 1

    pygame.quit()
