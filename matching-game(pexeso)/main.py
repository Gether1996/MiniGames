import random
import pygame

# game screen
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LOTR matching game!")

# images
images = []
for i in range(1, 17):
    image = pygame.image.load(f"images/lotr ({i}).jpg")
    images.append(image)
    images.append(image)
random.shuffle(images)
eye = pygame.image.load("images/eye.png")
ring = pygame.image.load("images/ring.jpg")

# variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (180, 50, 30)
FONT = pygame.font.SysFont("Comic Sans MS", 20)
FONT_label = pygame.font.SysFont("Comic Sans MS", 50)

song = pygame.mixer.Sound('song.mp3')

SQUARE_SIZE = 100
GAP_SIZE = 22

squares = []
for row in range(4):
    for column in range(8):
        x = column * (SQUARE_SIZE + GAP_SIZE) + 22
        y = row * (SQUARE_SIZE + GAP_SIZE) + 122
        square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        squares.append({"rect": square_rect, "revealed": False})


def get_best_score():
    with open("best_score.txt", "r") as f:
        best_score = int(f.read())
        return best_score


def update_best_score(score):
    with open("best_score.txt", "w") as f:
        f.write(str(score))


music_rect = pygame.Rect(20, 600, 150, 100)
label_rect = pygame.Rect(0, 0, WIDTH, 100)
label = FONT_label.render("LOTR - matching game!", True, BLACK)
revealed_squares = []
guide = FONT.render("Missed matches: ", True, WHITE)
guide2 = FONT.render("Record: ", True, WHITE)
song.play()

while True:
    mismatches = 0
    record = get_best_score()
    while not all(square["revealed"] for square in squares):
        screen.fill(BLACK)
        pygame.draw.rect(screen, BROWN, label_rect)
        pygame.draw.rect(screen, BLACK, music_rect)
        screen.blit(guide, (500, 600))
        screen.blit(guide2, (584, 640))
        screen.blit(label, (280, 10))
        screen.blit(eye, (120, 0))
        mismatches_surface = FONT.render(str(mismatches), True, WHITE)
        screen.blit(mismatches_surface, (700, 600))
        if record == 1000:
            pass
        else:
            record_surface = FONT.render(str(record), True, WHITE)
            screen.blit(record_surface, (700, 640))

        for square_data in squares:
            square_rect = square_data["rect"]
            if square_data["revealed"]:
                image_index = squares.index(square_data)
                image = images[image_index]
                image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(image, square_rect)
            else:
                image = pygame.transform.scale(ring, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(image, square_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if music_rect.collidepoint(event.pos):
                    song.stop()
                for square_data in squares:
                    if square_data["rect"].collidepoint(mouse_pos) and not square_data["revealed"]:
                        square_data["revealed"] = True
                        revealed_squares.append(square_data)
                        if len(revealed_squares) == 3:
                            if images[squares.index(revealed_squares[0])] == images[squares.index(revealed_squares[1])]:
                                revealed_squares.pop(0)
                                revealed_squares.pop(0)
                            else:
                                revealed_squares[0]["revealed"] = False
                                revealed_squares[1]["revealed"] = False
                                revealed_squares.pop(0)
                                revealed_squares.pop(0)
                                mismatches += 1

    # new window after user completes a game, he/she gets to choose new game or to quit.
    screen.fill(BLACK)
    message1 = "Congratulations! You have finished the game."
    message2 = "Press 'n' to start a new game or 'q' to quit."

    message1_surface = FONT.render(message1, True, WHITE)
    message2_surface = FONT.render(message2, True, WHITE)

    screen.blit(message1_surface, (30, 170))
    screen.blit(message2_surface, (30, 230))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    if mismatches < record:
                        best_score = mismatches
                        update_best_score(best_score)
                    revealed_squares = []
                    mismatches = 0
                    for square_data in squares:
                        square_data["revealed"] = False
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    break
        else:
            continue
        break


