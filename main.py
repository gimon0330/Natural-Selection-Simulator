import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1080,720))
pygame.display.set_caption("이미지 불러오기")
clock = pygame.time.Clock()

screen.fill((255,255,255))

player_posX =  100
player_posY =  100

class Predetor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.x_speed = 20
        self.y_speed = 20

    def update(self):
        self.rect.x += self.x_speed

class Prey(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()

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

while True:
    all_sprites.update()

    crash = pygame.sprite.groupcollide(prey_sprites, predetor_sprites, True, True)

    if crash:
        print("Crash")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    all_sprites.draw(screen)

    clock.tick(60)
    pygame.display.update()
