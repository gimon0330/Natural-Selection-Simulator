import pygame
import random
import time

pygame.init()

SCREEN_WIDTH =  1080
SCREEN_HEIGHT =  720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("이미지 불러오기")
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
        self.image = pygame.Surface((30, 30))
        self.image.fill((0,0,0))
        self.pos = pygame.Vector2(100, 100)
        self.rect = self.image.get_rect()
        self.speed = pygame.Vector2(2, 2)

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

for i in range(20):
    prey = Prey()
    prey_sprites.add(prey)
    all_sprites.add(prey)

day = 1

while True:
    print(f"day {day} ======")

    ############ 하루동안 (낮)

    while time.time() < 60:
        all_sprites.update()

        crash = pygame.sprite.groupcollide(prey_sprites, predetor_sprites, True, False)

        for pred, prey in crash.items():
                pred.eat()
                prey[0].kill()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((255,255,255))

        all_sprites.draw(screen)

        clock.tick(60)
        pygame.display.update()

    ############### 하루가 지나고 (밤)

    reproduced = 0

    for pred in predetor_sprites:
        if pred.eaten >= 2:
            reproduced += 1
