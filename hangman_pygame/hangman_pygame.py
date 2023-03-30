import random

import pygame
import string

# display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# images
images = []
for i in range(7):
    image = pygame.image.load(f"images/hangman{i}.png")
    images.append(image)

# game variables
words = ["car", "motorcycle", "glass", "hippo", "cheese", "python", "gameboy"]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
FONT_BIGGER = pygame.font.Font(None, 60)
guide = FONT.render("Insert character: ", True, BLACK)
guide2 = FONT.render("Guesses so far: ", True, BLACK)

while True:
    random_word = random.choice(words)
    underscores = ["_" for char in random_word]
    underscores_string = " ".join(underscores)
    underscores_surface = FONT_BIGGER.render(underscores_string, True, BLACK)
    right_guess = 0
    wrong_guess = 0
    list_guesses_so_far = []
    string_guesses_so_far = ", ".join(list_guesses_so_far)
    surface_guesses_so_far = FONT.render(string_guesses_so_far, True, BLACK)
    guess = ""
    guess_surface = FONT.render(guess, True, BLACK)

    while wrong_guess < 6 and right_guess < len(random_word):
        win.fill(WHITE)
        win.blit(images[wrong_guess], (300, 20))
        win.blit(guide, (10, 400))
        win.blit(guide2, (10, 450))
        win.blit(underscores_surface, (250, 280))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode in string.ascii_letters and len(guess) < 1:
                    guess += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN:
                    if guess == "" or guess.lower() in list_guesses_so_far:
                        continue
                    else:

                        if guess in random_word:
                            indexes = [i for i, char in enumerate(random_word) if char == guess]
                            for index in indexes:
                                underscores[index] = guess
                            underscores_string = " ".join(underscores)
                            underscores_surface = FONT_BIGGER.render(underscores_string, True, BLACK)
                            right_guess += len(indexes)
                        elif guess not in random_word:
                            wrong_guess += 1
                        list_guesses_so_far.append(guess)
                        guess = ""
                        string_guesses_so_far = ", ".join(list_guesses_so_far)
                        surface_guesses_so_far = FONT.render(string_guesses_so_far, True, BLACK)

                guess_surface = FONT.render(guess, True, (0, 0, 0))

        win.blit(guess_surface, (220, 400))
        win.blit(surface_guesses_so_far, (220, 450))
        pygame.display.update()
