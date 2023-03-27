import random
import os


def print_hangman(wrong):
    stages = [
        """
        +---+
        |   |
            |
            |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
            |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
        |   |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|   |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|\  |
            |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|\  |
       /    |
            |
        =========
        """,
        """
        +---+
        |   |
        O   |
       /|\  |
       / \  |
            |
        =========
        """
    ]
    print(stages[wrong])
    if wrong == 6:
        print("Sorry, but your game ends here. You ran out of tries.")
        again()


def again():
    again = input("Wanna play again?(y/n): ")
    while again.lower() not in "yn":
        again = input("Invalid response. Please enter 'y' or 'n': ")
    quit() if again == "n" else run_game()


def take_guess():
    guess = input("Guess a character: ")
    while len(guess) > 1:
        guess = input("Please insert only 1 character: ")
    return guess


def run_game():
    random_word = random.choice(words)
    right_guess = 0
    wrong_guess = 0
    guesses_done = []
    underscores = ["_" for char in random_word]
    print("Welcome to Hangman!\n")

    while right_guess < len(random_word):
        print("\n")
        print(" ".join(underscores))
        print("\n")
        guess = take_guess()
        os.system("cls")
        if guess in guesses_done:
            print_hangman(wrong_guess)
            print("Wrong input, this character is already used.\n")
            guesses_string = ", ".join(guesses_done)
            print(f"Letters guessed so far: {guesses_string}")
            continue
        elif guess in random_word:
            indexes = [i for i, char in enumerate(random_word) if char == guess]
            for index in indexes:
                underscores[index] = guess
            right_guess += len(indexes)
            guesses_done.append(guess)
            guesses_string = ", ".join(guesses_done)
            print_hangman(wrong_guess)
            print("Correct!")
            print(f"Letters guessed so far: {guesses_string}")
        else:
            wrong_guess += 1
            guesses_done.append(guess)
            print_hangman(wrong_guess)
            guesses_string = ", ".join(guesses_done)
            print("Wrong, let's try again.")
            print(f"Letters guessed so far: {guesses_string}")

    else:
        print(f"\nYou did it! Congratulations, the hidden word was {random_word.upper()}.")
        again()


words = ["car", "motorcycle", "glass", "hippo", "cheese", "python", "gameboy"]
run_game()

