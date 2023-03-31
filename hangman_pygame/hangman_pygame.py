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


class Category:

    def __init__(self, name, items):
        self.name = name
        self.items = items


human_body = Category("Human Body",
                      ['head', 'shoulder', 'armpit', 'forearm', 'finger', 'nose', 'foot', 'nail', 'heart', 'liver',
                       'lungs', 'stomach', 'brain', 'spine', 'knuckle'])
occupations = Category("Occupations",
                       ['doctor', 'lawyer', 'teacher', 'engineer', 'nurse', 'pilot', 'chef', 'scientist', 'artist',
                        'musician', 'writer', 'programmer', 'accountant', 'architect', 'firefighter'])
brands = Category("Brands",
                  ['nike', 'adidas', 'apple', 'samsung', 'google', 'amazon', 'tesla', 'microsoft', 'sony', 'coca-cola',
                   'pepsi', 'toyota', 'mcdonalds', 'kfc', 'burger king'])
animals = Category("Animals",
                   ['dog', 'ladybug', 'lion', 'tiger', 'elephant', 'giraffe', 'zebra', 'monkey', 'bear', 'fox', 'wolf',
                    'rabbit', 'horse', 'deer', 'sheep'])
plants = Category("Plants",
                  ['tree', 'flower', 'grass', 'weed', 'cactus', 'mushroom', 'fern', 'ivy', 'oak', 'bamboo', 'rose',
                   'lily', 'daisy', 'tulip', 'sunflower'])
all_categories = [human_body, occupations, brands, animals, plants]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 28)
FONT_BIGGER = pygame.font.Font(None, 60)
guide = FONT.render("Type a character: ", True, BLACK)
guide2 = FONT.render("Guesses so far: ", True, BLACK)
guide3 = FONT.render("- letters without diacritics", True, BLACK)
guide4 = FONT.render("- press Enter to confirm", True, BLACK)
guide5 = FONT.render("- press Backspace to erase", True, BLACK)

while True:
    # pick a random category and word from that category
    random_category = random.choice(all_categories)
    words = random_category.items
    category_name = random_category.name
    category_surface = FONT_BIGGER.render(category_name, True, BLACK)
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
        win.blit(category_surface, (40, 30))
        win.blit(images[wrong_guess], (480, 40))
        win.blit(guide, (20, 410))
        win.blit(guide2, (20, 450))
        win.blit(guide3, (20, 150))
        win.blit(guide4, (20, 190))
        win.blit(guide5, (20, 230))
        win.blit(underscores_surface, (380, 310))

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

                        if guess.lower() in random_word:
                            indexes = [i for i, char in enumerate(random_word) if char == guess.lower()]
                            for index in indexes:
                                underscores[index] = guess.lower()
                            underscores_string = " ".join(underscores)
                            underscores_surface = FONT_BIGGER.render(underscores_string, True, BLACK)
                            right_guess += len(indexes)
                        elif guess.lower() not in random_word:
                            wrong_guess += 1
                        list_guesses_so_far.append(guess.lower())
                        guess = ""
                        string_guesses_so_far = ", ".join(list_guesses_so_far)
                        surface_guesses_so_far = FONT.render(string_guesses_so_far, True, BLACK)

                guess_surface = FONT.render(guess, True, (0, 0, 0))

        win.blit(guess_surface, (210, 410))
        win.blit(surface_guesses_so_far, (210, 450))
        pygame.display.update()

    win.fill(WHITE)
    if right_guess == len(random_word):
        message = f"Congratulations, you guessed the word {random_word.upper()}!"
    else:
        message = f"Sorry, you ran out of guesses. The word was {random_word.upper()}."
    message1 = "Press 'n' to start a new game or 'q' to quit."
    message_surface = FONT.render(message, True, BLACK)
    message1_surface = FONT.render(message1, True, BLACK)

    win.blit(message_surface, (30, 200))
    win.blit(message1_surface, (30, 230))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    wrong_guess = 0
                    right_guess = 0
                    guess = ""
                    list_guesses_so_far = []
                    random_word = random.choice(words)
                    underscores = ["_" for char in random_word]
                    underscores_string = " ".join(underscores)
                    underscores_surface = FONT_BIGGER.render(underscores_string, True, BLACK)
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    break
        else:
            continue
        break
