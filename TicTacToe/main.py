import pygame

pygame.init()
screen = pygame.display.set_mode((540, 640))
pygame.display.set_caption("TicTac")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

lower_bar = pygame.rect.Rect(0, 540, 540, 100)
imageX = pygame.image.load("imageX.png")
imageO = pygame.image.load("imageO.png")
FONT = pygame.font.SysFont("Comic Sans MS", 26)
again_text = FONT.render("AGAIN", True, BLACK)
again_rect = pygame.rect.Rect(20, 560, 140, 60)


SQUARE_SIZE = 178
GAP_SIZE = 2

winning_positions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]


def check_for_win(player_squares):
    if len(player_squares) >= 3:
        for position in winning_positions:
            if set(position).issubset(player_squares):
                return True
    return False


squares = []
number = 0
for row in range(3):
    for column in range(3):
        x = column * (SQUARE_SIZE + GAP_SIZE)
        y = row * (SQUARE_SIZE + GAP_SIZE)
        square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        squares.append({"rect": square_rect, "revealed": False, "number": number})
        number += 1

player = "X"
revealed_squares = []
player_X_squares = []
player_X_wins = 0
player_O_squares = []
player_O_wins = 0


while True:

    text1 = FONT.render(f"X wins: {player_X_wins}", True, WHITE)
    text2 = FONT.render(f"O wins: {player_O_wins}", True, WHITE)
    which_player_is_playing = FONT.render(f"{player}'s move", True, WHITE)

    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, lower_bar)
    pygame.draw.rect(screen, WHITE, again_rect)
    screen.blit(which_player_is_playing, (220, 570))
    screen.blit(again_text, (45, 570))
    screen.blit(text1, (380, 550))
    screen.blit(text2, (380, 590))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for square_data in squares:
                if square_data["rect"].collidepoint(mouse_pos) and not square_data["revealed"]:
                    square_data["revealed"] = True
                    if player == "X":
                        player = "O"
                        square_data["shape"] = "X"
                        revealed_squares.append(square_data)
                        player_X_squares.append(square_data["number"])
                    else:
                        player = "X"
                        square_data["shape"] = "O"
                        revealed_squares.append(square_data)
                        player_O_squares.append(square_data["number"])

            if again_rect.collidepoint(mouse_pos):
                for square_data in squares:
                    square_data["revealed"] = False
                revealed_squares = []
                player_X_squares = []
                player_O_squares = []

    if check_for_win(player_X_squares):
        player_X_wins += 1
        pygame.time.wait(1000)
        for square_data in squares:
            square_data["revealed"] = False
        revealed_squares = []
        player_X_squares = []
        player_O_squares = []

    if check_for_win(player_O_squares):
        player_O_wins += 1
        pygame.time.wait(1000)
        for square_data in squares:
            square_data["revealed"] = False
        revealed_squares = []
        player_X_squares = []
        player_O_squares = []

    for square in squares:
        square_rect = square["rect"]
        pygame.draw.rect(screen, WHITE, square_rect)

    for square_data in revealed_squares:
        square_rect = square_data["rect"]
        if square_data["shape"] == "X":
            image = pygame.transform.scale(imageX, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(image, square_rect)
        elif square_data["shape"] == "O":
            image = pygame.transform.scale(imageO, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(image, square_rect)

    pygame.display.update()