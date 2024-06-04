import pygame
from random import randint

# inicializace pygame
pygame.init()

# barvy
LIGHTBLUE = (0, 255, 255)
RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 190, 0)
# zakladni nastaveni
fps = 40
clock = pygame.time.Clock()
n = 9
start_x = 5
start_y = 5
monsters = []
num_monsters = 24
score = 0
bg_color = BLACK
text_color = YELLOW

# obrazovka
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
screen.fill(LIGHTBLUE)

# fonts
font = pygame.font.SysFont('arial', 60)
min_font = pygame.font.SysFont('arial', 30)
# text
# lose
You_lose_text = font.render('YOU LOSE', True, RED)
You_lose_text_rect = You_lose_text.get_rect()
You_lose_text_rect.x = width // 2 - 60
You_lose_text_rect.y = height // 2

# win
You_win_text = font.render('YOU WIN', True, GREEN)
You_win_text_rect = You_win_text.get_rect()
You_win_text_rect.x = width // 2 - 60
You_win_text_rect.y = height // 2

# continue text
Continue_text = min_font.render('Do you want to play again? Press any key', True, text_color)
Continue_text_rect = Continue_text.get_rect()
Continue_text_rect.x = width // 2 - 150
Continue_text_rect.y = height // 2 + 60


# class Area
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = bg_color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(screen, self.fill_color, self.rect)

    def outline(self, frame_color, thickneess):
        pygame.draw.rect(screen, frame_color, self.rect, thickneess)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)


# class Picture
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Objekty
# Bg
# Bg = Picture('bg.png3.jpg',0,0,width,height)
# ball
ball = Picture('img/chocolate-ball-icon.png', 160, 200, 50, 50)
ball.direction_y = 'up'
ball.direction_x = 'left'

# platform
platform = Picture('img/platform.png', 250, height - 100, 50, 50)
for j in range(3):
    x = start_x + (27 * j)
    y = start_y + (55 * j)
    for i in range(n):
        monster = Picture('img/Alien-icon.png', x, y, 50, 50)
        monsters.append(monster)
        x += 55

    n -= 1
# Hlavni cykl
lets_continue = True
while lets_continue:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and platform.rect.x > 0:
        platform.rect.x -= 5
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and platform.rect.x + platform.rect.width + 50 < width:
        platform.rect.x += 5
    # ball moving

    if ball.rect.y <= 0:
        ball.direction_y = 'down'
        random01 = randint(0, 1)
        if random01 == 0:
            ball.direction_x = 'left'
        if random01 == 1:
            ball.direction_x = 'right'
    if ball.rect.x <= 0:
        ball.direction_x = 'right'
    if ball.rect.x + 50 >= width:
        ball.direction_x = 'left'
    if ball.rect.colliderect(platform.rect):
        ball.direction_y = 'up'
        random01 = randint(0, 1)
        if random01 == 0:
            ball.direction_x = 'left'
        if random01 == 1:
            ball.direction_x = 'right'

    if ball.direction_y == 'up':
        ball.rect.y -= 3
    if ball.direction_y == 'down':
        ball.rect.y += 3
    if ball.direction_x == 'left':
        ball.rect.x -= 3
    if ball.direction_x == 'right':
        ball.rect.x += 3

    screen.fill(bg_color)

    for monster in monsters:
        monster.fill()
        monster.draw()
        if len(monsters) <= 24:
            for monster in monsters:
                if monster.rect.colliderect(ball.rect):
                    monsters.remove(monster)
                    num_monsters -= 1
                    score += 1
                    ball.direction_y = 'down'
                    random01 = randint(0, 1)
                    if random01 == 0:
                        ball.direction_x = 'left'
                    if random01 == 1:
                        ball.direction_x = 'right'
    if len(monsters) <= 0:

        pause = True
        while pause:
            screen.blit(You_win_text, You_win_text_rect)
            screen.blit(Continue_text, Continue_text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False
                if event.type == pygame.KEYDOWN:
                    n = 9
                    for monster in monsters:
                        monsters.remove(monster)
                    monsters = []
                    score = 0
                    for j in range(3):
                        x = start_x + (27 * j)
                        y = start_y + (55 * j) + 50
                        for i in range(n):
                            monster = Picture('img/Alien-icon.png', x, y, 50, 50)
                            monsters.append(monster)
                            x += 55

                        n -= 1
                    ball.direction_y = 'up'
                    ball.direction_x = 'left'
                    ball.rect.x = 160
                    ball.rect.y = 200
                    pause = False

            pygame.display.update()
            clock.tick(fps)
    if ball.rect.y > 500:

        pause1 = True
        while pause1:
            screen.blit(You_lose_text, You_lose_text_rect)
            screen.blit(Continue_text, Continue_text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False
                if event.type == pygame.KEYDOWN:
                    n = 9
                    for monster in monsters:
                        monsters.remove(monster)
                    monsters = []
                    score = 0
                    for j in range(3):
                        x = start_x + (27 * j)
                        y = start_y + (55 * j)
                        for i in range(n):
                            monster = Picture('img/Alien-icon.png', x, y, 50, 50)
                            monsters.append(monster)
                            x += 55

                        n -= 1
                    ball.direction_y = 'up'
                    ball.direction_x = 'left'
                    ball.rect.x = 160
                    ball.rect.y = 200

                    pause1 = False

            pygame.display.update()
            clock.tick(fps)

    ball.fill()
    ball.draw()

    platform.fill()
    platform.draw()

    pygame.display.update()
    clock.tick(fps)
