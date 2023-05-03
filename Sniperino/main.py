import pygame

pygame.init()
screen = pygame.display.set_mode((1500, 850))
pygame.display.set_caption("Sniperino")
clock = pygame.time.Clock()

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


bullets = []

while True:
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
                if len(bullets) % 10 == 0 and len(bullets) > 1:
                    bullet_image = fire_bullet
                else:
                    bullet_image = bullet
                fired_shot = bullet_image.get_rect(center=(bullet_position_x, sniper_position_y + 45))
                bullets.append((fired_shot, bullet_image))

    screen.blit(background, (0, 0))
    screen.blit(sniper, (30, sniper_position_y))
    for bullet_rect, bullet_image in bullets:
        bullet_rect.x += 15
        screen.blit(bullet_image, bullet_rect)

    pygame.display.update()
    clock.tick(60)


