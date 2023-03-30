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
guide = FONT.render("Insert character: ", True, BLACK)
guide2 = FONT.render("Guesses so far: ", True, BLACK)

while True:
    random_word = random.choice(words)
    hangman_status = 0
    list_guesses_so_far = []
    guesses_string = ", ".join(list_guesses_so_far)
    guesses_surface = FONT.render(guesses_string, True, BLACK)
    guess = ""
    guess_surface = FONT.render(guess, True, BLACK)

    while hangman_status < 6:
        win.fill(WHITE)
        win.blit(images[hangman_status], (300, 20))
        win.blit(guide, (10, 400))
        win.blit(guide2, (10, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode in string.ascii_letters and len(guess) < 1:
                    guess += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN:
                    if guess == "" or guess in list_guesses_so_far:
                        continue
                    else:
                        if guess not in random_word:
                            hangman_status += 1
                        list_guesses_so_far.append(guess)
                        guess = ""
                        guesses_string = ", ".join(list_guesses_so_far)
                        guesses_surface = FONT.render(guesses_string, True, BLACK)

                guess_surface = FONT.render(guess, True, (0, 0, 0))

        win.blit(guess_surface, (220, 400))
        win.blit(guesses_surface, (220, 450))
        pygame.display.update()
