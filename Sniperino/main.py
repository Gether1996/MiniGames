import pygame
import random

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 900))
pygame.display.set_caption("Sniperino")
clock = pygame.time.Clock()

# sounds
bullet_sound = pygame.mixer.Sound('shot_sound.mp3')
fire_shot_sound = pygame.mixer.Sound('fire_shot_sound.mp3')

# images
background = pygame.image.load('images/background.jpg')
sniper = pygame.image.load('images/sniper.png').convert_alpha()
zombie1 = pygame.image.load('images/zombie.png').convert_alpha()
zombie2 = pygame.image.load('images/zombie2.png').convert_alpha()
zombie_boss = pygame.image.load('images/zombie_boss.png').convert_alpha()
bullet = pygame.image.load('images/power_bullet.png').convert_alpha()
fire_bullet = pygame.image.load('images/flame_shot.png').convert_alpha()
sound_on = pygame.image.load('images/sound_on.png').convert_alpha()
sound_off = pygame.image.load('images/sound_off.png').convert_alpha()
legend = pygame.image.load('images/legend.png').convert_alpha()
legend2 = pygame.image.load('images/legend2.png').convert_alpha()

# positions and rectangles
sniper_position_y = 20
bullet_position_x = 160
UI_rect = pygame.Rect(0, 700, 1500, 200)
fire_bullet_to_catch_pos_x = 1600

# colors & fonts
BROWN = (205, 133, 63)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Comic Sans MS", 36)

random_y_spawning_positions = [20, 160, 300, 440, 580]

# new zombie1 added to game each 30 seconds
ADD_ZOMBIE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ZOMBIE_EVENT, 30000)

# fire bullet every 20 seconds
FIRE_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(FIRE_BULLET_EVENT, 20000)

# 5 seconds of fire ammunition
RESET_FIRE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(RESET_FIRE_EVENT, 5000)


class Zombie:
    def __init__(self, name_image):
        self.name_image = name_image
        if self.name_image == zombie1:
            self.rect = self.name_image.get_rect(topleft=(1500, random.choice(random_y_spawning_positions)))
            self.hit_points = 2
        elif self.name_image == zombie2:
            self.rect = self.name_image.get_rect(topleft=(1500, random.choice(random_y_spawning_positions)))
            self.hit_points = 4
        else:
            self.rect = self.name_image.get_rect(topleft=(1500, random.choice(random_y_spawning_positions[0:4])))
            self.rect = self.rect.inflate(-30, -30)
            self.hit_points = 12


class Bullet:
    def __init__(self, name_image):
        self.name_image = name_image
        self.visible = True
        if self.name_image == bullet:
            self.damage = 1
            self.rect = self.name_image.get_rect(center=(bullet_position_x, sniper_position_y + 40))
        elif self.name_image == fire_bullet:
            self.damage = 4
            self.rect = self.name_image.get_rect(center=(bullet_position_x, sniper_position_y + 40))


zombies = []
# creating starting zombies
for i in range(3):
    zombie = Zombie(zombie1)
    zombie.rect.x += 100 * i
    zombies.append(zombie)
for x in range(2):
    zombie = Zombie(zombie2)
    zombie.rect.x += 150 * x
    zombies.append(zombie)
zombie_boss1 = Zombie(zombie_boss)
zombies.append(zombie_boss1)

bullets = []
sound_turned_on = True
fire_ammunition = False
fire_bullet_to_catch = Bullet(fire_bullet)
fire_bullet_to_catch.visible = False
score = 0
stage_of_game = 1

while True:
    while stage_of_game == 1:
        sniper_rect = sniper.get_rect(topleft=(30, sniper_position_y))
        sound_rect = sound_on.get_rect(topleft=(60, 780))
        score_surface = FONT.render(f"Score: {score}", True, BLACK)
        velocity = 0.2
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BROWN, UI_rect)
        screen.blit(legend, (1250, 705))
        screen.blit(legend2, (900, 735))
        screen.blit(score_surface, (30, 700))
        screen.blit(sniper, (30, sniper_position_y))

        #######################################################                EVENTS          ####################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and sniper_position_y > 140:
                    sniper_position_y -= 140
                if event.key == pygame.K_DOWN and sniper_position_y < 550:
                    sniper_position_y += 140
                if event.key == pygame.K_SPACE:
                    if fire_ammunition:
                        fire_shot_sound.play()
                        new_bullet = Bullet(fire_bullet)
                        bullets.append(new_bullet)
                    else:
                        new_bullet = Bullet(bullet)
                        bullet_sound.play()
                        bullets.append(new_bullet)

            if event.type == ADD_ZOMBIE_EVENT:
                zombie = Zombie(zombie1)
                zombies.append(zombie)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if sound_rect.collidepoint(event.pos) and sound_turned_on:
                    sound_turned_on = False
                else:
                    sound_turned_on = True

            if event.type == FIRE_BULLET_EVENT:
                fire_bullet_to_catch.rect.x = 1600
                fire_bullet_to_catch.rect.y = random.choice(random_y_spawning_positions) + 20
                fire_bullet_to_catch.visible = True

            if event.type == RESET_FIRE_EVENT:
                fire_ammunition = False
                pygame.time.set_timer(RESET_FIRE_EVENT, 0)

        #######################################################         BULLETS / ZOMBIES          ####################
        for bullet_in_list in bullets:
            bullet_in_list.rect.x += 15
            if bullet_in_list.visible:
                screen.blit(bullet_in_list.name_image, bullet_in_list.rect)
            for zombie in zombies:
                if bullet_in_list.rect.colliderect(zombie.rect) and bullet_in_list.visible:
                    zombie.hit_points -= bullet_in_list.damage
                    bullet_in_list.visible = False
                    if zombie.hit_points <= 0:
                        velocity += 0.2
                        if zombie.name_image == zombie1:
                            score += 10
                            zombie.rect.x = 1550
                            zombie.rect.y = random.choice(random_y_spawning_positions)
                            zombie.hit_points = 2
                        elif zombie.name_image == zombie2:
                            score += 20
                            zombie.rect.x = 1520
                            zombie.rect.y = random.choice(random_y_spawning_positions)
                            zombie.hit_points = 4
                        else:
                            score += 60
                            zombie.rect.x = 1580
                            zombie.rect.y = random.choice(random_y_spawning_positions[0:4])
                            zombie.hit_points = 12

        for zombie in zombies:
            velocity += 0.2
            zombie.rect.x -= velocity
            if zombie.hit_points > 0:
                screen.blit(zombie.name_image, zombie.rect)
            if zombie.rect.colliderect(sniper_rect):
                quit()

        if fire_bullet_to_catch.visible:
            screen.blit(fire_bullet, fire_bullet_to_catch.rect)
            fire_bullet_to_catch.rect.x -= 10
            if fire_bullet_to_catch.rect.colliderect(sniper_rect):
                fire_bullet_to_catch.visible = False
                fire_ammunition = True
                pygame.time.set_timer(RESET_FIRE_EVENT, 5000)

        #######################################################         GAME BAR         ####################
        if sound_turned_on:
            screen.blit(sound_on, sound_rect)
            bullet_sound.set_volume(0.4)
            fire_shot_sound.set_volume(0.6)
        else:
            screen.blit(sound_off, sound_rect)
            bullet_sound.set_volume(0)
            fire_shot_sound.set_volume(0)

        pygame.display.update()
        clock.tick(60)
