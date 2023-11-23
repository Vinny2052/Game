import pygame
import gif_pygame
import random

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Coffee Run')
clock = pygame.time.Clock()

# Load the new font
bubble_font = pygame.font.Font("font/bul.ttf", 35)

# Button dimensions
button_width = 200
button_height = 200

# Load the button images and resize them to fit the hitbox
button_image = pygame.transform.scale(pygame.image.load("graphics/button.png"), (button_width, button_height))
button_hover_image = pygame.transform.scale(pygame.image.load("graphics/button hover.png"), (button_width, button_height))  # Renamed file
button_click_image = pygame.transform.scale(pygame.image.load("graphics/button click.png"), (button_width, button_height))  # Renamed file

Spike = pygame.image.load("graphics/spike.png")
player = gif_pygame.load("graphics/caB.gif")
Ground = gif_pygame.load("graphics/G.gif")
example_gif = gif_pygame.load("graphics/BG.gif")

# Load the new enemy
flying_eye = gif_pygame.load("graphics/flying_eye.gif")

# Player position
player_x, player_y = 0, 400
# Player speed
speed = 5
# Jump variables
is_jumping = False
jump_speed = 10
gravity = 0.5

# Spike position
spike_x = 600  # Set the spike_x to 600
spike_y = 430

# Flying Eye position
flying_eye_x = 800  # Set the flying_eye_x to 800
flying_eye_y = 200  # Set the flying_eye_y to 200

# Spike speed
spike_speed = 5

# Flying Eye speed
flying_eye_speed = 3

# Game state
game_state = 'title'  # Start with the title screen

# Button position
button_x = 325
button_y = 135

# Define the hitbox dimensions and position
hitbox_width = 220
hitbox_height = 70
hitbox_x = 325 + button_width // 2 - hitbox_width // 2  # Center the hitbox
hitbox_y = 125 + button_height // 2 - hitbox_height // 2  # Center the hitbox

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse click on the hitbox
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if hitbox_x < mouse_x < hitbox_x + hitbox_width and hitbox_y < mouse_y < hitbox_y + hitbox_height:
                game_state = 'game'
                spike_x = 600  # Reset the spike position when the game starts
                flying_eye_x = 800  # Reset the flying_eye position when the game starts

    keys = pygame.key.get_pressed()
    if game_state == 'title':
        # Display title screen
        win.blit(example_gif.blit_ready(), (0, 0))
        win.blit(Ground.blit_ready(), (0, -40)) 
        title_text = bubble_font.render('Coffee Run', True, (0, 0, 0))
        win.blit(title_text, (200, 100))  # Display the title in the middle of the screen

        # Draw the start button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if hitbox_x < mouse_x < hitbox_x + hitbox_width and hitbox_y < mouse_y < hitbox_y + hitbox_height:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button is pressed
                win.blit(button_click_image, (button_x, button_y))
            else:  # Mouse is hovering over the button
                win.blit(button_hover_image, (button_x, button_y))
        else:  # Mouse is not interacting with the button
            win.blit(button_image, (button_x, button_y))

        start_text = bubble_font.render('Start', True, (0, 0, 0))
        win.blit(start_text, (350, 200))

    elif game_state == 'game':
        if keys[pygame.K_SPACE] and not is_jumping:  # Jump
            is_jumping = True
        if keys[pygame.K_d]:  # Move right
            player_x += speed
        if keys[pygame.K_a]:  # Move left
            player_x -= speed

        # Jump physics
        if is_jumping:
            player_y -= jump_speed
            jump_speed -= gravity
            if jump_speed < -10:  # Reset variables when jump is over
                is_jumping = False
                jump_speed = 10

        # Spike movement
        spike_x -= spike_speed
        if spike_x < -50:  # Spike has moved off screen
            spike_x = 650  # Move spike to the right side of the screen
            spike_x = random.randint(300, 600)  # Randomly position spike vertically with a minimum distance of 300px

        # Flying Eye movement
        flying_eye_x -= flying_eye_speed
        if flying_eye_x < -50:  # Flying Eye has moved off screen
            flying_eye_x = 850  # Move Flying Eye to the right side of the screen
            flying_eye_y = random.randint(100, 300)  # Randomly position Flying Eye vertically

        # Check for collision with spike
        if abs(player_x - spike_x) < 50 and abs(player_y - spike_y) < 50:  # Adjust collision detection as needed
            print("Game Over")
            game_state = 'title'  # Go back to the title screen when the player dies
            spike_x = 600  # Reset the spike position when the player dies

        # Check for collision with Flying Eye
        if abs(player_x - flying_eye_x) < 50 and abs(player_y - flying_eye_y) < 50:  # Adjust collision detection as needed
            print("Game Over")
            game_state = 'title'  # Go back to the title screen when the player dies
            flying_eye_x = 800  # Reset the Flying Eye position when the player dies

        win.blit(example_gif.blit_ready(), (0, 0))
        win.blit(Ground.blit_ready(), (0, -40))
        win.blit(player.blit_ready(), (player_x, player_y))
        win.blit(Spike, (spike_x, spike_y))
        win.blit(flying_eye.blit_ready(), (flying_eye_x, flying_eye_y))  # Draw the Flying Eye

    pygame.display.flip()
    clock.tick(60)
