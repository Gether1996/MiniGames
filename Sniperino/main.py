import pygame
import random

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 900))
pygame.display.set_caption("Sniperino")
clock = pygame.time.Clock()

# sounds
bullet_sound = pygame.mixer.Sound('sounds/shot_sound.mp3')
fire_shot_sound = pygame.mixer.Sound('sounds/fire_shot_sound.mp3')
pygame.mixer.music.load('sounds/music.mp3')

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
shark_bullet_bigger = pygame.image.load('images/shark_bigger.png').convert_alpha()
sound_on = pygame.image.load('images/sound_on.png').convert_alpha()
sound_off = pygame.image.load('images/sound_off.png').convert_alpha()
clickable_square = pygame.image.load('images/clickable_square.png').convert_alpha()
info_1 = pygame.image.load('images/info_1.png').convert_alpha()
info_2 = pygame.image.load('images/info_2.png').convert_alpha()
virus = pygame.image.load('images/virus.png').convert_alpha()
push = pygame.image.load('images/push.png').convert_alpha()

random_y_spawning_positions = [20, 160, 300, 440, 580]

# positions and game bar
sniper_position_y = 20
bullet_position_x = 160
virus_position_x = 2500
virus_position_y = random.choice(random_y_spawning_positions)
UI_rect = pygame.Rect(0, 700, 1500, 200)
fire_bullet_to_catch_pos_x = 1600


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
            self.hit_points = 50


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
            self.damage = 12
            self.rect = self.name_image.get_rect(center=(bullet_position_x, sniper_position_y + 40))


class Virus:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(virus_position_x, virus_position_y))


# colors & fonts
BROWN = (205, 133, 63)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Comic Sans MS", 36)
FONT_BIGGER = pygame.font.SysFont("Comic Sans MS", 60)

# new events
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

# push_skill usable each 45sec
PUSH_SKILL_READY = pygame.USEREVENT + 5
pygame.time.set_timer(PUSH_SKILL_READY, 25000)

# creating starting zombies and viruses
zombies_stage1 = []      # 5x zombie1, 1x zombie2
zombies_stage2 = []      # 5x zombie1, 4x zombie2, 1x zombie_boss
zombies_stage3 = []      # 5x zombie1, 4x zombie2, 3x zombie_boss
zombies_stage4 = []
viruses = []             # 1 for each stage
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

for t in range(3):
    new_virus = Virus(virus)
    viruses.append(new_virus)

# starting stats
bullets = []
boxes = []
sound_turned_on = True
fire_ammunition = False
fire_bullet_to_catch = Bullet(fire_bullet)
fire_bullet_to_catch.visible = False
score = 0
player_name = ""
stage_of_game = "starting menu"
reset_zombies = True
summon_final_boss = True
show_info_of_game = False
shark_bullet_skill_ready = False
push_skill_ready = False
infinite_game = False
input_box_active = False
got_player_name = False


# functions
def get_best_score():
    with open("record.txt", "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            best_score = int(lines[0].strip())
            best_name = ""
        else:
            best_score = int(lines[0].strip())
            best_name = lines[1].strip()
        return best_score, best_name


def update_best_score(points, name):
    best_score, best_name = get_best_score()
    if points > best_score and len(name) > 0:
        with open("record.txt", "w") as f:
            f.write(str(points) + "\n" + name)
    else:
        with open("record.txt", "w") as f:
            f.write(str(points) + "\n" + "Unknown")


def get_zombie_list_based_on_stage():
    if stage_of_game == 1:
        return zombies_stage1
    elif stage_of_game == 2:
        return zombies_stage2
    elif stage_of_game == 3:
        return zombies_stage3
    else:
        return zombies_stage4


def get_viruses_based_on_stage():
    if stage_of_game == 1:
        return viruses[0:1]
    elif stage_of_game == 2:
        return viruses[0:2]
    else:
        return viruses[0:3]


def reset_zombies_and_viruses_x_position(x_position):
    velocity = 0.2
    pygame.time.set_timer(ADD_ZOMBIE_EVENT, 30000)
    for i, zombie in enumerate(get_zombie_list_based_on_stage()):
        zombie.rect.x = x_position + i * 150
    for i, virus in enumerate(viruses):
        virus.rect.x = x_position + (i + 1) * 1500
        virus.rect.y = random.choice(random_y_spawning_positions)
    return velocity


def fill_zombies(zombie_list):
    for o in range(8):
        zombie_to_append = Zombie(zombie1)
        zombie_list.append(zombie_to_append)
    for u in range(4):
        zombie2_to_append = Zombie(zombie2)
        zombie_list.append(zombie2_to_append)
    for boss in range(3):
        boss_to_append = Zombie(zombie_boss)
        zombie_list.append(boss_to_append)


pygame.mixer.music.play()
while True:
    while stage_of_game == "starting menu":
        player_name_rect = pygame.Rect(150, 50, 350, 100)
        player_name_rect_color = (0, 255, 127)
        player_name_rect_hover_color = (60, 179, 113)
        input_box_rect = pygame.Rect(130, 40, 370, 120)
        enter_name = FONT_BIGGER.render("Enter name", True, BLACK)
        got_name = FONT_BIGGER.render(f"{player_name}", True, BLACK)
        sniperino_surface = FONT_BIGGER.render("SNIPERINO", True, BLACK)
        created_by = FONT.render("Created by Patrik Kredátus", True, BLACK)
        record, player = get_best_score()
        if len(player) == 0:
            player = "Unknown"
        record_surface = FONT.render(f"Best score: {record} by: {player}", True, BLACK)

        screen.blit(background, (0, 0))
        screen.blit(sniperino_surface, (600, 50))
        screen.blit(record_surface, (550, 130))
        screen.blit(created_by, (550, 850))
        if show_info_of_game:
            screen.blit(info_1, (40, 180))
            screen.blit(info_2, (880, 250))

        for i in range(3):
            again_button = clickable_square.get_rect(topleft=(665, 250 + i * 120))
            screen.blit(clickable_square, again_button)
            boxes.append(again_button)
        text1 = FONT.render("START", True, BLACK)
        text2 = FONT.render("INFO", True, BLACK)
        text3 = FONT.render("QUIT", True, BLACK)
        screen.blit(text1, (700, 270))
        screen.blit(text2, (715, 390))
        screen.blit(text3, (710, 510))

        if player_name_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, player_name_rect_hover_color, player_name_rect)
        else:
            pygame.draw.rect(screen, player_name_rect_color, player_name_rect)
        if input_box_active:
            pygame.draw.rect(screen, WHITE, input_box_rect)

        if len(player_name) > 0:
            screen.blit(got_name, (165, 60))
        else:
            screen.blit(enter_name, (165, 60))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if input_box_active:
                    if event.key == pygame.K_RETURN and len(player_name) > 0:
                        input_box_active = False
                        got_player_name = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if player_name_rect.collidepoint(event.pos):
                    input_box_active = True
                if boxes[0].collidepoint(event.pos):
                    stage_of_game = 1
                    reset_zombies = True
                    show_info_of_game = False
                    pygame.time.set_timer(ADD_ZOMBIE_EVENT, 30000)
                elif boxes[1].collidepoint(event.pos):
                    show_info_of_game = True
                elif boxes[2].collidepoint(event.pos):
                    quit()
                if player_name_rect.collidepoint(event.pos):
                    input_box_active = True

    while stage_of_game in [1, 2, 3, 4]:
        if reset_zombies:
            reset_zombies = False
            reset_zombies_and_viruses_x_position(1500)
            shark_bullet_skill_ready = False
            push_skill_ready = False
        sniper_rect = sniper.get_rect(topleft=(30, sniper_position_y))
        sound_rect = sound_on.get_rect(topleft=(360, 760))
        back_to_menu_surface = clickable_square.get_rect(topleft=(100, 750))
        back_to_menu_text = FONT.render("MENU", True, BLACK)
        shark_key = FONT.render("Y", True, BLACK)
        push_key = FONT.render("X", True, BLACK)
        score_surface = FONT.render(f"Score: {score}", True, BLACK)
        current_stage_surface = FONT_BIGGER.render(f"Stage: {stage_of_game}", True, BLACK)
        velocity = 0.2
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, BROWN, UI_rect)
        screen.blit(clickable_square, back_to_menu_surface)
        screen.blit(back_to_menu_text, (145, 770))
        screen.blit(score_surface, (1250, 730))
        screen.blit(current_stage_surface, (1220, 790))
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
                if event.key == pygame.K_y and shark_bullet_skill_ready:
                    shark_bullet_skill_ready = False
                    for i in range(1, 6):
                        new_shark_bullet = Bullet(shark_bullet)
                        new_shark_bullet.rect.y = 60 + 140*(i-1)
                        bullets.append(new_shark_bullet)
                if event.key == pygame.K_x and push_skill_ready:
                    push_skill_ready = False
                    for zombie in get_zombie_list_based_on_stage():
                        zombie.rect.x += 400

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if sound_rect.collidepoint(event.pos) and sound_turned_on:
                    sound_turned_on = False
                elif sound_rect.collidepoint(event.pos) and not sound_turned_on:
                    sound_turned_on = True
                elif back_to_menu_surface.collidepoint(event.pos):
                    stage_of_game = "starting menu"

            if event.type == ADD_ZOMBIE_EVENT:
                zombie = Zombie(zombie1)
                get_zombie_list_based_on_stage().append(zombie)

            if event.type == SHARK_SKILL_READY:
                shark_bullet_skill_ready = True

            if event.type == PUSH_SKILL_READY:
                push_skill_ready = True

            if event.type == FIRE_BULLET_EVENT:
                fire_bullet_to_catch.rect.x = 1600
                fire_bullet_to_catch.rect.y = random.choice(random_y_spawning_positions) + 20
                fire_bullet_to_catch.visible = True

            if event.type == RESET_FIRE_EVENT:
                fire_ammunition = False
                pygame.time.set_timer(RESET_FIRE_EVENT, 0)

        #######################################################    BULLETS / ZOMBIES / VIRUSES     ####################
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
                            infinite_game = True
                            fill_zombies(zombies_stage4)
                            reset_zombies_and_viruses_x_position(1500)

        if score > 1000:
            stage_of_game = 2
        if score > 2500:
            stage_of_game = 3
        if score > 4000 and summon_final_boss:
            reset_zombies_and_viruses_x_position(10000)
            dragon = Zombie(final_boss)
            get_zombie_list_based_on_stage().append(dragon)
            velocity = 0.1
            pygame.time.set_timer(ADD_ZOMBIE_EVENT, 300000)
            summon_final_boss = False
        if score > 4000 and infinite_game:
            stage_of_game = 4

        for zombie in get_zombie_list_based_on_stage():
            velocity += 0.2
            zombie.rect.x -= velocity
            if zombie.hit_points > 0:
                screen.blit(zombie.name_image, zombie.rect)
            if zombie.rect.colliderect(sniper_rect):
                stage_of_game = "starting menu"
                update_best_score(score, player_name)
                score = 0
            if zombie.rect.x < -100:
                stage_of_game = "starting menu"
                update_best_score(score, player_name)
                score = 0

        for virus in get_viruses_based_on_stage():
            screen.blit(virus.image, virus.rect)
            virus.rect.x -= 4
            if virus.rect.x < -200:
                virus.rect.x = random.randint(2000, 3000)
                virus.rect.y = random.choice(random_y_spawning_positions)

            if virus.rect.colliderect(sniper_rect):
                stage_of_game = "starting menu"
                update_best_score(score, player_name)
                score = 0
                reset_zombies = True

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
            pygame.mixer_music.set_volume(1)
        else:
            screen.blit(sound_off, sound_rect)
            bullet_sound.set_volume(0)
            fire_shot_sound.set_volume(0)
            pygame.mixer_music.set_volume(0)

        if shark_bullet_skill_ready:
            screen.blit(shark_bullet_bigger, (580, 780))
            screen.blit(shark_key, (650, 700))

        if push_skill_ready:
            screen.blit(push, (800, 780))
            screen.blit(push_key, (850, 700))

        pygame.display.update()
        clock.tick(60)
