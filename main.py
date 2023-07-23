import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Set the window dimensions
window_width, window_height = 1200, 600

# Set up the game window
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define colors (RGB format)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Snake properties
snake_block = 10
snake_speed = 70

# Create the Snake
snake = [(window_width // 2, window_height // 2)]
dx, dy = 0, 0

# Food position
food_pos = (random.randrange(0, window_width - snake_block, snake_block),
            random.randrange(0, window_height - snake_block, snake_block))

# Score
score = 0

# Highest score
highest_score = 0

# Timer to control the blinking of the food
blink_timer = pygame.time.get_ticks()

def read_highest_score():
    if os.path.exists("highest_score.txt"):
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    return 0

def write_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))

def draw_snake(win, snake, snake_block):
    for segment in snake:
        pygame.draw.rect(win, green, [segment[0], segment[1], snake_block, snake_block])

def draw_food(win, food_pos, snake_block):
    global blink_timer
    current_time = pygame.time.get_ticks()
    # Toggle the visibility of the food every 0.6 seconds
    if current_time - blink_timer >= 600:
        blink_timer = current_time
        pygame.draw.rect(win, red, [food_pos[0], food_pos[1], snake_block, snake_block])

def display_score(win, score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, white)
    win.blit(text, (10, 10))

def display_highest_score(win, highest_score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Highest Score: " + str(highest_score), True, white)
    win.blit(text, (10, 30))

def draw_boundary(win):
    pygame.draw.rect(win, yellow, [0, 0, window_width, snake_block])  # Top boundary
    pygame.draw.rect(win, yellow, [0, window_height - snake_block, window_width, snake_block])  # Bottom boundary
    pygame.draw.rect(win, yellow, [0, 0, snake_block, window_height])  # Left boundary
    pygame.draw.rect(win, yellow, [window_width - snake_block, 0, snake_block, window_height])  # Right boundary

def is_inside_button(pos, button_rect):
    x, y = pos
    button_x, button_y, button_width, button_height = button_rect
    return button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height

def toggle_game_state():
    global is_playing
    is_playing = not is_playing

def draw_buttons(win):
    # Play button
    button_width, button_height = 100, 50
    button_color = (100, 100, 100)
    button_text_color = (255, 255, 255)

    play_button_rect = pygame.draw.rect(win, button_color, [window_width // 4 - button_width // 2, window_height - button_height - 20, button_width, button_height])
    font = pygame.font.SysFont(None, 25)
    text = font.render("Play", True, button_text_color)
    win.blit(text, (window_width // 4 - button_width // 4, window_height - button_height // 2 - 20))

    # Pause button
    pause_button_rect = pygame.draw.rect(win, button_color, [window_width * 3 // 4 - button_width // 2, window_height - button_height - 20, button_width, button_height])
    text = font.render("Pause", True, button_text_color)
    win.blit(text, (window_width * 3 // 4 - button_width // 4, window_height - button_height // 2 - 20))

    return play_button_rect, pause_button_rect

def draw_menu(win):
    # New Game button
    button_width, button_height = 200, 50
    button_color = (100, 100, 100)
    button_text_color = (255, 255, 255)

    new_game_button_rect = pygame.draw.rect(win, button_color, [window_width // 2 - button_width // 2, window_height // 2 - 2 * button_height, button_width, button_height])
    font = pygame.font.SysFont(None, 30)
    text = font.render(" New Game", True, button_text_color)
    win.blit(text, (window_width // 2 - button_width // 4, window_height // 2 - 2 * button_height // 1.2))

    # Continue button
    continue_button_rect = pygame.draw.rect(win, button_color, [window_width // 2 - button_width // 2, window_height // 2, button_width, button_height])
    text = font.render(" Continue Game  ", True, button_text_color)
    win.blit(text, (window_width // 2 - button_width // 2.5, window_height // 2 - button_height // 150))

    # End button
    end_button_rect = pygame.draw.rect(win, button_color, [window_width // 2 - button_width // 2, window_height // 2 + 2 * button_height, button_width, button_height])
    text = font.render("    End", True, button_text_color)
    win.blit(text, (window_width // 2 - button_width // 4, window_height // 2 + 2 * button_height // 0.85))

    return new_game_button_rect, continue_button_rect, end_button_rect

def game_loop():
    global snake, dx, dy, food_pos, score, highest_score, blink_timer, is_playing

    highest_score = read_highest_score()

    # Load and resize the background image
    background_image = pygame.image.load("image/background.png")  # Replace "background.jpg" with your image filename
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

    # Play and Pause button properties
    button_width, button_height = 100, 50
    button_color = (0, 0, 0)
    button_text_color = (255, 255, 255)

    is_playing = True

    menu_screen = True
    play_button_rect, pause_button_rect = draw_buttons(win)
    new_game_button_rect, continue_button_rect, end_button_rect = draw_menu(win)

    while menu_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game if the "X" button is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_inside_button(event.pos, new_game_button_rect):
                    # Start a new game
                    menu_screen = False
                elif is_inside_button(event.pos, continue_button_rect):
                    # Continue the previous game
                    menu_screen = False
                    is_playing = True
                elif is_inside_button(event.pos, end_button_rect):
                    # End the game
                    pygame.quit()

        win.blit(background_image, (0, 0))  # Blit the background image
        draw_menu(win)  # Draw the menu buttons

        pygame.display.update()

    if not menu_screen:
        game_over = False
        snake = [(window_width // 2, window_height // 2)]
        dx, dy = 0, 0
        score = 0
        food_pos = (random.randrange(0, window_width - snake_block, snake_block),
                    random.randrange(0, window_height - snake_block, snake_block))

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx, dy = -snake_block, 0
                    elif event.key == pygame.K_RIGHT:
                        dx, dy = snake_block, 0
                    elif event.key == pygame.K_UP:
                        dx, dy = 0, -snake_block
                    elif event.key == pygame.K_DOWN:
                        dx, dy = 0, snake_block
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if is_inside_button(event.pos, play_button_rect):
                        toggle_game_state()
                    elif is_inside_button(event.pos, pause_button_rect):
                        toggle_game_state()

            # Update the game logic if playing
            if is_playing:
                # Update snake position and other game logic
                head_x, head_y = snake[-1]
                new_head = (head_x + dx, head_y + dy)

                # Check for collision with boundaries
                if new_head[0] < 0 or new_head[0] >= window_width or new_head[1] < 0 or new_head[1] >= window_height:
                    game_over = True

                snake.append(new_head)

                # Check for collision with food
                if new_head == food_pos:
                    score += 1
                    food_pos = (random.randrange(0, window_width - snake_block, snake_block),
                                random.randrange(0, window_height - snake_block, snake_block))
                else:
                    # Remove tail segment
                    if len(snake) > 1:
                        snake.pop(0)

            # Draw the window and game elements
            win.blit(background_image, (0, 0))  # Blit the background image
            draw_boundary(win)  # Draw the boundary
            draw_snake(win, snake, snake_block)
            draw_food(win, food_pos, snake_block)
            display_score(win, score)
            display_highest_score(win, highest_score)
            draw_buttons(win)  # Draw the play and pause buttons

            # Check for collision with itself
            if is_playing and new_head in snake[:-1]:
                game_over = True

            # Update the display
            pygame.display.update()

            # Set the game speed
            pygame.time.delay(snake_speed)

        # Update the highest score if needed
        if score > highest_score:
            highest_score = score
            write_highest_score(highest_score)

        # Game Over message
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, white)
        win.blit(text, (window_width // 2 - 100, window_height // 2))
        pygame.display.update()

        # Wait for a few seconds before quitting the game
        time.sleep(3)

        pygame.quit()

if __name__ == "__main__":
    game_loop()
