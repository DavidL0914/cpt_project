import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move the Sprite")

# Colors
white = (255, 255, 255)

# Load the sprite sheet
sprite_sheet_url = 'walk.png'  # Make sure this is the correct path to your sprite sheet image
sprite_sheet = pygame.image.load(sprite_sheet_url).convert_alpha()

# Constants for sprite animation
frame_count = 6
sprite_width = sprite_sheet.get_width() // frame_count
sprite_height = sprite_sheet.get_height()
frame_duration = 5  # How many game loops each frame lasts

# Variables
current_frame = 0
frame_ticks = 0
sprite_x = width // 2 - sprite_width // 2
sprite_y = height - sprite_height - 30
sprite_velocity = 5

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press detection
    keys = pygame.key.get_pressed()
    moving = False  # Flag to detect if the sprite is moving

    if keys[pygame.K_LEFT]:
        sprite_x -= sprite_velocity
        moving = True
    if keys[pygame.K_RIGHT]:
        sprite_x += sprite_velocity
        moving = True

    # Boundary checking to keep the sprite within the screen
    if sprite_x < 0:
        sprite_x = 0
    elif sprite_x > width - sprite_width:
        sprite_x = width - sprite_width

    # Update the frame based on the duration and movement
    if moving:
        frame_ticks += 1
        if frame_ticks >= frame_duration:
            frame_ticks = 0
            current_frame = (current_frame + 1) % frame_count
    else:
        # If not moving, reset the animation to the first frame or a standing pose frame
        current_frame = 0  # Reset to first frame or a specific idle frame

    # Extract the current frame from the sprite sheet
    frame_rect = (current_frame * sprite_width, 0, sprite_width, sprite_height)
    frame_image = sprite_sheet.subsurface(frame_rect)

    # Fill the screen with white
    screen.fill(white)

    # Draw the current frame
    screen.blit(frame_image, (sprite_x, sprite_y))

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
