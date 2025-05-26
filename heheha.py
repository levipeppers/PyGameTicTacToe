import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Glitch")

# Colors
black = (0, 0, 0)
tan = (210, 180, 140)  # New background color
grey = (100, 100, 100)
green = (0, 255, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Player properties
player_radius = 20
player_speed = 5
player_health = 100
player_stamina = 70
stamina_regen_rate = 1  # Stamina regenerates per frame
sprint_stamina_cost = 2  # Stamina cost per frame while sprinting
stamina_boost_duration = 10 * 60  # 10 seconds in frames
stamina_boost_active = False
stamina_boost_timer = 0

# Boss properties
boss_radius = int(player_radius * 1.5)
boss_speed = player_speed * 1.2  # Ensure boss speed is 1.2x player speed
boss_x, boss_y = random.randint(0, width), random.randint(0, height)
boss_cooldowns = {"slash": 60, "spawn": 600, "lunge": 1}  # Cooldowns in frames
boss_last_used = {"slash": 0, "spawn": 0, "lunge": False}
burning_timer = 0
burning_active = False
minions = []

# Adjusted boss movement cooldown
boss_movement_cooldown = int(60 / 2.7)  # 2.7x faster movement cooldown

# Minion properties
minion_radius = 10
minion_speed = player_speed * 0.8
minion_lifetime = 300  # Minions live for 5 seconds (300 frames)

# Menu options
menu_options = ["Buggy Spawn", "Option 2", "Option 3"]
selected_option = 0

# Menu selection delay
menu_selection_delay = 10  # Frames to wait between menu selections
menu_last_selection = 0

# Game state
in_menu = True
player_x, player_y = width // 2, height // 2

# Timer properties
game_duration = 120  # 2 minutes in seconds
time_remaining = game_duration

# Coin system
coins = 0

# Helper function to draw text
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Helper function to draw health and stamina meters
def draw_meters(health, stamina):
    pygame.draw.rect(screen, red, (10, height - 50, 200, 20))  # Health bar background
    pygame.draw.rect(screen, green, (10, height - 50, 2 * health, 20))  # Health bar
    draw_text(f"HP: {int(health)}", small_font, white, 220, height - 50)  # Remove decimals

    pygame.draw.rect(screen, blue, (10, height - 25, 200, 20))  # Stamina bar background
    pygame.draw.rect(screen, white, (10, height - 25, 2 * stamina, 20))  # Stamina bar
    draw_text(f"Stam: {int(stamina)}", small_font, white, 220, height - 25)  # Remove decimals

# Helper function to draw burning status
def draw_burning_status():
    if burning_active:
        draw_text("YOU'RE BURNING", small_font, red, 10, height - 80)

# Helper function to draw the timer
def draw_timer(time_remaining):
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    timer_text = f"Time: {minutes:02}:{seconds:02}"
    draw_text(timer_text, font, white, width // 2 - 100, 10)

# Helper function to display "You Win!" message
def display_win_message():
    screen.fill(tan)
    draw_text("YOU WIN!", font, green, width // 2 - 100, height // 2 - 50)
    pygame.display.flip()
    pygame.time.delay(3000)  # Display for 3 seconds

# Helper function to display coins
def draw_coins(coins):
    coin_text = f"Coins: ${coins}"
    draw_text(coin_text, font, white, 10, 10)

# Helper function to handle end-of-game rewards
def handle_rewards(win, time_remaining):
    global coins
    if win:
        coins += 40  # Add $40 for a win
    elif time_remaining > 90:  # Loss under 30 seconds
        coins += 10  # Add $10 for a quick loss

# Main game loop
clock = pygame.time.Clock()
frame_count = 0
while True:
    screen.fill(tan)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if in_menu:
        # Menu logic
        if frame_count - menu_last_selection > menu_selection_delay:
            if keys[pygame.K_w]:  # Move up in menu
                selected_option = (selected_option - 1) % len(menu_options)
                menu_last_selection = frame_count
            elif keys[pygame.K_s]:  # Move down in menu
                selected_option = (selected_option + 1) % len(menu_options)
                menu_last_selection = frame_count

        for i, option in enumerate(menu_options):
            color = grey if i != selected_option else white
            draw_text(option, font, color, width // 2 - 100, height // 2 - 100 + i * 60)

        if keys[pygame.K_RETURN]:  # Select menu option
            if selected_option == 0:  # "Buggy Spawn"
                in_menu = False
                player_health = 100  # Reset health
                player_stamina = 70  # Reset stamina
                boss_x, boss_y = random.randint(0, width), random.randint(0, height)  # Reset boss position
                minions.clear()  # Clear minions
                time_remaining = game_duration  # Reset timer
    else:
        # Game logic
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed

        # Sprint logic
        if keys[pygame.K_LSHIFT] and player_stamina > 0:
            player_speed = 8.5  # 1.7x normal speed
            player_stamina = max(0, player_stamina - sprint_stamina_cost / 60)
        else:
            player_speed = 5
            player_stamina = min(70 if not stamina_boost_active else 90, player_stamina + stamina_regen_rate / 60)

        # Stamina boost logic
        if keys[pygame.K_q] and not stamina_boost_active:
            stamina_boost_active = True
            stamina_boost_timer = stamina_boost_duration
            player_stamina = 90  # Max stamina increased to 90
            player_health -= 30

        if stamina_boost_active:
            stamina_boost_timer -= 1
            if stamina_boost_timer <= 0:
                stamina_boost_active = False
                player_stamina = min(70, player_stamina)

        # Boss logic
        if frame_count % boss_movement_cooldown == 0:  # Boss moves toward the player every cooldown
            dx, dy = player_x - boss_x, player_y - boss_y
            dist = math.hypot(dx, dy)
            if dist > 0:
                boss_x += boss_speed * dx / dist
                boss_y += boss_speed * dy / dist

        # Boss abilities
        if frame_count - boss_last_used["slash"] > boss_cooldowns["slash"]:
            if math.hypot(player_x - boss_x, player_y - boss_y) < boss_radius + player_radius:
                burning_active = True
                burning_timer = 180  # 3 seconds
                boss_last_used["slash"] = frame_count

        if burning_active:
            burning_timer -= 1
            player_health -= 3 / 60  # 3 damage per second
            if burning_timer <= 0:
                burning_active = False

        if frame_count - boss_last_used["spawn"] > boss_cooldowns["spawn"]:
            for _ in range(3):  # Spawn 3 minions
                minion_x = random.randint(0, width)
                minion_y = random.randint(0, height)
                minions.append({"x": minion_x, "y": minion_y, "active": True, "lifetime": minion_lifetime})
            boss_last_used["spawn"] = frame_count

        if not boss_last_used["lunge"] and frame_count % 600 == 0:  # Lunge once
            dx, dy = player_x - boss_x, player_y - boss_y
            dist = math.hypot(dx, dy)
            if dist > 0:
                boss_x += 3 * boss_speed * dx / dist
                boss_y += 3 * boss_speed * dy / dist
                player_health -= 30
                boss_last_used["lunge"] = True

        # Minion logic
        for minion in minions:
            if minion["active"]:
                dx, dy = player_x - minion["x"], player_y - minion["y"]
                dist = math.hypot(dx, dy)
                if dist > 0:
                    minion["x"] += minion_speed * dx / dist
                    minion["y"] += minion_speed * dy / dist
                if dist < player_radius + minion_radius:
                    player_health -= 10
                    minion["active"] = False
                minion["lifetime"] -= 1
                if minion["lifetime"] <= 0:
                    minion["active"] = False

        # Check if player is dead
        if player_health <= 0:
            handle_rewards(win=False, time_remaining=time_remaining)  # Handle loss rewards
            in_menu = True  # Return to menu
            continue

        # Update timer
        if frame_count % 60 == 0:  # Decrease time every second
            time_remaining -= 1
            if time_remaining <= 0:
                handle_rewards(win=True, time_remaining=time_remaining)  # Handle win rewards
                display_win_message()  # Show "You Win!" message
                in_menu = True  # Return to menu
                continue

        # Draw boss
        pygame.draw.circle(screen, red, (int(boss_x), int(boss_y)), boss_radius)

        # Draw minions
        for minion in minions:
            if minion["active"]:
                pygame.draw.circle(screen, (139, 0, 0), (int(minion["x"]), int(minion["y"])), minion_radius)

        # Draw player
        pygame.draw.circle(screen, green, (player_x, player_y), player_radius)

        # Draw health and stamina meters
        draw_meters(player_health, player_stamina)

        # Draw burning status
        draw_burning_status()

        # Draw timer
        draw_timer(time_remaining)

        # Draw coins
        draw_coins(coins)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1
