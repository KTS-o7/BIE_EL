import pygame
import random

# initialize Pygame
pygame.init()

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bio-inspired Antivirus System")

# define variables
CELL_SIZE = 20
CELL_SPEED = 5
VIRUS_SIZE = 10
VIRUS_SPAWN_RATE = 50
virus_list = []

# create a cell class
class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - CELL_SIZE)
        self.rect.y = random.randrange(WINDOW_HEIGHT - CELL_SIZE)

    def update(self):
        # move the cell randomly
        self.rect.x += random.randrange(-CELL_SPEED, CELL_SPEED)
        self.rect.y += random.randrange(-CELL_SPEED, CELL_SPEED)

        # keep the cell on the screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WINDOW_WIDTH - CELL_SIZE:
            self.rect.x = WINDOW_WIDTH - CELL_SIZE
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > WINDOW_HEIGHT - CELL_SIZE:
            self.rect.y = WINDOW_HEIGHT - CELL_SIZE

    def attack_virus(self):
        # find the nearest virus
        nearest_virus = None
        min_distance = float("inf")
        for virus in virus_list:
            distance = ((self.rect.x - virus.rect.x) ** 2 + (self.rect.y - virus.rect.y) ** 2) ** 0.5
            if distance < min_distance:
                nearest_virus = virus
                min_distance = distance

        # move towards the nearest virus
        if nearest_virus:
            if self.rect.x < nearest_virus.rect.x:
                self.rect.x += CELL_SPEED
            elif self.rect.x > nearest_virus.rect.x:
                self.rect.x -= CELL_SPEED
            if self.rect.y < nearest_virus.rect.y:
                self.rect.y += CELL_SPEED
            elif self.rect.y > nearest_virus.rect.y:
                self.rect.y -= CELL_SPEED

            # consume the virus if close enough
            if ((self.rect.x - nearest_virus.rect.x) ** 2 + (self.rect.y - nearest_virus.rect.y) ** 2) ** 0.5 < CELL_SIZE:
                virus_list.remove(nearest_virus)
                nearest_virus.kill()

# create a virus class
class Virus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((VIRUS_SIZE, VIRUS_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - VIRUS_SIZE)
        self.rect.y = random.randrange(WINDOW_HEIGHT - VIRUS_SIZE)
        self.direction = random
                # set a random direction
        self.change_direction()

    def change_direction(self):
        self.direction = random.choice(["up", "down", "left", "right"])

    def update(self):
        # move the virus in its current direction
        if self.direction == "up":
            self.rect.y -= CELL_SPEED
        elif self.direction == "down":
            self.rect.y += CELL_SPEED
        elif self.direction == "left":
            self.rect.x -= CELL_SPEED
        elif self.direction == "right":
            self.rect.x += CELL_SPEED

        # change direction randomly
        if random.randrange(50) == 0:
            self.change_direction()

# create sprite groups
all_sprites = pygame.sprite.Group()
cells = pygame.sprite.Group()
viruses = pygame.sprite.Group()

# create cells
for i in range(10):
    cell = Cell()
    all_sprites.add(cell)
    cells.add(cell)

# set up the game loop
clock = pygame.time.Clock()
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # spawn viruses randomly
    if random.randrange(VIRUS_SPAWN_RATE) == 0:
        virus = Virus()
        all_sprites.add(virus)
        viruses.add(virus)
        virus_list.append(virus)

    # update cells and viruses
    for cell in cells:
        cell.attack_virus()
        cell.update()
    for virus in viruses:
        virus.update()

    # draw the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # draw the virus sequence
    for i in range(len(virus_list)):
        pygame.draw.circle(screen, RED, (20 + i * 15, 20), VIRUS_SIZE // 2)

    # draw the antivirus sequence
    for cell in cells:
        if len(virus_list) > 0:
            nearest_virus = None
            min_distance = float("inf")
            for virus in virus_list:
                distance = ((cell.rect.x - virus.rect.x) ** 2 + (cell.rect.y - virus.rect.y) ** 2) ** 0.5
                if distance < min_distance:
                    nearest_virus = virus
                    min_distance = distance
            if nearest_virus:
                pygame.draw.line(screen, GREEN, (cell.rect.x + CELL_SIZE // 2, cell.rect.y + CELL_SIZE // 2), (nearest_virus.rect.x + VIRUS_SIZE // 2, nearest_virus.rect.y + VIRUS_SIZE // 2))

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)

# quit Pygame
pygame.quit()
