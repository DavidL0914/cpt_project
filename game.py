import pygame
import random
import math
import sys

pygame.init()

GALAXY_WIDTH, GALAXY_HEIGHT = 800, 600
CLOCK_SPEED = 60
SPACE_ROCK_SIZES = [30, 50, 70]

COLOR_BLIND_WHITE = (255, 255, 255)
VOID_BLACK = (0, 0, 0)

space = pygame.display.set_mode((GALAXY_WIDTH, GALAXY_HEIGHT))
pygame.display.set_caption("Cosmic Collision")

cosmic_cruiser = pygame.transform.scale(pygame.image.load('spaceship.png'), (50, 50))
meteor_chunk = pygame.image.load('asteroid.png')

universal_script = pygame.font.Font(None, 36)

class SpaceFalcon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spin = 0

    def draw(self):
        flipped_cruiser = pygame.transform.rotate(cosmic_cruiser, self.spin)
        fresh_rect = flipped_cruiser.get_rect(center=(self.x, self.y))
        space.blit(flipped_cruiser, fresh_rect.topleft)

    def update(self, mouse_x, mouse_y):
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.spin = -(180 / math.pi * math.atan2(rel_y, rel_x)) - 90

class LaserBeamOfDeath:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = 5
        self.rect = pygame.Rect(self.x - self.size, self.y - self.size, 2 * self.size, 2 * self.size)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self):
        pygame.draw.circle(space, COLOR_BLIND_WHITE, (int(self.x), int(self.y)), self.size)

class SpaceRock:
    def __init__(self, x, y, size, dx, dy):
        self.x = x
        self.y = y
        self.mass = size
        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(self.x, self.y, self.mass, self.mass)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self):
        scaled_rock = pygame.transform.scale(meteor_chunk, (self.mass, self.mass))
        space.blit(scaled_rock, self.rect.topleft)

cosmic_falcon = SpaceFalcon(GALAXY_WIDTH // 2, GALAXY_HEIGHT // 2)
death_rays = []
space_rocks = []
galactic_credits = 0
cosmic_timer = 0

def create_space_rock():
    cosmic_factor = min(cosmic_timer / 10000, 1)
    density = (0.6 + 0.4 * cosmic_factor, 0.3, 0.1 + 0.2 * cosmic_factor)
    mass = random.choices(SPACE_ROCK_SIZES, weights=density)[0]
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        x, y = -mass, random.randint(0, GALAXY_HEIGHT)
    elif side == 'right':
        x, y = GALAXY_WIDTH + mass, random.randint(0, GALAXY_HEIGHT)
    elif side == 'top':
        x, y = random.randint(0, GALAXY_WIDTH), -mass
    else:
        x, y = random.randint(0, GALAXY_WIDTH), GALAXY_HEIGHT + mass
    dx, dy = cosmic_falcon.x - x, cosmic_falcon.y - y
    distance = math.hypot(dx, dy)
    speed_boost = 0.5 + 1.5 * cosmic_factor
    dx, dy = (dx / distance) * random.uniform(speed_boost, speed_boost + 1), (dy / distance) * random.uniform(speed_boost, speed_boost + 1)
    space_rocks.append(SpaceRock(x, y, mass, dx, dy))

def manage_death_rays():
    for death_ray in death_rays[:]:
        death_ray.move()
        if death_ray.x < 0 or death_ray.x > GALAXY_WIDTH or death_ray.y < 0 or death_ray.y > GALAXY_HEIGHT:
            death_rays.remove(death_ray)
        else:
            death_ray.draw()

def manage_space_rocks():
    global galactic_credits
    for rock in space_rocks[:]:
        rock.move()
        rock.draw()
        falcon_rect = pygame.Rect(cosmic_falcon.x - 25, cosmic_falcon.y - 25, 50, 50)
        if falcon_rect.colliderect(rock.rect):
            print(f"Game Over! Your score was: {galactic_credits}")
            pygame.quit()
            sys.exit()
        for death_ray in death_rays[:]:
            if death_ray.rect.colliderect(rock.rect):
                galactic_credits += 10
                death_rays.remove(death_ray)
                if rock.mass == 70:
                    for _ in range(2):
                        new_mass = rock.mass // 2
                        new_dx, new_dy = random.uniform(-2, 2), random.uniform(-2, 2)
                        new_rock = SpaceRock(rock.x, rock.y, new_mass, new_dx, new_dy)
                        new_rock.rect.center = (rock.x, rock.y)
                        space_rocks.append(new_rock)
                space_rocks.remove(rock)
                break

def show_credits():
    credits_text = universal_script.render(f"Score: {galactic_credits}", True, COLOR_BLIND_WHITE)
    space.blit(credits_text, (GALAXY_WIDTH - 150, 10))

cosmic_clock = pygame.time.Clock()
still_flying = True
while still_flying:
    space.fill(VOID_BLACK)
    for cosmic_event in pygame.event.get():
        if cosmic_event.type == pygame.QUIT:
            still_flying = False
        if cosmic_event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - cosmic_falcon.x, my - cosmic_falcon.y
            range_to_target = math.hypot(dx, dy)
            dx, dy = dx / range_to_target, dy / range_to_target
            death_rays.append(LaserBeamOfDeath(cosmic_falcon.x, cosmic_falcon.y, dx * 10, dy * 10))

    mx, my = pygame.mouse.get_pos()
    cosmic_falcon.update(mx, my)
    cosmic_falcon.draw()

    manage_death_rays()
    manage_space_rocks()
    show_credits()

    if random.random() < 0.01 * (1 + cosmic_timer / 60000):
        create_space_rock()

    pygame.display.flip()
    cosmic_clock.tick(CLOCK_SPEED)
    cosmic_timer += cosmic_clock.get_time()

pygame.quit()
