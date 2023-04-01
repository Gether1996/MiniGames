import random
import pygame
import string

# display
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# sounds
correct = pygame.mixer.Sound('sounds/correct-choice-43861.mp3')
wrong = pygame.mixer.Sound('sounds/wrong-100536.mp3')
won = pygame.mixer.Sound('sounds/success-1-6297.mp3')
failed = pygame.mixer.Sound('sounds/failure-1-89170.mp3')

# images
images = []
for i in range(7):
    image = pygame.image.load(f"images/hangman{i}.png")
    images.append(image)
heart = pygame.image.load("images/heart.png")


class Category:

    def __init__(self, name, items):
        self.name = name
        self.items = items


human_body = Category("Human Body",
                      ['head', 'shoulder', 'armpit', 'forearm', 'finger', 'nose', 'foot', 'nail', 'heart', 'liver',
                       'lungs', 'stomach', 'brain', 'spine', 'knuckle', 'knee', 'elbow', 'toes', 'palm', 'eyebrow',
                       'teeth', 'tongue', 'thigh', 'hip', 'ribs', 'neck', 'ear', 'cheek', 'lip', 'chin'])
occupations = Category("Occupations",
                       ['doctor', 'lawyer', 'teacher', 'engineer', 'nurse', 'pilot', 'chef', 'scientist', 'artist',
                        'musician', 'writer', 'programmer', 'accountant', 'architect', 'firefighter', 'police officer',
                        'salesperson', 'mechanic', 'athlete', 'entrepreneur', 'designer', 'pharmacist', 'psychologist',
                        'dentist', 'veterinarian', 'electrician', 'plumber', 'carpenter', 'farmer'])
brands = Category("Brands",
                  ['nike', 'adidas', 'apple', 'samsung', 'google', 'amazon', 'tesla', 'microsoft', 'sony', 'cocacola',
                   'pepsi', 'toyota', 'mcdonalds', 'bugatti', 'gucci', 'prada', 'louisvuitton', 'chanel', 'ferrari',
                   'rolex', 'omega', 'puma', 'underarmour', 'bmw', 'mercedes', 'audi', 'volkswagen', 'honda'])
animals = Category("Animals",
                   ['dog', 'ladybug', 'lion', 'tiger', 'elephant', 'giraffe', 'zebra', 'monkey', 'bear', 'fox', 'wolf',
                    'rabbit', 'horse', 'deer', 'sheep', 'cat', 'hamster', 'snake', 'crocodile', 'penguin', 'dolphin',
                    'shark', 'whale', 'owl', 'seagull', 'butterfly', 'octopus', 'crab', 'lobster'])
plants = Category("Plants",
                  ['tree', 'flower', 'grass', 'weed', 'cactus', 'mushroom', 'fern', 'ivy', 'oak', 'bamboo', 'rose',
                   'lily', 'daisy', 'tulip', 'sunflower', 'maple', 'palm', 'pine', 'cherry', 'apple', 'orange',
                   'watermelon', 'banana', 'coconut', 'aloe vera', 'lavender', 'peppermint', 'coriander', 'basil'])
diseases = Category("Diseases",
                    ['cancer', 'diabetes', 'arthritis', 'alzheimer', 'asthma', 'hypertension', 'malaria',
                     'tuberculosis', 'ebola', 'parkinson', 'hiv', 'headache', 'pneumonia', 'jaundice', 'leprosy'])
hobbies = Category("Hobbies",
                   ['photography', 'gardening', 'cooking', 'painting', 'reading', 'writing', 'knitting', 'sewing',
                    'scrapbooking', 'origami', 'woodworking', 'calligraphy', 'embroidery', 'cross-stitch', 'quilling'])
sports = Category("Sports",
                  ['football', 'basketball', 'tennis', 'golf', 'boxing', 'swimming', 'cycling', 'volleyball',
                   'baseball', 'hockey', 'cricket', 'rugby', 'skiing', 'snowboarding', 'skateboarding'])
meals = Category("Meals",
                 ['lasagna', 'sushi', 'tacos', 'pizza', 'hamburger', 'ramen', 'steak', 'curry',
                  'pancakes', 'rice', 'spaghetti', 'quesadilla', 'gnocchi', 'samosa', 'dumplings'])
all_categories = [human_body, occupations, brands, animals, plants, diseases, hobbies, sports, meals]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("Comic Sans MS", 20)
FONT_BIGGER = pygame.font.SysFont("Comic Sans MS", 40)
guide = FONT.render("Type a character: ", True, BLACK)
guide2 = FONT.render("Guesses so far: ", True, BLACK)
guide4 = FONT.render("- press Enter to confirm", True, BLACK)
guide5 = FONT.render("- press Backspace to erase", True, BLACK)

while True:  # new game
    # get a random category and word from that category
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
        win.blit(heart, (380, 270))
        win.blit(guide, (20, 410))
        win.blit(guide2, (20, 450))
        win.blit(guide4, (20, 130))
        win.blit(guide5, (20, 170))
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
                            correct.play()
                            indexes = [i for i, char in enumerate(random_word) if char == guess.lower()]
                            for index in indexes:
                                underscores[index] = guess.lower()
                            underscores_string = " ".join(underscores)
                            underscores_surface = FONT_BIGGER.render(underscores_string, True, BLACK)
                            right_guess += len(indexes)
                        elif guess.lower() not in random_word:
                            wrong.play()
                            wrong_guess += 1
                        list_guesses_so_far.append(guess.lower())
                        guess = ""
                        string_guesses_so_far = ", ".join(list_guesses_so_far)
                        surface_guesses_so_far = FONT.render(string_guesses_so_far, True, BLACK)

                guess_surface = FONT.render(guess, True, (0, 0, 0))

        win.blit(guess_surface, (210, 410))
        win.blit(surface_guesses_so_far, (210, 450))
        pygame.display.update()

    # new window after user completes a game, he/she gets to choose new game or to quit.
    win.fill(WHITE)
    message1 = ""
    if right_guess == len(random_word):
        won.play()
        message = f"Congratulations, you guessed the word {random_word.upper()}!"
        if wrong_guess < 2:
            message1 = f"Finished with {wrong_guess} mistake! Impressive."
        else:
            message1 = f"Finished with {wrong_guess} mistakes. Good Job."
    else:
        failed.play()
        message = f"Sorry, you ran out of guesses. The word was {random_word.upper()}."
    message2 = "Press 'n' to start a new game or 'q' to quit."
    message_surface = FONT.render(message, True, BLACK)
    message1_surface = FONT.render(message1, True, BLACK)
    message2_surface = FONT.render(message2, True, BLACK)

    win.blit(message_surface, (30, 200))
    win.blit(message1_surface, (30, 170))
    win.blit(message2_surface, (30, 230))
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
