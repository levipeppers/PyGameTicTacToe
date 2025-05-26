import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600  # Keep logical dimensions for element placement
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set fullscreen mode
fullscreen_width, fullscreen_height = screen.get_size()  # Get actual fullscreen dimensions
pygame.display.set_caption("Particle Simulation")

# Grid parameters for spatial partitioning
CELL_SIZE = 50  # Size of each grid cell
grid_width = fullscreen_width // CELL_SIZE + 1
grid_height = fullscreen_height // CELL_SIZE + 1

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
interaction_distance = 100
interaction_distance_squared = interaction_distance * interaction_distance

# Reinitialize particles with the updated count
red_particles = []
yellow_particles = []
green_particles = []
orange_particles = []
cyan_particles = []

# Dictionary to easily access particle lists by color name
particle_lists = {
    "red": red_particles,
    "yellow": yellow_particles,
    "green": green_particles,
    "orange": orange_particles,
    "cyan": cyan_particles
}

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

# Preset configurations for particle interactions
preset_configs = {
    "Cycle": {
        "red": {"attract": "orange", "repel": "cyan"},
        "orange": {"attract": "yellow", "repel": "red"},
        "yellow": {"attract": "green", "repel": "orange"},
        "green": {"attract": "cyan", "repel": "yellow"},
        "cyan": {"attract": "red", "repel": "green"}
    },
    "Hole": {
        "red": {"attract": "cyan", "repel": None},
        "orange": {"attract": "cyan", "repel": None},
        "yellow": {"attract": "cyan", "repel": None},
        "green": {"attract": "cyan", "repel": None},
        "cyan": {"attract": None, "repel": None}
    },
    "Random": {  # Keep current random behavior as a preset
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
}

# Current preset name
current_preset = "Random"

# Helper function to calculate squared distance (more efficient than regular distance)
def squared_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return dx*dx + dy*dy

# Helper function to calculate distance
def distance(p1, p2):
    return math.sqrt(squared_distance(p1, p2))

# Helper function to resolve collisions
def resolve_collision(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dist_squared = dx*dx + dy*dy
    
    if dist_squared < 4 * particle_radius * particle_radius:  # If particles are overlapping
        dist = math.sqrt(dist_squared)
        if dist == 0:  # Avoid division by zero
            dx, dy = 1, 0
            dist = 1
        else:
            dx, dy = dx/dist, dy/dist
            
        overlap = 2 * particle_radius - dist
        p1[0] += dx * overlap / 2
        p1[1] += dy * overlap / 2
        p2[0] -= dx * overlap / 2
        p2[1] -= dy * overlap / 2

# Function to get grid cell for a particle
def get_grid_position(particle):
    grid_x = int(particle[0] // CELL_SIZE)
    grid_y = int(particle[1] // CELL_SIZE)
    return grid_x, grid_y

# Function to build spatial grid from particles
def build_spatial_grid(particles):
    grid = {}
    for i, particle in enumerate(particles):
        grid_pos = get_grid_position(particle)
        if grid_pos not in grid:
            grid[grid_pos] = []
        grid[grid_pos].append((i, particle))
    return grid

# Function to get neighboring cells for a grid position
def get_neighbor_cells(grid_x, grid_y):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = grid_x + dx, grid_y + dy
            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                neighbors.append((nx, ny))
    return neighbors

# Helper function to resolve collisions for all particles using spatial grid for optimization
def resolve_all_collisions(particles):
    # Build spatial grid for particles
    grid = build_spatial_grid(particles)
    
    # Check collisions only within same cell and neighboring cells
    for i, p1 in enumerate(particles):
        grid_pos = get_grid_position(p1)
        neighbors = get_neighbor_cells(*grid_pos)
        
        # Check collision with particles in neighboring cells
        for cell in neighbors:
            if cell in grid:
                for j, p2 in grid[cell]:
                    if i != j:  # Don't check collision with self
                        resolve_collision(p1, p2)

# Helper function to keep particles within screen boundaries
def keep_within_bounds(particle):
    if particle[0] < particle_radius:
        particle[0] = particle_radius
    elif particle[0] > fullscreen_width - particle_radius:  # Use fullscreen_width
        particle[0] = fullscreen_width - particle_radius
    if particle[1] < particle_radius:
        particle[1] = particle_radius
    elif particle[1] > fullscreen_height - particle_radius:  # Use fullscreen_height
        particle[1] = fullscreen_height - particle_radius

# Helper function to handle particle attraction
def handle_attraction(source_particle, target_particles):
    for target in target_particles:
        if squared_distance(source_particle, target) < interaction_distance_squared:
            angle = math.atan2(target[1] - source_particle[1], target[0] - source_particle[0])
            source_particle[0] += speed * math.cos(angle) * 0.1
            source_particle[1] += speed * math.sin(angle) * 0.1

# Helper function to handle particle repulsion
def handle_repulsion(source_particle, target_particles):
    for target in target_particles:
        if squared_distance(source_particle, target) < interaction_distance_squared:
            angle = math.atan2(target[1] - source_particle[1], target[0] - source_particle[0])
            source_particle[0] -= speed * math.cos(angle) * 0.2
            source_particle[1] -= speed * math.sin(angle) * 0.2

# Font for rendering text
font = pygame.font.Font(None, 36)

# Colors for cycling through interactions
interaction_colors = ["red", "yellow", "green", "orange", "cyan", None]  # Ensure "cyan" and None are included

# Function to render the menu and handle interaction editing
def render_menu(edit_mode=False, preset_mode=False):
    menu_surface = pygame.Surface((width, height))
    menu_surface.set_alpha(200)  # Make it semi-transparent
    menu_surface.fill((50, 50, 50))  # Gray background

    clickable_areas = []  # Store clickable areas

    if preset_mode:
        # Render preset options
        title_text = "Select Preset Configuration:"
        title_surface = font.render(title_text, True, (255, 255, 255))
        menu_surface.blit(title_surface, (50, 30))
        
        y_offset = 100
        for i, preset_name in enumerate(preset_configs.keys()):
            color = (255, 255, 255) if preset_name == current_preset else (200, 200, 200)
            preset_surface = font.render(preset_name, True, color)
            menu_surface.blit(preset_surface, (width // 2 - 100, y_offset))
            clickable_areas.append(((width // 2 - 100, y_offset, 200, 40), preset_name))
            y_offset += 60
    else:
        # Render text for each color's interactions
        y_offset = 50
        for color, interactions in color_interactions.items():
            attract_text = f"{color.capitalize()} attracts: {interactions['attract'] or 'None'}"
            repel_text = f"{color.capitalize()} repels: {interactions['repel'] or 'None'}"

            attract_surface = font.render(attract_text, True, (255, 255, 255))
            repel_surface = font.render(repel_text, True, (255, 255, 255))

            menu_surface.blit(attract_surface, (50, y_offset))
            if edit_mode:
                clickable_areas.append(((50, y_offset, 300, 30), color, "attract"))  # Clickable for attract
            y_offset += 40

            menu_surface.blit(repel_surface, (50, y_offset))
            if edit_mode:
                clickable_areas.append(((50, y_offset, 300, 30), color, "repel"))  # Clickable for repel
            y_offset += 60
        
        # Display current preset name
        preset_text = f"Current Preset: {current_preset}"
        preset_surface = font.render(preset_text, True, (255, 255, 0))
        menu_surface.blit(preset_surface, (width - 350, height - 50))

    screen.blit(menu_surface, (0, 0))
    pygame.display.flip()

    return clickable_areas

# Process particle interactions for a specific color
def process_particle_interactions(source_particles, source_color):
    attract_target = color_interactions[source_color]["attract"]
    repel_target = color_interactions[source_color]["repel"]
    
    for source_particle in source_particles:
        # Handle attraction if configured
        if attract_target in particle_lists:
            handle_attraction(source_particle, particle_lists[attract_target])
        
        # Handle repulsion if configured
        if repel_target in particle_lists:
            handle_repulsion(source_particle, particle_lists[repel_target])
        
        # Keep particles within bounds
        keep_within_bounds(source_particle)

# Main game loop
menu_active = False
edit_mode = False
preset_mode = False
clock = pygame.time.Clock()

# Prepare rendering lists once
all_particles = [
    (red_particles, red),
    (yellow_particles, yellow),
    (green_particles, green),
    (orange_particles, orange),
    (cyan_particles, cyan)
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  # Toggle menu with 'M'
                menu_active = not menu_active
                edit_mode = False  # Disable edit mode when toggling the menu
                preset_mode = False  # Disable preset mode when toggling the menu
            elif event.key == pygame.K_p and menu_active:  # Enable edit mode with 'P'
                edit_mode = not edit_mode
                preset_mode = False
            elif event.key == pygame.K_r and menu_active:  # Enable preset mode with 'R' instead of 'P'
                preset_mode = True
                edit_mode = False

        elif event.type == pygame.MOUSEBUTTONDOWN and menu_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if preset_mode:
                clickable_areas = render_menu(edit_mode=False, preset_mode=True)  # Get clickable areas
                for area, preset_name in clickable_areas:
                    x, y, w, h = area
                    if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                        # Apply the selected preset
                        color_interactions = preset_configs[preset_name].copy()
                        current_preset = preset_name
                        break
            elif edit_mode:
                clickable_areas = render_menu(edit_mode=True)  # Get clickable areas
                for area, color, interaction_type in clickable_areas:
                    x, y, w, h = area
                    if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                        # Cycle through the interaction for the clicked color and type
                        current_value = color_interactions[color][interaction_type]
                        if current_value not in interaction_colors:
                            current_value = None  # Default to None if the value is invalid
                        next_index = (interaction_colors.index(current_value) + 1) % len(interaction_colors)
                        color_interactions[color][interaction_type] = interaction_colors[next_index]
                        current_preset = "Custom"  # Change to custom preset when editing
                        break

    if menu_active:
        render_menu(edit_mode=edit_mode, preset_mode=preset_mode)
        continue  # Skip updating particles when the menu is active

    # Process interactions for each color
    process_particle_interactions(red_particles, "red")
    process_particle_interactions(yellow_particles, "yellow")
    process_particle_interactions(green_particles, "green")
    process_particle_interactions(orange_particles, "orange")
    process_particle_interactions(cyan_particles, "cyan")

    # Resolve collisions for all particle types using spatial grid
    resolve_all_collisions(red_particles)
    resolve_all_collisions(yellow_particles)
    resolve_all_collisions(green_particles)
    resolve_all_collisions(orange_particles)
    resolve_all_collisions(cyan_particles)

    # Inter-color collision detection using spatial grid
    all_particles_grid = {}
    
    # Build a combined grid of all particle types
    for color, particles in [("red", red_particles), ("yellow", yellow_particles), 
                            ("green", green_particles), ("orange", orange_particles), 
                            ("cyan", cyan_particles)]:
        for i, particle in enumerate(particles):
            grid_pos = get_grid_position(particle)
            if grid_pos not in all_particles_grid:
                all_particles_grid[grid_pos] = []
            all_particles_grid[grid_pos].append((color, i, particle))
    
    # Check collisions between particles of different colors only within neighboring cells
    processed_pairs = set()
    
    for grid_pos, particles in all_particles_grid.items():
        # Check collisions within this cell
        for i in range(len(particles)):
            color1, idx1, p1 = particles[i]
            for j in range(i + 1, len(particles)):
                color2, idx2, p2 = particles[j]
                if color1 != color2:  # Different colors
                    pair = (color1, idx1, color2, idx2)
                    if pair not in processed_pairs:
                        resolve_collision(p1, p2)
                        processed_pairs.add(pair)
                        processed_pairs.add((color2, idx2, color1, idx1))  # Add reverse pair too
        
        # Check collisions with neighboring cells
        for neighbor_pos in get_neighbor_cells(*grid_pos):
            if neighbor_pos in all_particles_grid and neighbor_pos != grid_pos:
                for color1, idx1, p1 in particles:
                    for color2, idx2, p2 in all_particles_grid[neighbor_pos]:
                        if color1 != color2:  # Different colors
                            pair = (color1, idx1, color2, idx2)
                            if pair not in processed_pairs:
                                resolve_collision(p1, p2)
                                processed_pairs.add(pair)
                                processed_pairs.add((color2, idx2, color1, idx1))  # Add reverse pair too

    # Draw everything
    screen.fill(black)
    
    # Batch rendering for improved performance
    for particles, color in all_particles:
        for particle in particles:
            pygame.draw.circle(screen, color, (int(particle[0]), int(particle[1])), particle_radius)

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS
