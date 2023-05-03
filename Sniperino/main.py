import pygame
import random

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 850))
pygame.display.set_caption("Sniperino")
clock = pygame.time.Clock()

shot_sound = pygame.mixer.Sound('shot_sound.mp3')
fire_shot_sound = pygame.mixer.Sound('fire_shot_sound.mp3')

# images
background = pygame.image.load('images/background.jpg')
sniper = pygame.image.load('images/sniper.png').convert_alpha()
zombie1 = pygame.image.load('images/zombie.png').convert_alpha()
zombie2 = pygame.image.load('images/zombie2.png').convert_alpha()
zombie_boss = pygame.image.load('images/zombie_boss.png').convert_alpha()
bullet = pygame.image.load('images/power_bullet.png').convert_alpha()
fire_bullet = pygame.image.load('images/flame_shot.png').convert_alpha()

# positions
sniper_position_y = 30
bullet_position_x = 195
bullet_position_y = sniper_position_y + 40

random_y_position_for_zombie = [30, 190, 350, 510, 670]

ADD_ZOMBIE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ZOMBIE_EVENT, 30000)


class Zombie:
    def __init__(self, name_image):
        self.name_image = name_image
        if self.name_image == zombie1:
            self.rect = self.name_image.get_rect(topleft=(1600, random.choice(random_y_position_for_zombie)))
            self.hit_points = 2
        elif self.name_image == zombie2:
            self.rect = self.name_image.get_rect(topleft=(1800, random.choice(random_y_position_for_zombie)))
            self.hit_points = 4
        else:
            self.rect = self.name_image.get_rect(topleft=(2000, random.choice(random_y_position_for_zombie[0:4])))
            self.hit_points = 12


class Bullet:
    def __init__(self, name_image):
        self.name_image = name_image
        if self.name_image == bullet:
            self.damage = 1
            self.rect = self.name_image.get_rect(center=(bullet_position_x, sniper_position_y + 45))
        elif self.name_image == fire_bullet:
            self.damage = 4
            self.rect = self.name_image.get_rect(center=(bullet_position_x, sniper_position_y + 45))


zombies = []

for i in range(3):
    zombie = Zombie(zombie1)
    zombies.append(zombie)
for x in range(2):
    zombie = Zombie(zombie2)
    zombies.append(zombie)
zombie = Zombie(zombie_boss)
zombies.append(zombie)

num_of_bullets = 0
bullets = []

while True:
    sniper_rect = sniper.get_rect(topleft=(30, sniper_position_y))
    velocity = 0.2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and sniper_position_y > 160:
                sniper_position_y -= 160
            if event.key == pygame.K_DOWN and sniper_position_y < 650:
                sniper_position_y += 160
            if event.key == pygame.K_SPACE:
                num_of_bullets += 1
                if num_of_bullets % 10 == 0:
                    new_bullet = Bullet(fire_bullet)
                    fire_shot_sound.play()
                    bullets.append(new_bullet)
                else:
                    shot_sound.play()
                    new_bullet = Bullet(bullet)
                    bullets.append(new_bullet)

        if event.type == ADD_ZOMBIE_EVENT:
            zombie = Zombie(zombie1)
            zombies.append(zombie)

    screen.blit(background, (0, 0))
    screen.blit(sniper, (30, sniper_position_y))

    for bullet_in_list in bullets:
        bullet_in_list.rect.x += 15
        screen.blit(bullet_in_list.name_image, bullet_in_list.rect)
        for zombie in zombies:
            if bullet_in_list.rect.colliderect(zombie.rect):
                zombie.hit_points -= bullet_in_list.damage
                bullets.remove(bullet_in_list)
                if zombie.hit_points <= 0:
                    velocity += 0.1
                    if zombie.name_image == zombie1:
                        zombie.rect.x = 1600
                        zombie.hit_points = 2
                    elif zombie.name_image == zombie2:
                        zombie.rect.x = 1800
                        zombie.hit_points = 4
                    else:
                        zombie.rect.x = 2200
                        zombie.hit_points = 20

    for zombie in zombies:
        velocity += 0.2
        zombie.rect.x -= velocity
        if zombie.hit_points > 0:
            screen.blit(zombie.name_image, zombie.rect)
        if zombie.rect.colliderect(sniper_rect):
            quit()

    pygame.display.update()
    clock.tick(60)
