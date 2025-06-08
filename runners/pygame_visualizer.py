import pygame
import numpy as np
from evaluation.Fenotype_Realtime import DualPlot
from agents.RaptorAgent import RaptorAgent
from agents.SlothAgent import SlothAgent
from agents.TurtleAgent import TurtleAgent
from agents.agent import Agent

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (30,30,30)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
FOOD = (255, 140, 0)  # Orange color for food
LIGHT_PINK = (255, 182, 193)

color_map = {
    RaptorAgent: RED,
    TurtleAgent: GREEN,
    SlothAgent: YELLOW,
    Agent: BLUE
}

def run_pygame(simulation, steps=1000, initial_dt=0.1, scale=600):
    pygame.init()
    font = pygame.font.SysFont("Arial", 16)
    size_px = int(simulation.env.size * scale)
    
    # Create wider window to fit scatter plot
    screen = pygame.display.set_mode((size_px + 400, max(size_px, 600)))
    clock = pygame.time.Clock()
    
    # Initialize scatter plot
    scatter_plot = DualPlot()

    # Create a surface for text backgrounds
    text_bg = pygame.Surface((100, 70), pygame.SRCALPHA)  # Semi-transparent
    text_bg.fill((0, 0, 0, int(0.75*256)))  # Black with 50% opacity
    
    running = True
    step = 0
    
    # Simulation control variables
    dt = initial_dt
    paused = False
    speed_multiplier = 1.0
    min_speed = 0.1  # Minimum speed (1/10th normal)
    max_speed = 10.0  # Maximum speed (10x normal)
    min_dt = 0.01  # Maximum speed (10x normal)
    max_dt = 1.0   # Minimum speed (1/10th normal)

    while running and step < steps:
        screen.fill(BLACK)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # Toggle pause
                elif event.key == pygame.K_RIGHT:
                    speed_multiplier += 0.1  # Speed up
                elif event.key == pygame.K_LEFT:
                    speed_multiplier -= 0.1  # Slow down
                elif event.key == pygame.K_r:  # Reset speed
                    speed_multiplier = 1.0
                    dt = initial_dt
                speed_multiplier = max(min_speed, min(max_speed, speed_multiplier))  # Clamp dt to limits
                dt = initial_dt* speed_multiplier  # Apply speed multiplier

        # Simulation step
        # Only update simulation if not paused
        if not paused:
            simulation.step(dt)
            step += 1

        # Draw environment (original visualization)
        for res in simulation.env.resources:
            pos_px = (int(res[0] * scale), int(res[1] * scale))
            pygame.draw.rect(screen, LIGHT_PINK, (*pos_px, 4, 4))

        for agent in simulation.agents:
            agentColor = getAgentColor(agent)
            pos_px = (int(agent.pos[0] * scale), int(agent.pos[1] * scale))
            pygame.draw.circle(screen, agentColor, pos_px, 3)

        # Update scatter plot
        plot_surface = scatter_plot.update(simulation.time, simulation.agents)
        if plot_surface:
            screen.blit(plot_surface, (size_px, 0))  # Draw plot on right side

        # Draw text background before text
        screen.blit(text_bg, (5, 5))  # Position slightly offset from text

        # Labels with better contrast
        time_label = font.render(f"Time: {simulation.time:.2f}", True, (255, 255, 255))  # White text
        count_label = font.render(f"Agents: {len(simulation.agents)}", True, (255, 255, 255))
        time_step = font.render(f"Time Step: {dt:.2f}", True, (255, 255, 255))
        screen.blit(time_label, (10, 10))
        screen.blit(count_label, (10, 30))
        screen.blit(time_step, (10, 50))

        pygame.display.flip()
        clock.tick(60)
        step += 1

    pygame.quit()

def getAgentColor(agent):
    for spec, color in color_map.items():
        if isinstance(agent, spec):
            return color
    return WHITE
