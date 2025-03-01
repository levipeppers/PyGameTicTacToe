import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 600  # Increase width to accommodate the green bar
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 10
BAR_WIDTH = 100
BAR_COLOR = (0, 128, 0)  # Darker green

# Constants for X and O
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
CELL_SIZE = (WIDTH - BAR_WIDTH) // 3  # Adjust cell size to exclude the bar

# Grid state
grid = [[None, None, None], [None, None, None], [None, None, None]]

# Points
points = 0

# Hardcore mode
hardcore_mode = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Font for displaying points
font = pygame.font.SysFont(None, 48)

def draw_grid():
    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)
    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH - BAR_WIDTH, HEIGHT // 3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH - BAR_WIDTH, 2 * HEIGHT // 3), LINE_WIDTH)

def draw_xo():
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 'X':
                draw_x(row, col)
            elif grid[row][col] == 'O':
                draw_o(row, col)

def draw_x(row, col):
    start_pos = (col * CELL_SIZE + 20, row * CELL_SIZE + 20)
    end_pos = ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20)
    pygame.draw.line(screen, X_COLOR, start_pos, end_pos, LINE_WIDTH)
    start_pos = (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20)
    end_pos = ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20)
    pygame.draw.line(screen, X_COLOR, start_pos, end_pos, LINE_WIDTH)

def draw_o(row, col):
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, O_COLOR, center, CELL_SIZE // 2 - 20, LINE_WIDTH)

def draw_bar():
    pygame.draw.rect(screen, BAR_COLOR, (WIDTH - BAR_WIDTH, 0, BAR_WIDTH, HEIGHT))
    points_text = font.render(str(points), True, (255, 255, 255))
    outline_color = (0, 0, 0) if points >= 0 else (255, 0, 0)
    outline_text = font.render(str(points), True, outline_color)
    screen.blit(outline_text, (WIDTH - BAR_WIDTH + 10, 10))
    screen.blit(points_text, (WIDTH - BAR_WIDTH + 10, 10))
    draw_hardcore_button()

def draw_hardcore_button():
    button_color = (0, 255, 0) if not hardcore_mode else (255, 255, 255)
    pygame.draw.circle(screen, button_color, (WIDTH - BAR_WIDTH + 50, HEIGHT - 35), 25)
    if hardcore_mode:
        pygame.draw.polygon(screen, (0, 0, 0), [(WIDTH - BAR_WIDTH + 35, HEIGHT - 45), (WIDTH - BAR_WIDTH + 65, HEIGHT - 45), (WIDTH - BAR_WIDTH + 50, HEIGHT - 25)])

def handle_click(pos):
    global points, hardcore_mode
    if pos[0] < WIDTH - BAR_WIDTH:  # Ignore clicks on the bar
        row = pos[1] // CELL_SIZE
        col = pos[0] // CELL_SIZE
        if grid[row][col] is None:
            grid[row][col] = 'O'
            place_random_x()
            if hardcore_mode:
                place_random_x()
            check_winner()
    elif WIDTH - BAR_WIDTH + 25 <= pos[0] <= WIDTH - BAR_WIDTH + 75 and HEIGHT - 60 <= pos[1] <= HEIGHT - 10:
        hardcore_mode = not hardcore_mode

def place_random_x():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if grid[r][c] is None]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 'X'

def check_winner():
    global points
    for row in range(3):
        if grid[row][0] == grid[row][1] == grid[row][2] and grid[row][0] is not None:
            update_points(grid[row][0])
            reset_board()
            return
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] and grid[0][col] is not None:
            update_points(grid[0][col])
            reset_board()
            return
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] is not None:
        update_points(grid[0][0])
        reset_board()
        return
    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] is not None:
        update_points(grid[0][2])
        reset_board()
        return
    if all(grid[row][col] is not None for row in range(3) for col in range(3)):
        reset_board()

def update_points(winner):
    global points
    if winner == 'O':
        points += 1
    elif winner == 'X':
        points -= 1

def reset_board():
    global grid
    grid = [[None, None, None], [None, None, None], [None, None, None]]

def main():
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the grid
        draw_grid()
        draw_xo()

        # Draw the green bar
        draw_bar()

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
