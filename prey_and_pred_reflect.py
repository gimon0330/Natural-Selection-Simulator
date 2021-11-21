import pygame, random, time, sys

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
        self.image = pygame.Surface((35, 35))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(800, 600)
        self.speed = pygame.Vector2(8, 8)
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
        self.size_x = random.uniform(0.00, 50.00)
        self.size_y = random.uniform(0.00, 50.00)
        self.image = pygame.Surface((self.size_x, self.size_y))
        self.image.fill((0,0,0))

        self.posx = 100 + random.uniform(50.0,-50.0)
        self.posy = 100 + random.uniform(50.0,-50.0)
        self.pos = pygame.Vector2((self.posx, self.posy))
        
        self.rect = self.image.get_rect()
        self.speed = pygame.Vector2(7, 7)
        self.speed.rotate_ip(random.uniform(0,360))

    def draw(self):
        if self.size_x <= 0: self.size_x = 0.1
        if self.size_y <= 0: self.size_y = 0.1
        self.image = pygame.Surface((self.size_x, self.size_y))
        
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.left, self.rect.right, self.size_x, self.size_y))

        self.rect = self.image.get_rect()
        

    def update(self):
        self.speed.rotate_ip(random.gauss(0,1)*5)
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

for i in range(4):
    predetor = Predetor()
    predetor_sprites.add(predetor)
    all_sprites.add(predetor)

for i in range(400):
    prey = Prey()
    prey_sprites.add(prey)
    all_sprites.add(prey)

day = 1
day_speed = 3

while True:
    print(f"day {day} ======")

    ############ 하루동안 (낮)
    count = time.time() + day_speed

    while time.time() < count:
        all_sprites.update()

        crash = pygame.sprite.groupcollide(prey_sprites, predetor_sprites, True, False)

        for prey, pred in crash.items():
            if 100 < len(prey_sprites):
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
    average_size = 0
    for preys in prey_sprites:
        average_size += preys.size_x * preys.size_y
    print(f"Amount : {len(prey_sprites)}, Average : {average_size/len(prey_sprites)}")

    for preys in prey_sprites:
        if len(prey_sprites) > 1000:
            break
        
        new_prey = Prey()

        if random.randint(0, 100) < 1: #돌연변이 발생
            new_prey.size_x = preys.size_x + random.uniform(-5.0,5.0)
            new_prey.size_y = preys.size_y + random.uniform(-5.0,5.0)
        
        else: 
            new_prey.size_x = preys.size_x + random.uniform(-1.0,1.0)
            new_prey.size_y = preys.size_y + random.uniform(-1.0,1.0)
        
        new_prey.pos = preys.rect.center

        prey_sprites.add(new_prey)
        all_sprites.add(new_prey)

    """for predetors in predetor_sprites:
        if predetors.eaten < 3:
            predetors.kill()
        if predetors.eaten > 60:
            new_predetor = Predetor()
            new_predetor.pos = predetors.rect.center
            
            predetor_sprites.add(new_predetor)
            all_sprites.add(new_predetor)

        predetors.eaten = 0"""

    if not predetor_sprites:
        print("All predetors dead")
        pygame.quit()
        sys.exit()

    if not prey_sprites:
        print("All preys dead")
        pygame.quit()
        sys.exit()