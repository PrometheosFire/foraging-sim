import pygame
import numpy as np
from evaluation.Mean_Realtime import RealTimeMeanPlot

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def run_pygame(simulation, steps=1000, dt=0.1, scale=600):
    pygame.init()
    font = pygame.font.SysFont("Arial", 16)
    size_px = int(simulation.env.size * scale)
    screen = pygame.display.set_mode((size_px, size_px))
    clock = pygame.time.Clock()

    plotter = RealTimeMeanPlot()

    running = True
    step = 0

    while running and step < steps:
        screen.fill(WHITE)

        # Event handler to allow quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Run simulation logic
        simulation.step(dt)

        # Draw resources
        for res in simulation.env.resources:
            pos_px = (int(res[0] * scale), int(res[1] * scale))
            pygame.draw.rect(screen, RED, (*pos_px, 4, 4))  # small red square

        # Draw agents
        for agent in simulation.agents:
            pos_px = (int(agent.pos[0] * scale), int(agent.pos[1] * scale))
            pygame.draw.circle(screen, BLUE, pos_px, 3)

        # Labels
        time_label = font.render(f"Time: {simulation.time:.2f}", True, (0, 0, 0))
        count_label = font.render(f"Agents: {len(simulation.agents)}", True, (0, 0, 0))
        screen.blit(time_label, (10, 10))
        screen.blit(count_label, (10, 30))

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS
        step += 1

        if step % 10 == 0:  # Update plot every 10 steps
            plotter.update(simulation.time, simulation.agents)

    # After the loop ends
    plotter.finalize()
    pygame.quit()
