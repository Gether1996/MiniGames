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
final_boss = pygame.image.load('images/final_boss.png').convert_alpha()
bullet = pygame.image.load('images/power_bullet.png').convert_alpha()
fire_bullet = pygame.image.load('images/flame_shot.png').convert_alpha()
shark_bullet = pygame.image.load('images/shark_bullet.png').convert_alpha()
sound_on = pygame.image.load('images/sound_on.png').convert_alpha()
sound_off = pygame.image.load('images/sound_off.png').convert_alpha()
legend = pygame.image.load('images/legend.png').convert_alpha()
legend2 = pygame.image.load('images/legend2.png').convert_alpha()
clickable_square = pygame.image.load('images/clickable_square.png').convert_alpha()
info_1 = pygame.image.load('images/info_1.png').convert_alpha()
info_2 = pygame.image.load('images/info_2.png').convert_alpha()


# positions and rectangles
sniper_position_y = 20
bullet_position_x = 160
UI_rect = pygame.Rect(0, 700, 1500, 200)
fire_bullet_to_catch_pos_x = 1600

# colors & fonts
BROWN = (205, 133, 63)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Comic Sans MS", 36)
FONT_BIGGER = pygame.font.SysFont("Comic Sans MS", 60)

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

# shark_bullet_skill usable each 30sec
SHARK_SKILL_READY = pygame.USEREVENT + 4
pygame.time.set_timer(SHARK_SKILL_READY, 30000)


class Zombie:
    def __init__(self, name_image):
        self.name_image = name_image
        if self.name_image == zombie1:
            self.rect = self.name_image.get_rect(topleft=(1500, random.choice(random_y_spawning_positions)))
            self.hit_points = 2
        elif self.name_image == zombie2:
            self.rect = self.name_image.get_rect(topleft=(1500, random.choice(random_y_spawning_positions)))
            self.hit_points = 4
        elif self.name_image == zombie_boss:
            self.rect = self.name_image.get_rect(topleft=(1500, random.choice(random_y_spawning_positions[0:4])))
            self.rect = self.rect.inflate(-30, -30)
            self.hit_points = 12
        else:
            self.rect = self.name_image.get_rect(topleft=(1500, 100))
            self.hit_points = 36


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
        elif self.name_image == shark_bullet:
            self.damage = 8
            self.rect = self.name_image.get_rect(center=(bullet_position_x, sniper_position_y + 40))


# creating starting zombies
zombies_stage1 = []      # 5x zombie1, 1x zombie2
zombies_stage2 = []      # 5x zombie1, 4x zombie2, 1x zombie_boss
zombies_stage3 = []      # 5x zombie1, 4x zombie2, 3x zombie_boss
# zombies 1
for i in range(6):
    zombie = Zombie(zombie1)
    zombies_stage1.append(zombie)
    zombies_stage2.append(zombie)
    zombies_stage3.append(zombie)

# zombies 2
for x in range(4):
    zombie = Zombie(zombie2)
    zombies_stage2.append(zombie)
    zombies_stage3.append(zombie)
zombie2_for_stage1 = Zombie(zombie2)
zombies_stage1.append(zombie2_for_stage1)

# zombie bosses
for j in range(3):
    zombie = Zombie(zombie_boss)
    zombies_stage3.append(zombie)
zombie_boss_stage2 = Zombie(zombie_boss)
zombies_stage2.append(zombie_boss_stage2)

# starting stats
bullets = []
boxes = []
sound_turned_on = True
fire_ammunition = False
fire_bullet_to_catch = Bullet(fire_bullet)
fire_bullet_to_catch.visible = False
score = 0
stage_of_game = "starting menu"
starting_menu = True
reset_zombies = True
summon_final_boss = True
show_info_of_game = False
shark_bullet_skill_ready = False


def get_zombie_list_based_on_stage():
    if stage_of_game == 1:
        return zombies_stage1
    elif stage_of_game == 2:
        return zombies_stage2
    else:
        return zombies_stage3


def reset_zombies_x_position(x_position):
    velocity = 0.2
    for i, zombie in enumerate(get_zombie_list_based_on_stage()):
        zombie.rect.x = x_position + i * 50
    return velocity


def fill_zombies_stage3(zombie_list):
    for o in range(6):
        zombie_to_append = Zombie(zombie1)
        zombie_list.append(zombie_to_append)
    for u in range(4):
        zombie2_to_append = Zombie(zombie2)
        zombie_list.append(zombie2_to_append)
    for boss in range(3):
        boss_to_append = Zombie(zombie_boss)
        zombie_list.append(boss_to_append)


while True:
    while stage_of_game == "starting menu":
        score_surface = FONT.render(f"Score: {score}", True, BLACK)
        sniperino_surface = FONT_BIGGER.render("SNIPERINO", True, BLACK)
        created_by = FONT.render("Created by Patrik Kredátus", True, BLACK)

        screen.blit(background, (0, 0))
        screen.blit(sniperino_surface, (600, 50))
        screen.blit(score_surface, (700, 130))
        screen.blit(created_by, (550, 850))
        if show_info_of_game:
            screen.blit(info_1, (40, 250))
            screen.blit(info_2, (1000, 300))

        if starting_menu:
            for i in range(4):
                again_button = clickable_square.get_rect(topleft=(665, 250 + i * 120))
                screen.blit(clickable_square, again_button)
                boxes.append(again_button)
            text1 = FONT.render("START", True, BLACK)
            text2 = FONT.render("STAGES", True, BLACK)
            text3 = FONT.render("INFO", True, BLACK)
            text4 = FONT.render("QUIT", True, BLACK)
            screen.blit(text1, (700, 270))
            screen.blit(text2, (690, 390))
            screen.blit(text3, (710, 510))
            screen.blit(text4, (715, 630))
        else:
            for i in range(3):
                again_button = clickable_square.get_rect(topleft=(665, 250 + i * 120))
                screen.blit(clickable_square, again_button)
                boxes.append(again_button)
            text1 = FONT.render("1", True, BLACK)
            text2 = FONT.render("2", True, BLACK)
            text3 = FONT.render("3", True, BLACK)
            screen.blit(text1, (756, 270))
            screen.blit(text2, (750, 390))
            screen.blit(text3, (750, 510))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and starting_menu:
                    quit()
                else:
                    starting_menu = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if starting_menu:
                    if boxes[0].collidepoint(event.pos):
                        stage_of_game = 1
                        reset_zombies = True
                        show_info_of_game = False
                    elif boxes[1].collidepoint(event.pos):
                        starting_menu = False
                    elif boxes[2].collidepoint(event.pos):
                        show_info_of_game = True
                    elif boxes[3].collidepoint(event.pos):
                        quit()
                else:
                    if boxes[0].collidepoint(event.pos):
                        stage_of_game = 1
                        reset_zombies = True
                        show_info_of_game = False
                    elif boxes[1].collidepoint(event.pos):
                        stage_of_game = 2
                        reset_zombies = True
                        show_info_of_game = False
                    elif boxes[2].collidepoint(event.pos):
                        stage_of_game = 3
                        reset_zombies = True
                        show_info_of_game = False

    while stage_of_game in [1, 2, 3]:
        if reset_zombies:
            reset_zombies = False
            reset_zombies_x_position(1500)
        sniper_rect = sniper.get_rect(topleft=(30, sniper_position_y))
        sound_rect = sound_on.get_rect(topleft=(150, 780))
        again_button = clickable_square.get_rect(topleft=(500, 330))
        quit_button = clickable_square.get_rect(topleft=(800, 330))
        back_to_menu_surface = clickable_square.get_rect(topleft=(400, 780))
        shark_bullet_skill_surface = shark_bullet.get_rect(topleft=(400, 710))
        back_to_menu_text = FONT.render(f"MENU", True, BLACK)
        score_surface = FONT.render(f"Score: {score}", True, BLACK)
        current_stage_surface = FONT.render(f"Stage: {stage_of_game}", True, BLACK)
        again_text = FONT.render("AGAIN", True, BLACK)
        quit_text = FONT.render("QUIT", True, BLACK)
        congratz = FONT_BIGGER.render("CONGRATULATIONS!", True, BLACK)
        velocity = 0.2
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BROWN, UI_rect)
        screen.blit(clickable_square, back_to_menu_surface)
        screen.blit(back_to_menu_text, (448, 800))
        screen.blit(legend, (1000, 735))
        screen.blit(legend2, (650, 735))
        if shark_bullet_skill_ready:
            screen.blit(shark_bullet, shark_bullet_skill_surface)
        screen.blit(score_surface, (200, 700))
        screen.blit(current_stage_surface, (30, 700))
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
                if event.key == pygame.K_ESCAPE:
                    stage_of_game = "starting menu"
                    reset_zombies = True
                    starting_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if sound_rect.collidepoint(event.pos) and sound_turned_on:
                    sound_turned_on = False
                elif sound_rect.collidepoint(event.pos) and not sound_turned_on:
                    sound_turned_on = True
                elif back_to_menu_surface.collidepoint(event.pos):
                    stage_of_game = "starting menu"
                elif again_button.collidepoint(event.pos):
                    fill_zombies_stage3(zombies_stage3)
                    score = 0
                    stage_of_game = 1
                    reset_zombies = True
                    summon_final_boss = True
                elif quit_button.collidepoint(event.pos):
                    quit()
                elif shark_bullet_skill_surface.collidepoint(event.pos):
                    shark_bullet_skill_ready = False
                    for i in range(1, 6):
                        new_shark_bullet = Bullet(shark_bullet)
                        new_shark_bullet.rect.y = 60 + 140*(i-1)
                        bullets.append(new_shark_bullet)

            if event.type == ADD_ZOMBIE_EVENT:
                zombie = Zombie(zombie1)
                get_zombie_list_based_on_stage().append(zombie)

            if event.type == SHARK_SKILL_READY:
                shark_bullet_skill_ready = True

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
            for zombie in get_zombie_list_based_on_stage():
                if bullet_in_list.rect.colliderect(zombie.rect) and bullet_in_list.visible:
                    zombie.hit_points -= bullet_in_list.damage
                    bullet_in_list.visible = False
                    if zombie.hit_points <= 0:
                        velocity += 0.3
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
                        elif zombie.name_image == zombie_boss:
                            score += 60
                            zombie.rect.x = 1580
                            zombie.rect.y = random.choice(random_y_spawning_positions[0:4])
                            zombie.hit_points = 12
                        elif zombie.name_image == final_boss:
                            zombies_stage3.clear()

        if score > 200:
            stage_of_game = 2
        if score > 400:
            stage_of_game = 3
        if score > 550 and summon_final_boss:
            reset_zombies_x_position(10000)
            dragon = Zombie(final_boss)
            get_zombie_list_based_on_stage().append(dragon)
            velocity = 0.1
            pygame.time.set_timer(ADD_ZOMBIE_EVENT, 300000)
            summon_final_boss = False

        for zombie in get_zombie_list_based_on_stage():
            velocity += 0.2
            zombie.rect.x -= velocity
            if zombie.hit_points > 0:
                screen.blit(zombie.name_image, zombie.rect)
            if zombie.rect.colliderect(sniper_rect):
                stage_of_game = "starting menu"
                score = 0
            if zombie.rect.x < -100:
                stage_of_game = "starting menu"
                score = 0

        if fire_bullet_to_catch.visible:
            screen.blit(fire_bullet, fire_bullet_to_catch.rect)
            fire_bullet_to_catch.rect.x -= 10
            if fire_bullet_to_catch.rect.colliderect(sniper_rect):
                fire_bullet_to_catch.visible = False
                fire_ammunition = True
                pygame.time.set_timer(RESET_FIRE_EVENT, 5000)

        if len(zombies_stage3) == 0:
            screen.blit(again_text, (530, 350))
            screen.blit(quit_text, (845, 350))
            screen.blit(congratz, (430, 200))
            screen.blit(clickable_square, again_button)
            screen.blit(clickable_square, quit_button)

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
