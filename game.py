import pygame
import random
import math
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
ASTEROID_SIZES = [30, 50, 70]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Game")

ship_image = pygame.transform.scale(pygame.image.load('spaceship.png'), (50, 50))
asteroid_image = pygame.image.load('asteroid.png')
laser_image = pygame.transform.scale(pygame.image.load('laser.png'), (40, 20))

font = pygame.font.Font(None, 36)

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.ammo = 10  # Maximum ammo as integer
        self.max_ammo = 10  # For drawing the ammo bar
        self.ammo_reg = 10.0  # Floating point for precise regeneration tracking

    def draw(self):
        rotated_image = pygame.transform.rotate(ship_image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect.topleft)
        self.draw_ammo_bar()

    def update(self, mouse_x, mouse_y):
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.angle = -(180 / math.pi * math.atan2(rel_y, rel_x)) - 90

    def draw_ammo_bar(self):
        for i in range(int(self.ammo)):  # Convert float to int for range
            pygame.draw.rect(screen, YELLOW, (self.x - 25 + i * 5, self.y + 30, 4, 10))

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            self.ammo_reg -= 1.0
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - self.x, my - self.y
            distance = math.hypot(dx, dy)
            dx, dy = dx / distance, dy / distance
            bullets.append(Bullet(self.x, self.y, dx * 10, dy * 10))

    def regenerate_ammo(self):
        if self.ammo_reg < self.max_ammo:
            self.ammo_reg += 0.02  # Regenerate ammo gradually
            if self.ammo_reg > self.ammo:  # Only update integer ammo if fractional ammo exceeds it
                self.ammo = int(self.ammo_reg)

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(laser_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Asteroid:
    def __init__(self, x, y, size, dx, dy, level=1):
        self.x = x
        self.y = y
        self.size = size
        self.dx = dx
        self.dy = dy
        self.level = level
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self):
        asteroid_scaled = pygame.transform.scale(asteroid_image, (self.size, self.size))
        screen.blit(asteroid_scaled, self.rect.topleft)

def spawn_asteroid():
    time_factor = min(game_time / 10000, 1)
    weights = (0.6 + 0.4 * time_factor, 0.3, 0.1 + 0.2 * time_factor)
    size = random.choices(ASTEROID_SIZES, weights=weights)[0]
    edge = random.choice(['left', 'right', 'top', 'bottom'])
    if edge == 'left':
        x, y = -size, random.randint(0, SCREEN_HEIGHT)
    elif edge == 'right':
        x, y = SCREEN_WIDTH + size, random.randint(0, SCREEN_HEIGHT)
    elif edge == 'top':
        x, y = random.randint(0, SCREEN_WIDTH), -size
    else:
        x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + size
    dx, dy = ship.x - x, ship.y - y
    dist = math.hypot(dx, dy)
    speed_multiplier = 0.5 + 1.5 * time_factor
    dx, dy = (dx / dist) * random.uniform(speed_multiplier, speed_multiplier + 1), (dy / dist) * random.uniform(speed_multiplier, speed_multiplier + 1)

    if random.random() < 0.03:
        size = 150
        speed_factor = 300.0
        dx, dy = dx / dist * speed_factor, dy / dist * speed_factor
        asteroids.append(Asteroid(x, y, size, dx, dy, level=4))
    else:
        asteroids.append(Asteroid(x, y, size, dx, dy))

def handle_bullets():
    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
            bullets.remove(bullet)
        else:
            bullet.draw()

def handle_asteroids():
    global score
    for asteroid in asteroids[:]:
        asteroid.move()
        asteroid.draw()
        ship_rect = pygame.Rect(ship.x - 25, ship.y - 25, 50, 50)
        if ship_rect.colliderect(asteroid.rect):
            show_game_over_screen()
        for bullet in bullets[:]:
            if bullet.rect.colliderect(asteroid.rect):
                score += 10
                bullets.remove(bullet)
                if asteroid.level == 1:
                    if asteroid.size == 70:
                        for _ in range(2):
                            new_size = asteroid.size // 2
                            new_dx, new_dy = random.uniform(-2, 2), random.uniform(-2, 2)
                            asteroids.append(Asteroid(asteroid.x, asteroid.y, new_size, new_dx, new_dy))
                elif asteroid.level == 2:
                    for _ in range(2):
                        new_size = 50
                        new_dx, new_dy = random.uniform(-2, 2), random.uniform(-2, 2)
                        asteroids.append(Asteroid(asteroid.x, asteroid.y, new_size, new_dx, new_dy, level=1))
                elif asteroid.level == 3:
                    for _ in range(3):
                        new_size = 70
                        new_dx, new_dy = random.uniform(-1, 1), random.uniform(-1, 1)
                        asteroids.append(Asteroid(asteroid.x, asteroid.y, new_size, new_dx, new_dy, level=2))
                elif asteroid.level == 4:
                    for _ in range(5):
                        new_size = 70
                        new_dx, new_dy = random.uniform(-1, 1), random.uniform(-1, 1)
                        asteroids.append(Asteroid(asteroid.x, asteroid.y, new_size, new_dx, new_dy, level=3))
                asteroids.remove(asteroid)
                break

def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

def show_game_over_screen():
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    play_again_text = font.render("Click to play again", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 30))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_input = False
                reset_game()  # Reset the game state right after the decision to play again

def reset_game():
    global bullets, asteroids, score, game_time
    bullets = []
    asteroids = []
    score = 0
    game_time = 0
    ship.ammo = ship.max_ammo  # Reset ammo to full
    ship.ammo_reg = float(ship.max_ammo)  # Reset fractional ammo tracking

ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
bullets = []
asteroids = []
score = 0
game_time = 0

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()

    mx, my = pygame.mouse.get_pos()
    ship.update(mx, my)
    ship.draw()

    ship.regenerate_ammo()  # Regenerate ammo every frame

    handle_bullets()
    handle_asteroids()
    display_score()

    if random.random() < 0.01 * (1 + game_time / 60000):
        spawn_asteroid()

    pygame.display.flip()
    clock.tick(FPS)
    game_time += clock.get_time()

pygame.quit()