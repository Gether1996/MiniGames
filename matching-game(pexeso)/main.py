import random
import pygame

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LOTR matching game!")

images = []
for i in range(1, 17):
    image = pygame.image.load(f"images/lotr ({i}).jpg")
    images.append(image)
    images.append(image)
random.shuffle(images)

GREY = (100, 100, 100)
WHITE = (255, 255, 255)

SQUARE_SIZE = 100
GAP_SIZE = 22

label_rect = pygame.Rect(0, 0, WIDTH, 100)

squares = []
for row in range(4):
    for column in range(8):
        x = column * (SQUARE_SIZE + GAP_SIZE) + 22
        y = row * (SQUARE_SIZE + GAP_SIZE) + 122
        square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        squares.append({"rect": square_rect, "revealed": False})

while True:
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREY, label_rect)
    for square_data in squares:
        square_rect = square_data["rect"]
        if square_data["revealed"]:
            image_index = squares.index(square_data)
            image = images[image_index]
            image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(image, square_rect)
        else:
            pygame.draw.rect(screen, GREY, square_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for square_data in squares:
                if square_data["rect"].collidepoint(mouse_pos) and not square_data["revealed"]:
                    square_data["revealed"] = True
                    break
