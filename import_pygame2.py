import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Particle Simulation")

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Particle properties
num_particles = 100
particle_radius = 5
speed = 2
red_particles = []
yellow_particles = []

# Initialize particles
for _ in range(num_particles):
    red_particles.append([random.randint(0, width), random.randint(0, height), random.uniform(-speed, speed), random.uniform(-speed, speed)])
    yellow_particles.append([random.randint(0, width), random.randint(0, height), random.uniform(-speed, speed), random.uniform(-speed, speed)])

# Helper function to calculate distance
def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Update particle positions
    for particles in [red_particles, yellow_particles]:
        for particle in particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

            # Bounce off walls
            if particle[0] - particle_radius < 0 or particle[0] + particle_radius > width:
                particle[2] = -particle[2]
            if particle[1] - particle_radius < 0 or particle[1] + particle_radius > height:
                particle[3] = -particle[3]

    # Check for collisions and move particles back
    for particles in [red_particles, yellow_particles]:
        for i, particle in enumerate(particles):
            for other in particles[i + 1:]:
                if distance(particle, other) < 2 * particle_radius:
                    # Move particles in random directions
                    angle = random.uniform(0, 2 * math.pi)
                    particle[0] -= math.cos(angle) * speed
                    particle[1] -= math.sin(angle) * speed
                    other[0] += math.cos(angle) * speed
                    other[1] += math.sin(angle) * speed

    # Draw everything
    screen.fill(black)
    for red_particle in red_particles:
        pygame.draw.circle(screen, red, (int(red_particle[0]), int(red_particle[1])), particle_radius)
    for yellow_particle in yellow_particles:
        pygame.draw.circle(screen, yellow, (int(yellow_particle[0]), int(yellow_particle[1])), particle_radius)

    pygame.display.flip()
    clock.tick(60)
