import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
ASTEROID_SIZE = 64

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Game")

# Load images
ship_image = pygame.transform.scale(pygame.image.load('spaceship.png'), (50, 50))
asteroid_image = pygame.image.load('asteroid.png')

# Ship class
class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        rotated_image = pygame.transform.rotate(ship_image, 0)
        new_rect = rotated_image.get_rect(center=ship_image.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

# Bullet class
class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 5
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

# Asteroid class
class Asteroid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-2, 2)
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self):
        asteroid_scaled = pygame.transform.scale(asteroid_image, (self.size, self.size))
        screen.blit(asteroid_scaled, (self.x, self.y))

# Game initialization
ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
bullets = []
asteroids = []

# Helper functions
def handle_bullets():
    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)
        else:
            bullet.draw()

def handle_asteroids():
    for asteroid in asteroids[:]:
        asteroid.move()
        if asteroid.x + asteroid.size < 0 or asteroid.x > SCREEN_WIDTH or asteroid.y + asteroid.size < 0 or asteroid.y > SCREEN_HEIGHT:
            asteroids.remove(asteroid)
        else:
            asteroid.draw()

def handle_collisions():
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            distance = math.sqrt((bullet.x - asteroid.x)**2 + (bullet.y - asteroid.y)**2)
            if distance < asteroid.size / 2 + bullet.radius:
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                break

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - ship.x, my - ship.y
            distance = math.hypot(dx, dy)
            dx, dy = dx / distance, dy / distance
            bullets.append(Bullet(ship.x, ship.y, dx * 10, dy * 10))
    
    ship.draw()
    handle_bullets()
    handle_asteroids()
    handle_collisions()
    
    # Spawn new asteroids
    if len(asteroids) < 10:
        if random.random() < 0.02:
            size = random.choice([30, 50, 70])
            x, y = random.choice([(-size, random.randint(0, SCREEN_HEIGHT)),
                                  (SCREEN_WIDTH + size, random.randint(0, SCREEN_HEIGHT)),
                                  (random.randint(0, SCREEN_WIDTH), -size),
                                  (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + size)])
            asteroids.append(Asteroid(x, y, size))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
