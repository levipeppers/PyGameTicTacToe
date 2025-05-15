import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Circle")

# Colors
blue = (0, 0, 255)
tangerine = (242, 133, 0)
white = (255, 255, 255)
grey = (169, 169, 169)
cyan = (0, 255, 255)

# Circle properties
circle_radius = 20
circle_x = circle_radius
circle_y = height - circle_radius - 10
circle_speed = 5

# Dart properties
darts = []
dart_speed = 10

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - circle_y, mouse_x - circle_x)
            darts.append((circle_x, circle_y, angle))

    # Move the circle
    circle_x += circle_speed
    if circle_x > width - circle_radius or circle_x < circle_radius:
        circle_speed = -circle_speed

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate angle between circle center and mouse position
    angle = math.atan2(mouse_y - circle_y, mouse_x - circle_x)

    # Calculate triangle position
    triangle_points = [
        (circle_x + circle_radius * math.cos(angle), circle_y + circle_radius * math.sin(angle)),
        (circle_x + (circle_radius + 20) * math.cos(angle + math.pi / 6), circle_y + (circle_radius + 20) * math.sin(angle + math.pi / 6)),
        (circle_x + (circle_radius + 20) * math.cos(angle - math.pi / 6), circle_y + (circle_radius + 20) * math.sin(angle - math.pi / 6))
    ]

    # Move darts
    for i, (dart_x, dart_y, dart_angle) in enumerate(darts):
        dart_x += dart_speed * math.cos(dart_angle)
        dart_y += dart_speed * math.sin(dart_angle)
        darts[i] = (dart_x, dart_y, dart_angle)

    # Remove darts that are off-screen
    darts = [dart for dart in darts if 0 <= dart[0] <= width and 0 <= dart[1] <= height]

    # Draw everything
    screen.fill(blue)  # Background
    pygame.draw.rect(screen, tangerine, (0, 0, width, 10))  # Top wall
    pygame.draw.rect(screen, tangerine, (0, height - 10, width, 10))  # Bottom wall
    pygame.draw.rect(screen, tangerine, (0, 0, 10, height))  # Left wall
    pygame.draw.rect(screen, tangerine, (width - 10, 0, 10, height))  # Right wall
    pygame.draw.circle(screen, white, (circle_x, circle_y), circle_radius)  # Circle
    pygame.draw.polygon(screen, grey, triangle_points)  # Triangle

    # Draw darts
    for dart_x, dart_y, _ in darts:
        pygame.draw.circle(screen, cyan, (int(dart_x), int(dart_y)), 5)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
