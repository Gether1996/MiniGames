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
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Comic Sans MS", 20)
FONT_label = pygame.font.SysFont("Comic Sans MS", 50)

SQUARE_SIZE = 100
GAP_SIZE = 22

squares = []
for row in range(4):
    for column in range(8):
        x = column * (SQUARE_SIZE + GAP_SIZE) + 22
        y = row * (SQUARE_SIZE + GAP_SIZE) + 122
        square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        squares.append({"rect": square_rect, "revealed": False})


label_rect = pygame.Rect(0, 0, WIDTH, 100)
label = FONT_label.render("LOTR - matching game!", True, BLACK)
revealed_squares = []
matches = 0
mismatches = 0
guide = FONT.render("Missed matches: ", True, BLACK)

while True:

    while matches != (len(images)) / 2:
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREY, label_rect)
        screen.blit(guide, (500, 600))
        screen.blit(label, (220, 10))
        mismatches_surface = FONT.render(str(mismatches), True, BLACK)
        screen.blit(mismatches_surface, (700, 600))

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
                        revealed_squares.append(square_data)
                        if len(revealed_squares) == 2:
                            if images[squares.index(revealed_squares[0])] == images[squares.index(revealed_squares[1])]:
                                revealed_squares = []
                                matches += 1
                            else:
                                revealed_squares[0]["revealed"] = False
                                revealed_squares[1]["revealed"] = False
                                revealed_squares = []
                                mismatches += 1



