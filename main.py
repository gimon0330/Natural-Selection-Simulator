import pygame
import random
import time

pygame.init()

SCREEN_WIDTH =  1080
SCREEN_HEIGHT =  720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BSIS 10기 Natural Selection Simulator")
clock = pygame.time.Clock()

screen.fill((255,255,255))


class Predetor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(800, 600)
        self.speed = pygame.Vector2(3, 3)
        self.eaten = 0

    def update(self):
        self.speed.rotate_ip(random.gauss(0, 1) * 10)
        self.pos += self.speed
        self.rect.center = self.pos

        if self.rect.left < 0:
            self.speed.x *= -1
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.speed.x *= -1
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.speed.y *= -1
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.speed.y *= -1
            self.rect.bottom = SCREEN_HEIGHT
    
    def eat(self):
        self.eaten += 1


class Prey(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size_x = random.uniform(5.0, 45.0)
        self.size_y = random.uniform(5.0, 45.0)
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill((0,0,0))

        self.posx = 100 + random.uniform(50.0,-50.0)
        self.posy = 100 + random.uniform(50.0,-50.0)
        self.pos = pygame.Vector2((self.posx, self.posy))
        
        self.rect = self.image.get_rect()
        self.speedsc = random.uniform(0.2, 6.0)
        self.speed = pygame.Vector2(self.speedsc, self.speedsc)

    def draw(self):
        self.image = pygame.Surface((self.size_x, self.size_y))
        
        pygame.draw.rect(screen, (0, 0, 0), (self.posx, self.posy, self.size_x, self.size_y))

        self.rect = self.image.get_rect()
        

    def update(self):
        self.speed.rotate_ip(random.gauss(0, 1) * 10)
        self.pos += self.speed
        self.rect.center = self.pos

        if self.rect.left < 0:
            self.speed.x *= -1
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.speed.x *= -1
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.speed.y *= -1
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.speed.y *= -1
            self.rect.bottom = SCREEN_HEIGHT


all_sprites = pygame.sprite.Group()
predetor_sprites = pygame.sprite.Group()
prey_sprites = pygame.sprite.Group()

for i in range(6):
    predetor = Predetor()
    predetor_sprites.add(predetor)
    all_sprites.add(predetor)

for i in range(30):
    prey = Prey()
    prey_sprites.add(prey)
    all_sprites.add(prey)

day = 1
day_speed = 5

while True:
    print(f"day {day} ======")

    ############ 하루동안 (낮)
    count = time.time() + day_speed

    while time.time() < count:
        all_sprites.update()

        crash = pygame.sprite.groupcollide(prey_sprites, predetor_sprites, True, False)

        for prey, pred in crash.items():
            pred[0].eat()
            prey.kill()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((255,255,255))

        all_sprites.draw(screen)

        clock.tick(60)
        pygame.display.update()

    ############### 하루가 지나고 (밤)

    day+=1

    for preys in prey_sprites:
        new_prey = Prey()
        new_prey.size_x = preys.size_x + random.uniform(-0.5,0.5)
        new_prey.size_y = preys.size_y + random.uniform(-0.5,0.5)
        new_prey.speedsc = preys.speedsc + random.uniform(-0.5,0.5)
        
        new_prey.posx = preys.pos.x
        new_prey.posy = preys.pos.y

        new_prey.draw()
        prey_sprites.add(new_prey)
        all_sprites.add(new_prey)
