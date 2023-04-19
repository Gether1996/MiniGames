import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("SNAKE")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pos_x_snake_head = random.randint(0, 950)
pos_y_snake_head = random.randint(0, 550)
pos_x_food = random.randint(0, 980)
pos_y_food = random.randint(0, 580)
snake_head_size = 50
snake_body_size = 40

horizontal_barrier_top = pygame.Rect(0, -1, 1000, 1)
horizontal_barrier_bottom = pygame.Rect(0, 601, 1000, 1)
vertical_barrier_left = pygame.Rect(-1, 0, 1, 1000)
vertical_barrier_right = pygame.Rect(1001, 0, 1, 1000)
barriers = [horizontal_barrier_top, horizontal_barrier_bottom, vertical_barrier_left, vertical_barrier_right]

move_x = 0
move_y = 0

clock = pygame.time.Clock()
FPS = 5

snake_bodies_count = 0
snake_bodies_list = []

while True:
    snake_head = pygame.Rect(pos_x_snake_head, pos_y_snake_head, snake_head_size, snake_head_size)
    food = pygame.Rect(pos_x_food, pos_y_food, 20, 20)
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, snake_head)
    pygame.draw.rect(screen, RED, food)

    pygame.draw.rect(screen, WHITE, horizontal_barrier_top)
    pygame.draw.rect(screen, WHITE, horizontal_barrier_bottom)
    pygame.draw.rect(screen, WHITE, vertical_barrier_left)
    pygame.draw.rect(screen, WHITE, vertical_barrier_right)

    pygame.display.update()
    clock.tick(FPS)

    if snake_head.colliderect(food):
        pos_x_food = random.randint(0, 970)
        pos_y_food = random.randint(0, 570)
        snake_bodies_count += 1

    for i in range(snake_bodies_count):
        snake_body = pygame.Rect(pos_x_snake_head + i*35, pos_y_snake_head, snake_body_size, snake_body_size)
        snake_bodies_list.append(snake_body)

    for body in snake_bodies_list:
        pygame.draw.rect(screen, GREEN, body)
    pygame.display.update()

    for barrier in barriers:
        if snake_head.colliderect(barrier):
            pos_x_snake_head = random.randint(0, 935)
            pos_y_snake_head = random.randint(0, 535)
            move_x = 0
            move_y = 0
            snake_head_size = 50
            snake_bodies_count = 0
            snake_bodies_list = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_x = -20
                move_y = 0
            if event.key == pygame.K_RIGHT:
                move_x = 20
                move_y = 0
            if event.key == pygame.K_UP:
                move_x = 0
                move_y = -20
            if event.key == pygame.K_DOWN:
                move_x = 0
                move_y = 20

    pos_x_snake_head += move_x
    pos_y_snake_head += move_y
