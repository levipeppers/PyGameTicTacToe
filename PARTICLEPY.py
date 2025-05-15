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
green = (0, 255, 0)
orange = (255, 165, 0)
cyan = (0, 255, 255)

# Updated particle properties
num_particles = 200  # Increased to 200 for each type
particle_radius = 4  # Reduced size
speed = 3  # Increased speed

# Reinitialize particles with the updated count
red_particles = []
yellow_particles = []
green_particles = []
orange_particles = []
cyan_particles = []
for _ in range(num_particles):
    red_particles.append([random.randint(0, width), random.randint(0, height)])
    yellow_particles.append([random.randint(0, width), random.randint(0, height)])
    green_particles.append([random.randint(0, width), random.randint(0, height)])
    orange_particles.append([random.randint(0, width), random.randint(0, height)])
    cyan_particles.append([random.randint(0, width), random.randint(0, height)])

# Randomly decide attraction and repulsion rules for each color
color_interactions = {
    "red": {
        "attract": random.choice(["yellow", "green", "orange", "cyan", None]),
        "repel": random.choice(["yellow", "green", "orange", "cyan", None]),
    },
    "yellow": {
        "attract": random.choice(["red", "green", "orange", "cyan", None]),
        "repel": random.choice(["red", "green", "orange", "cyan", None]),
    },
    "green": {
        "attract": random.choice(["red", "yellow", "orange", "cyan", None]),
        "repel": random.choice(["red", "yellow", "orange", "cyan", None]),
    },
    "orange": {
        "attract": random.choice(["red", "yellow", "green", "cyan", None]),
        "repel": random.choice(["red", "yellow", "green", "cyan", None]),
    },
    "cyan": {
        "attract": random.choice(["red", "yellow", "green", "orange", None]),
        "repel": random.choice(["red", "yellow", "green", "orange", None]),
    },
}

# Helper function to calculate distance
def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Helper function to resolve collisions
def resolve_collision(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dist = math.hypot(dx, dy)
    if dist < 2 * particle_radius:  # If particles are overlapping
        overlap = 2 * particle_radius - dist
        angle = math.atan2(dy, dx)
        p1[0] += math.cos(angle) * overlap / 2
        p1[1] += math.sin(angle) * overlap / 2
        p2[0] -= math.cos(angle) * overlap / 2
        p2[1] -= math.sin(angle) * overlap / 2

# Helper function to resolve collisions for all particles
def resolve_all_collisions(particles):
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i != j:
                resolve_collision(p1, p2)

# Helper function to keep particles within screen boundaries
def keep_within_bounds(particle):
    if particle[0] < particle_radius:
        particle[0] = particle_radius
    elif particle[0] > width - particle_radius:
        particle[0] = width - particle_radius
    if particle[1] < particle_radius:
        particle[1] = particle_radius
    elif particle[1] > height - particle_radius:
        particle[1] = height - particle_radius

# Font for rendering text
font = pygame.font.Font(None, 36)

# Function to render the menu
def render_menu():
    menu_surface = pygame.Surface((width, height))
    menu_surface.set_alpha(200)  # Make it semi-transparent
    menu_surface.fill((50, 50, 50))  # Gray background

    # Render text for each color's interactions
    y_offset = 50
    for color, interactions in color_interactions.items():
        attract_text = f"{color.capitalize()} attracts: {interactions['attract'] or 'None'}"
        repel_text = f"{color.capitalize()} repels: {interactions['repel'] or 'None'}"

        attract_surface = font.render(attract_text, True, (255, 255, 255))
        repel_surface = font.render(repel_text, True, (255, 255, 255))

        menu_surface.blit(attract_surface, (50, y_offset))
        y_offset += 40
        menu_surface.blit(repel_surface, (50, y_offset))
        y_offset += 60

    screen.blit(menu_surface, (0, 0))
    pygame.display.flip()

# Main game loop
menu_active = False
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Toggle menu with 'M'
                menu_active = not menu_active

    if menu_active:
        render_menu()
        continue  # Skip updating particles when the menu is active

    # Debugging logs
    print("Updating particles...")

    # Update particle positions
    for i, red_particle in enumerate(red_particles):
        # Red particle interactions
        if color_interactions["red"]["attract"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(red_particle, yellow_particle) < 100:
                    angle = math.atan2(red_particle[1] - yellow_particle[1], red_particle[0] - yellow_particle[0])
                    yellow_particle[0] -= speed * math.cos(angle) * 0.2
                    yellow_particle[1] -= speed * math.sin(angle) * 0.2
                    red_particle[0] += speed * math.cos(angle) * 0.1
                    red_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["red"]["attract"] == "green":
            for green_particle in green_particles:
                if distance(red_particle, green_particle) < 100:
                    angle = math.atan2(red_particle[1] - green_particle[1], red_particle[0] - green_particle[0])
                    green_particle[0] -= speed * math.cos(angle) * 0.2
                    green_particle[1] -= speed * math.sin(angle) * 0.2
                    red_particle[0] += speed * math.cos(angle) * 0.1
                    red_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["red"]["attract"] == "orange":
            for orange_particle in orange_particles:
                if distance(red_particle, orange_particle) < 100:
                    angle = math.atan2(red_particle[1] - orange_particle[1], red_particle[0] - orange_particle[0])
                    orange_particle[0] -= speed * math.cos(angle) * 0.2
                    orange_particle[1] -= speed * math.sin(angle) * 0.2
                    red_particle[0] += speed * math.cos(angle) * 0.1
                    red_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["red"]["attract"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(red_particle, cyan_particle) < 100:
                    angle = math.atan2(red_particle[1] - cyan_particle[1], red_particle[0] - cyan_particle[0])
                    cyan_particle[0] -= speed * math.cos(angle) * 0.2
                    cyan_particle[1] -= speed * math.sin(angle) * 0.2
                    red_particle[0] += speed * math.cos(angle) * 0.1
                    red_particle[1] += speed * math.sin(angle) * 0.1

        if color_interactions["red"]["repel"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(red_particle, yellow_particle) < 100:
                    angle = math.atan2(yellow_particle[1] - red_particle[1], yellow_particle[0] - red_particle[0])
                    red_particle[0] -= speed * math.cos(angle) * 0.2
                    red_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["red"]["repel"] == "green":
            for green_particle in green_particles:
                if distance(red_particle, green_particle) < 100:
                    angle = math.atan2(green_particle[1] - red_particle[1], green_particle[0] - red_particle[0])
                    red_particle[0] -= speed * math.cos(angle) * 0.2
                    red_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["red"]["repel"] == "orange":
            for orange_particle in orange_particles:
                if distance(red_particle, orange_particle) < 100:
                    angle = math.atan2(orange_particle[1] - red_particle[1], orange_particle[0] - red_particle[0])
                    red_particle[0] -= speed * math.cos(angle) * 0.2
                    red_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["red"]["repel"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(red_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - red_particle[1], cyan_particle[0] - red_particle[0])
                    red_particle[0] -= speed * math.cos(angle) * 0.2
                    red_particle[1] -= speed * math.sin(angle) * 0.2

        # Ensure red particles stay within bounds
        keep_within_bounds(red_particle)

    for i, yellow_particle in enumerate(yellow_particles):
        # Yellow particle interactions
        if color_interactions["yellow"]["attract"] == "red":
            for red_particle in red_particles:
                if distance(yellow_particle, red_particle) < 100:
                    angle = math.atan2(red_particle[1] - yellow_particle[1], red_particle[0] - yellow_particle[0])
                    yellow_particle[0] += speed * math.cos(angle) * 0.1
                    yellow_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["yellow"]["attract"] == "green":
            for green_particle in green_particles:
                if distance(yellow_particle, green_particle) < 100:
                    angle = math.atan2(green_particle[1] - yellow_particle[1], green_particle[0] - yellow_particle[0])
                    yellow_particle[0] += speed * math.cos(angle) * 0.1
                    yellow_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["yellow"]["attract"] == "orange":
            for orange_particle in orange_particles:
                if distance(yellow_particle, orange_particle) < 100:
                    angle = math.atan2(orange_particle[1] - yellow_particle[1], orange_particle[0] - yellow_particle[0])
                    yellow_particle[0] += speed * math.cos(angle) * 0.1
                    yellow_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["yellow"]["attract"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(yellow_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - yellow_particle[1], cyan_particle[0] - yellow_particle[0])
                    yellow_particle[0] += speed * math.cos(angle) * 0.1
                    yellow_particle[1] += speed * math.sin(angle) * 0.1

        if color_interactions["yellow"]["repel"] == "red":
            for red_particle in red_particles:
                if distance(yellow_particle, red_particle) < 100:
                    angle = math.atan2(red_particle[1] - yellow_particle[1], red_particle[0] - yellow_particle[0])
                    yellow_particle[0] -= speed * math.cos(angle) * 0.2
                    yellow_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["yellow"]["repel"] == "green":
            for green_particle in green_particles:
                if distance(yellow_particle, green_particle) < 100:
                    angle = math.atan2(green_particle[1] - yellow_particle[1], green_particle[0] - yellow_particle[0])
                    yellow_particle[0] -= speed * math.cos(angle) * 0.2
                    yellow_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["yellow"]["repel"] == "orange":
            for orange_particle in orange_particles:
                if distance(yellow_particle, orange_particle) < 100:
                    angle = math.atan2(orange_particle[1] - yellow_particle[1], orange_particle[0] - yellow_particle[0])
                    yellow_particle[0] -= speed * math.cos(angle) * 0.2
                    yellow_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["yellow"]["repel"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(yellow_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - yellow_particle[1], cyan_particle[0] - yellow_particle[0])
                    yellow_particle[0] -= speed * math.cos(angle) * 0.2
                    yellow_particle[1] -= speed * math.sin(angle) * 0.2

        # Ensure yellow particles stay within bounds
        keep_within_bounds(yellow_particle)

    for i, green_particle in enumerate(green_particles):
        # Green particle interactions
        if color_interactions["green"]["attract"] == "red":
            for red_particle in red_particles:
                if distance(green_particle, red_particle) < 100:
                    angle = math.atan2(red_particle[1] - green_particle[1], red_particle[0] - green_particle[0])
                    green_particle[0] += speed * math.cos(angle) * 0.1
                    green_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["green"]["attract"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(green_particle, yellow_particle) < 100:
                    angle = math.atan2(yellow_particle[1] - green_particle[1], yellow_particle[0] - green_particle[0])
                    green_particle[0] += speed * math.cos(angle) * 0.1
                    green_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["green"]["attract"] == "orange":
            for orange_particle in orange_particles:
                if distance(green_particle, orange_particle) < 100:
                    angle = math.atan2(orange_particle[1] - green_particle[1], orange_particle[0] - green_particle[0])
                    green_particle[0] += speed * math.cos(angle) * 0.1
                    green_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["green"]["attract"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(green_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - green_particle[1], cyan_particle[0] - green_particle[0])
                    green_particle[0] += speed * math.cos(angle) * 0.1
                    green_particle[1] += speed * math.sin(angle) * 0.1

        if color_interactions["green"]["repel"] == "red":
            for red_particle in red_particles:
                if distance(green_particle, red_particle) < 100:
                    angle = math.atan2(red_particle[1] - green_particle[1], red_particle[0] - green_particle[0])
                    green_particle[0] -= speed * math.cos(angle) * 0.2
                    green_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["green"]["repel"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(green_particle, yellow_particle) < 100:
                    angle = math.atan2(yellow_particle[1] - green_particle[1], yellow_particle[0] - green_particle[0])
                    green_particle[0] -= speed * math.cos(angle) * 0.2
                    green_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["green"]["repel"] == "orange":
            for orange_particle in orange_particles:
                if distance(green_particle, orange_particle) < 100:
                    angle = math.atan2(orange_particle[1] - green_particle[1], orange_particle[0] - green_particle[0])
                    green_particle[0] -= speed * math.cos(angle) * 0.2
                    green_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["green"]["repel"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(green_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - green_particle[1], cyan_particle[0] - green_particle[0])
                    green_particle[0] -= speed * math.cos(angle) * 0.2
                    green_particle[1] -= speed * math.sin(angle) * 0.2

        # Ensure green particles stay within bounds
        keep_within_bounds(green_particle)

    for i, orange_particle in enumerate(orange_particles):
        # Orange particle interactions
        if color_interactions["orange"]["attract"] == "red":
            for red_particle in red_particles:
                if distance(orange_particle, red_particle) < 100:
                    angle = math.atan2(red_particle[1] - orange_particle[1], red_particle[0] - orange_particle[0])
                    orange_particle[0] += speed * math.cos(angle) * 0.1
                    orange_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["orange"]["attract"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(orange_particle, yellow_particle) < 100:
                    angle = math.atan2(yellow_particle[1] - orange_particle[1], yellow_particle[0] - orange_particle[0])
                    orange_particle[0] += speed * math.cos(angle) * 0.1
                    orange_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["orange"]["attract"] == "green":
            for green_particle in green_particles:
                if distance(orange_particle, green_particle) < 100:
                    angle = math.atan2(green_particle[1] - orange_particle[1], green_particle[0] - orange_particle[0])
                    orange_particle[0] += speed * math.cos(angle) * 0.1
                    orange_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["orange"]["attract"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(orange_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - orange_particle[1], cyan_particle[0] - orange_particle[0])
                    orange_particle[0] += speed * math.cos(angle) * 0.1
                    orange_particle[1] += speed * math.sin(angle) * 0.1

        if color_interactions["orange"]["repel"] == "red":
            for red_particle in red_particles:
                if distance(orange_particle, red_particle) < 100:
                    angle = math.atan2(orange_particle[1] - red_particle[1], orange_particle[0] - red_particle[0])
                    orange_particle[0] -= speed * math.cos(angle) * 0.2
                    orange_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["orange"]["repel"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(orange_particle, yellow_particle) < 100:
                    angle = math.atan2(orange_particle[1] - yellow_particle[1], orange_particle[0] - yellow_particle[0])
                    orange_particle[0] -= speed * math.cos(angle) * 0.2
                    orange_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["orange"]["repel"] == "green":
            for green_particle in green_particles:
                if distance(orange_particle, green_particle) < 100:
                    angle = math.atan2(green_particle[1] - orange_particle[1], green_particle[0] - orange_particle[0])
                    orange_particle[0] -= speed * math.cos(angle) * 0.2
                    orange_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["orange"]["repel"] == "cyan":
            for cyan_particle in cyan_particles:
                if distance(orange_particle, cyan_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - orange_particle[1], cyan_particle[0] - orange_particle[0])
                    orange_particle[0] -= speed * math.cos(angle) * 0.2
                    orange_particle[1] -= speed * math.sin(angle) * 0.2

        # Ensure orange particles stay within bounds
        keep_within_bounds(orange_particle)

    for i, cyan_particle in enumerate(cyan_particles):
        # Cyan particle interactions
        if color_interactions["cyan"]["attract"] == "red":
            for red_particle in red_particles:
                if distance(cyan_particle, red_particle) < 100:
                    angle = math.atan2(red_particle[1] - cyan_particle[1], red_particle[0] - cyan_particle[0])
                    cyan_particle[0] += speed * math.cos(angle) * 0.1
                    cyan_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["cyan"]["attract"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(cyan_particle, yellow_particle) < 100:
                    angle = math.atan2(yellow_particle[1] - cyan_particle[1], yellow_particle[0] - cyan_particle[0])
                    cyan_particle[0] += speed * math.cos(angle) * 0.1
                    cyan_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["cyan"]["attract"] == "green":
            for green_particle in green_particles:
                if distance(cyan_particle, green_particle) < 100:
                    angle = math.atan2(green_particle[1] - cyan_particle[1], green_particle[0] - cyan_particle[0])
                    cyan_particle[0] += speed * math.cos(angle) * 0.1
                    cyan_particle[1] += speed * math.sin(angle) * 0.1
        elif color_interactions["cyan"]["attract"] == "orange":
            for orange_particle in orange_particles:
                if distance(cyan_particle, orange_particle) < 100:
                    angle = math.atan2(orange_particle[1] - cyan_particle[1], orange_particle[0] - cyan_particle[0])
                    cyan_particle[0] += speed * math.cos(angle) * 0.1
                    cyan_particle[1] += speed * math.sin(angle) * 0.1

        if color_interactions["cyan"]["repel"] == "red":
            for red_particle in red_particles:
                if distance(cyan_particle, red_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - red_particle[1], cyan_particle[0] - red_particle[0])
                    cyan_particle[0] -= speed * math.cos(angle) * 0.2
                    cyan_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["cyan"]["repel"] == "yellow":
            for yellow_particle in yellow_particles:
                if distance(cyan_particle, yellow_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - yellow_particle[1], cyan_particle[0] - yellow_particle[0])
                    cyan_particle[0] -= speed * math.cos(angle) * 0.2
                    cyan_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["cyan"]["repel"] == "green":
            for green_particle in green_particles:
                if distance(cyan_particle, green_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - green_particle[1], cyan_particle[0] - green_particle[0])
                    cyan_particle[0] -= speed * math.cos(angle) * 0.2
                    cyan_particle[1] -= speed * math.sin(angle) * 0.2
        elif color_interactions["cyan"]["repel"] == "orange":
            for orange_particle in orange_particles:
                if distance(cyan_particle, orange_particle) < 100:
                    angle = math.atan2(cyan_particle[1] - orange_particle[1], cyan_particle[0] - orange_particle[0])
                    cyan_particle[0] -= speed * math.cos(angle) * 0.2
                    cyan_particle[1] -= speed * math.sin(angle) * 0.2

        # Ensure cyan particles stay within bounds
        keep_within_bounds(cyan_particle)

    # Resolve collisions for all particle types
    resolve_all_collisions(red_particles)
    resolve_all_collisions(yellow_particles)
    resolve_all_collisions(green_particles)
    resolve_all_collisions(orange_particles)
    resolve_all_collisions(cyan_particles)

    # Ensure particles of different types repel each other
    for red_particle in red_particles:
        for yellow_particle in yellow_particles:
            resolve_collision(red_particle, yellow_particle)
        for green_particle in green_particles:
            resolve_collision(red_particle, green_particle)
        for orange_particle in orange_particles:
            resolve_collision(red_particle, orange_particle)
        for cyan_particle in cyan_particles:
            resolve_collision(red_particle, cyan_particle)

    for yellow_particle in yellow_particles:
        for green_particle in green_particles:
            resolve_collision(yellow_particle, green_particle)
        for orange_particle in orange_particles:
            resolve_collision(yellow_particle, orange_particle)
        for cyan_particle in cyan_particles:
            resolve_collision(yellow_particle, cyan_particle)

    for green_particle in green_particles:
        for orange_particle in orange_particles:
            resolve_collision(green_particle, orange_particle)
        for cyan_particle in cyan_particles:
            resolve_collision(green_particle, cyan_particle)

    for orange_particle in orange_particles:
        for cyan_particle in cyan_particles:
            resolve_collision(orange_particle, cyan_particle)

    # Draw everything
    screen.fill(black)
    for red_particle in red_particles:
        pygame.draw.circle(screen, red, (int(red_particle[0]), int(red_particle[1])), particle_radius)
    for yellow_particle in yellow_particles:
        pygame.draw.circle(screen, yellow, (int(yellow_particle[0]), int(yellow_particle[1])), particle_radius)
    for green_particle in green_particles:
        pygame.draw.circle(screen, green, (int(green_particle[0]), int(green_particle[1])), particle_radius)
    for orange_particle in orange_particles:
        pygame.draw.circle(screen, orange, (int(orange_particle[0]), int(orange_particle[1])), particle_radius)
    for cyan_particle in cyan_particles:
        pygame.draw.circle(screen, cyan, (int(cyan_particle[0]), int(cyan_particle[1])), particle_radius)

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS
