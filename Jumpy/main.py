import pygame
import random

pygame.init()
pygame.mixer.init(frequency=44100)
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Jumpy")
clock = pygame.time.Clock()

background = pygame.image.load('images/background.jpg').convert()
bird = pygame.image.load('images/bird.png').convert_alpha()
thunder = pygame.image.load('images/thunder.png').convert_alpha()
cloud = pygame.image.load('images/cloud.png').convert_alpha()
tornado = pygame.image.load('images/tornado.png').convert_alpha()
keys = pygame.image.load('images/keys.png').convert_alpha()
heart = pygame.image.load('images/heart.png').convert_alpha()

pygame.mixer.music.load('song.mp3')

tornado_x, thunder_x, cloud_x = 1200, 1200, 1200
tornado_y, thunder_y, cloud_y = 220, 20, 480
bird_y = 250
bird_x = 100
HP = 3
thunder_mov_speed = 1
cloud_mov_speed = 1.5
tornado_mov_speed = 2

bird_rect = bird.get_rect(center=(bird_x, bird_y))
bird_rect = bird_rect.inflate(-30, -30)
thunder_rect = thunder.get_rect(topleft=(thunder_x, thunder_y))
thunder_rect = thunder_rect.inflate(-30, 0)
cloud_rect = cloud.get_rect(topleft=(cloud_x, cloud_y))
tornado_rect = tornado.get_rect(topleft=(tornado_x, tornado_y))
tornado_rect = tornado_rect.inflate(-30, -30)

font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()
pygame.mixer.music.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird_y -= 100
            if event.key == pygame.K_RIGHT:
                bird_x += 50
            if event.key == pygame.K_LEFT:
                bird_x -= 50

    elapsed_time = pygame.time.get_ticks() / 1000
    cycle_time = elapsed_time % 3
    if cycle_time < 3 / 2:
        thunder_y += 2
    else:
        thunder_y -= 2

    if bird_rect.colliderect(thunder_rect) or bird_rect.colliderect(tornado_rect):
        HP -= 1
        thunder_x = 1100
        tornado_x = 1500
        cloud_x = 1300
        bird_y = 250
        bird_x = 100


    if HP == 0:
        exit()
    if bird_y < -1:
        bird_y = 0

    if bird_x < -1:
        bird_x = 0

    if bird_x > 940:
        bird_x = 940

    if bird_y == 650:
        HP -= 1
        thunder_x = 1100
        tornado_x = 1500
        cloud_x = 1300
        bird_y = 250
        bird_x = 100


    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = int(elapsed_time / 60000)
    seconds = int((elapsed_time - minutes * 60000) / 1000)
    milliseconds = elapsed_time - minutes * 60000 - seconds * 1000
    timer_text = '{:02d}:{:02d}:{:03d}'.format(minutes, seconds, milliseconds)

    timer_surface = font.render(timer_text, True, "White")
    timer_rect = timer_surface.get_rect(topright=(980, 10))

    screen.blit(background, (0, 0))
    for i in range(HP):
        screen.blit(heart, (20 + 80*i, 20))
    screen.blit(keys, (810, 480))
    screen.blit(bird, bird_rect)
    screen.blit(thunder, thunder_rect)
    screen.blit(cloud, cloud_rect)
    screen.blit(tornado, tornado_rect)
    screen.blit(timer_surface, timer_rect)
    pygame.display.update()
    clock.tick(60)

    thunder_x -= thunder_mov_speed
    thunder_rect.x = thunder_x
    thunder_rect.y = thunder_y
    if thunder_x < -300:
        thunder_x = 1100
        thunder_y = random.randint(10, 500)
        thunder_mov_speed += 0.5

    cloud_x -= cloud_mov_speed
    cloud_rect.x = cloud_x
    cloud_rect.y = cloud_y
    if cloud_x < -300:
        cloud_x = 1100
        cloud_y = random.randint(10, 550)
        cloud_mov_speed += 0.4

    tornado_x -= tornado_mov_speed
    tornado_rect.x = tornado_x
    tornado_rect.y = tornado_y
    if tornado_x < -300:
        tornado_x = 1500
        tornado_y = random.randint(10, 450)
        tornado_mov_speed += 0.4

    bird_y += 2
    bird_rect.y = bird_y
    bird_rect.x = bird_x



