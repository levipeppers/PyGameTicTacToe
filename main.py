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
gems = 0

# Modes
mode = 0  # 0: Normal, 1: Hardcore, 2: Double Hardcore
block_pos = None

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Font for displaying points
font = pygame.font.SysFont(None, 48)

# Leaderboard data
leaderboard = []
input_name = ""
input_active = False
shop_active = False
selected_symbol = None
owned_skins = {'O': True, 'T': True, 'S': False, 'D': False}

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
            elif grid[row][col] == 'T':
                draw_t(row, col)
            elif grid[row][col] == 'S':
                draw_s(row, col)
            elif grid[row][col] == 'D':
                draw_d(row, col)

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

def draw_t(row, col):
    pygame.draw.polygon(screen, (255, 255, 0), [(col * CELL_SIZE + 20, row * CELL_SIZE + 20), (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + CELL_SIZE // 2), (col * CELL_SIZE + 20, row * CELL_SIZE + CELL_SIZE - 20)], 5)

def draw_s(row, col):
    pygame.draw.polygon(screen, (255, 105, 180), [(col * CELL_SIZE + 20, row * CELL_SIZE + 20), (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + CELL_SIZE // 2), (col * CELL_SIZE + 20, row * CELL_SIZE + CELL_SIZE - 20)], 5)

def draw_d(row, col):
    pygame.draw.rect(screen, (0, 255, 0), (col * CELL_SIZE + 20, row * CELL_SIZE + 20, CELL_SIZE - 40, CELL_SIZE - 40), 5)

def draw_bar():
    pygame.draw.rect(screen, BAR_COLOR, (WIDTH - BAR_WIDTH, 0, BAR_WIDTH, HEIGHT))
    points_text = font.render(str(points), True, (255, 255, 255))
    outline_color = (0, 0, 0) if points >= 0 else (255, 0, 0)
    outline_text = font.render(str(points), True, outline_color)
    screen.blit(outline_text, (WIDTH - BAR_WIDTH + 10, 10))
    screen.blit(points_text, (WIDTH - BAR_WIDTH + 10, 10))
    draw_mode_button()

def draw_mode_button():
    if mode == 0:
        button_color = (0, 255, 0)
    elif mode == 1:
        button_color = (255, 0, 0)
    else:
        button_color = (255, 105, 180)  # Brighter, more violet pink
    pygame.draw.circle(screen, button_color, (WIDTH - BAR_WIDTH + 50, HEIGHT - 70), 25)
    if mode == 1:
        pygame.draw.polygon(screen, (255, 255, 255), [(WIDTH - BAR_WIDTH + 35, HEIGHT - 80), (WIDTH - BAR_WIDTH + 65, HEIGHT - 80), (WIDTH - BAR_WIDTH + 50, HEIGHT - 60)])
    elif mode == 2:
        pygame.draw.line(screen, (255, 255, 255), (WIDTH - BAR_WIDTH + 35, HEIGHT - 70), (WIDTH - BAR_WIDTH + 65, HEIGHT - 70), 5)
        pygame.draw.line(screen, (255, 255, 255), (WIDTH - BAR_WIDTH + 50, HEIGHT - 85), (WIDTH - BAR_WIDTH + 50, HEIGHT - 55), 5)
        pygame.draw.line(screen, (255, 255, 255), (WIDTH - BAR_WIDTH + 35, HEIGHT - 85), (WIDTH - BAR_WIDTH + 65, HEIGHT - 55), 5)
        pygame.draw.line(screen, (255, 255, 255), (WIDTH - BAR_WIDTH + 65, HEIGHT - 85), (WIDTH - BAR_WIDTH + 35, HEIGHT - 55), 5)

def draw_leaderboard_button():
    pygame.draw.circle(screen, (255, 255, 0), (WIDTH - BAR_WIDTH + 50, HEIGHT - 120), 15)

def draw_shop_button():
    pygame.draw.circle(screen, (0, 0, 255), (WIDTH - BAR_WIDTH + 50, HEIGHT - 170), 15)

def draw_leave_button():
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH - 60, 10, 50, 30))

def draw_leaderboard():
    screen.fill((0, 0, 0))
    headers = ["Name", "Mode", "Score"]
    for i, header in enumerate(headers):
        text = font.render(header, True, (255, 255, 0))
        screen.blit(text, (i * 200 + 50, 50))
    for row, entry in enumerate(leaderboard):
        for col, item in enumerate(entry):
            text = font.render(str(item), True, (255, 255, 0))
            screen.blit(text, (col * 200 + 50, 100 + row * 50))
    draw_leave_button()

def draw_shop():
    screen.fill((0, 100, 0))  # Dark green background
    for row in range(4):
        for col in range(4):
            pygame.draw.rect(screen, (0, 0, 0), (col * 80 + 200, row * 80 + 50, 70, 70))
    pygame.draw.circle(screen, O_COLOR, (200 + 35, 50 + 35), 30, 5)  # Hollow blue circle in top-left corner
    pygame.draw.polygon(screen, (255, 255, 0), [(280, 50), (320, 90), (280, 130)], 5)  # Hollow yellow triangle in second square
    pygame.draw.polygon(screen, (255, 105, 180), [(360, 50), (380, 70), (400, 50), (420, 70), (400, 90), (420, 110), (400, 130), (380, 110), (360, 130), (380, 90)], 5)  # Hollow pink star in third square
    pygame.draw.rect(screen, (0, 255, 0), (440, 50, 70, 70), 5)  # Hollow green dollar sign in fourth square
    pygame.draw.rect(screen, (255, 255, 255), (50, 50, 150, 150))  # Big white square for selected symbol
    if selected_symbol == 'O':
        pygame.draw.circle(screen, O_COLOR, (125, 125), 60, 5)  # Hollow blue circle in big square
    elif selected_symbol == 'T':
        pygame.draw.polygon(screen, (255, 255, 0), [(85, 85), (165, 125), (85, 165)], 5)  # Hollow yellow triangle in big square
    elif selected_symbol == 'S':
        pygame.draw.polygon(screen, (255, 105, 180), [(85, 85), (105, 105), (125, 85), (145, 105), (125, 125), (145, 145), (125, 165), (105, 145), (85, 165), (105, 125)], 5)  # Hollow pink star in big square
    elif selected_symbol == 'D':
        pygame.draw.rect(screen, (0, 255, 0), (85, 85, 80, 80), 5)  # Hollow green dollar sign in big square
        pygame.draw.line(screen, (0, 255, 0), (105, 105), (145, 145), 5)
        pygame.draw.line(screen, (0, 255, 0), (145, 105), (105, 145), 5)
    equip_text = None
    if selected_symbol in owned_skins and owned_skins[selected_symbol]:
        pygame.draw.rect(screen, (255, 255, 255), (200, 400, 100, 50))  # Equip button
        equip_text = font.render("Equip", True, (0, 0, 0))
    else:
        if selected_symbol == 'S':
            pygame.draw.rect(screen, (0, 255, 0), (200, 400, 100, 50))  # Buy button
            equip_text = font.render("Buy: 2", True, (0, 0, 0))
        elif selected_symbol == 'D':
            pygame.draw.rect(screen, (0, 255, 0), (200, 400, 100, 50))  # Buy button
            equip_text = font.render("Buy: 100", True, (0, 0, 0))
    if equip_text:
        screen.blit(equip_text, (220, 415))
    draw_leave_button()
    gems_text = font.render(f"Gems: {gems}", True, (255, 255, 255))
    screen.blit(gems_text, (10, 10))

def handle_click(pos):
    global points, mode, block_pos, input_active, shop_active, in_leaderboard
    if pos[0] < WIDTH - BAR_WIDTH:  # Ignore clicks on the bar
        row = pos[1] // CELL_SIZE
        col = pos[0] // CELL_SIZE
        if grid[row][col] is None and (block_pos is None or (row, col) != block_pos):
            if selected_symbol == 'O':
                grid[row][col] = 'O'
            elif selected_symbol == 'T':
                grid[row][col] = 'T'
            elif selected_symbol == 'S' and owned_skins['S']:
                grid[row][col] = 'S'
            elif selected_symbol == 'D' and owned_skins['D']:
                grid[row][col] = 'D'
            else:
                grid[row][col] = 'O'
            place_random_x()
            if mode == 1:
                place_random_x()
                move_block()
            elif mode == 2:
                move_block()
            check_winner()
            if all(grid[row][col] is not None for row in range(3) for col in range(3)):
                reset_board()
    elif WIDTH - BAR_WIDTH + 35 <= pos[0] <= WIDTH - BAR_WIDTH + 65 and HEIGHT - 135 <= pos[1] <= HEIGHT - 105:
        input_active = True
    elif WIDTH - BAR_WIDTH + 25 <= pos[0] <= WIDTH - BAR_WIDTH + 75 and HEIGHT - 95 <= pos[1] <= HEIGHT - 45:
        mode = (mode + 1) % 3
        if mode == 1 or mode == 2:
            move_block()
    elif WIDTH - BAR_WIDTH + 35 <= pos[0] <= WIDTH - BAR_WIDTH + 65 and HEIGHT - 185 <= pos[1] <= HEIGHT - 155:
        shop_active = True
    elif WIDTH - 60 <= pos[0] <= WIDTH - 10 and 10 <= pos[1] <= 40:
        in_leaderboard = False

def handle_leaderboard_click(pos):
    global in_leaderboard
    if WIDTH - 60 <= pos[0] <= WIDTH - 10 and 10 <= pos[1] <= 40:
        in_leaderboard = False
    return False

def handle_shop_click(pos):
    global shop_active, selected_symbol, gems
    if WIDTH - 60 <= pos[0] <= WIDTH - 10 and 10 <= pos[1] <= 40:
        shop_active = False
    elif 200 <= pos[0] <= 270 and 50 <= pos[1] <= 120:
        selected_symbol = 'O'
    elif 280 <= pos[0] <= 350 and 50 <= pos[1] <= 120:
        selected_symbol = 'T'
    elif 360 <= pos[0] <= 430 and 50 <= pos[1] <= 120:
        selected_symbol = 'S'
    elif 440 <= pos[0] <= 510 and 50 <= pos[1] <= 120:
        selected_symbol = 'D'
    elif 200 <= pos[0] <= 300 and 400 <= pos[1] <= 450:
        if selected_symbol in owned_skins and owned_skins[selected_symbol]:
            shop_active = False
        elif selected_symbol == 'S' and gems >= 2:
            gems -= 2
            owned_skins['S'] = True
        elif selected_symbol == 'D' and gems >= 100:
            gems -= 100
            owned_skins['D'] = True
        else:
            selected_symbol = None

def handle_leaderboard_input(event):

    global input_name, points, input_active, gems
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if len(input_name) == 2 and input_name.isalpha():
                mode_color = {0: "Green", 1: "Red", 2: "Pink"}[mode]
                leaderboard.append([input_name, mode_color, points])
                leaderboard.sort(key=lambda x: x[2], reverse=True)
                if len(leaderboard) > 7:
                    leaderboard.pop()
                gems += points // 5
                points = 0
                input_name = ""
                input_active = False
        elif event.key == pygame.K_BACKSPACE:
            input_name = input_name[:-1]
        elif len(input_name) < 2 and event.unicode.isalpha():
            input_name += event.unicode.upper()

def place_random_x():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if grid[r][c] is None and (block_pos is None or (r, c) != block_pos)]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 'X'
    else:
        reset_board()

def move_block():
    global block_pos
    empty_cells = [(r, c) for r in range(3) for c in range(3) if grid[r][c] is None]
    if empty_cells:
        block_pos = random.choice(empty_cells)

def draw_block():
    if block_pos and mode == 2:
        row, col = block_pos
        pygame.draw.rect(screen, (255, 165, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Orange blinding square

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
    if winner == 'O' or winner == 'T':
        points += 1
    elif winner == 'X':
        points -= 1

def reset_board():
    global grid, block_pos
    grid = [[None, None, None], [None, None, None], [None, None, None]]
    block_pos = None

def handle_hover(pos):
    if 200 <= pos[0] <= 270 and 50 <= pos[1] <= 120:
        pygame.draw.circle(screen, (0, 0, 255), (125, 125), 30)  # Blue circle in big square
    elif 300 <= pos[0] <= 370 and 50 <= pos[1] <= 120:
        pygame.draw.polygon(screen, (255, 255, 0), [(125, 85), (165, 125), (125, 165)])  # Yellow triangle in big square

def main():
    global input_active, shop_active, in_leaderboard
    in_leaderboard = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if in_leaderboard:
                    handle_leaderboard_click(event.pos)
                elif shop_active:
                    handle_shop_click(event.pos)
                elif WIDTH - BAR_WIDTH + 35 <= event.pos[0] <= WIDTH - BAR_WIDTH + 65 and HEIGHT - 135 <= event.pos[1] <= HEIGHT - 105:
                    in_leaderboard = True
                    input_active = True
                else:
                    handle_click(event.pos)
            elif input_active:
                handle_leaderboard_input(event)
            elif event.type == pygame.MOUSEMOTION and shop_active:
                handle_hover(event.pos)

        if in_leaderboard:
            draw_leaderboard()
        elif shop_active:
            draw_shop()
        else:
            screen.fill((0, 0, 0))
            draw_grid()
            draw_xo()
            draw_block()
            draw_bar()
            draw_leaderboard_button()
            draw_shop_button()
            if input_active:
                name_text = font.render(input_name, True, (255, 255, 255))
                screen.blit(name_text, (WIDTH - BAR_WIDTH + 10, HEIGHT - 120))
        pygame.display.flip()

if __name__ == "__main__":
    main()
