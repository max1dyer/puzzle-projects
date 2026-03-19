from colorama import Fore, Back
import random

"""
Reads a list of 5-letter words from a file and returns them as a list. 
To use create your own text file with 5-letter words, replace "wordle_words.txt" 
with the name of your file in the main function. 
"""
def get_words_from_file(filename):
    with open(filename, "r") as f:
        # Only include lines that are exactly 5 letters long and contain only alphabetic characters
        words = [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]
    return words

"""
Prompts the user to enter a valid 5-letter word from the valid list of words. 
"""
def prompt_five_letter_word(words):
    # Loop until the user enters a valid 5-letter word that is in the list
    while True:
        user_input = input("Enter a 5-letter word: ").strip().lower()
        if len(user_input) != 5:
            print("Please enter exactly 5 letters.")
            continue
        if not user_input.isalpha():
            print("Please use only letters (a-z).")
            continue
        if user_input not in words:
            print("That word is not in the word list.")
            continue
        return user_input

"""
Determines the color feedback for each letter in the user's guess.
    Green: correct letter in the correct position
    Yellow: correct letter in the wrong position
    Gray: incorrect letter or no more occurrences of that letter left in the correct word 
"""
def get_colors(user_word, correct_word, num_letters):
    colors = []
    # First pass to identify green letters and update num_letters
    for i in range(5):
        if user_word[i] == correct_word[i]:
            colors.append("green")
            # num_letters tracks remaining unused letters in the correct word so decrement when letter is used
            num_letters[user_word[i]] -= 1
        else:
            colors.append(None)

    # Second pass to identify yellow and gray letters
    for i in range(5):
        # Only check for yellow and gray if the letter wasn't already marked green
        if colors[i] is None:
            # If the letter is in the correct word and there are still occurrences left, mark as yellow
            if user_word[i] in correct_word and num_letters.get(user_word[i], 0) > 0:
                colors[i] = "yellow"
                num_letters[user_word[i]] -= 1
            # If the letter is not in the correct word or there are no occurrences left, mark as gray
            else:
                colors[i] = "gray"
    
    return colors

"""
Prints the user's guess with colored feedback 
"""
def print_guess(colors, user_word, num_guesses):
    # Map color names to colorama styles
    color_map = {
        "green": Back.GREEN + Fore.WHITE,
        "yellow": Back.YELLOW + Fore.BLACK
    }
    # Reset style after each letter
    reset = Back.RESET + Fore.RESET

    # Build the colored output string
    colored_output = "Guess " + str(num_guesses) + ": "
    for i in range(5):
        # If the color is not gray, apply the corresponding color style to the letter
        if colors[i] != "gray":
            colored_output += color_map[colors[i]] + user_word[i].upper() + reset
        else:
            colored_output += user_word[i].upper()
    print(colored_output)

if __name__ == "__main__":
    words = get_words_from_file("wordle_words.txt")
    # Select a random word from the list
    word = random.choice(words)

    correct_guess = False
    num_guesses = 0
    # Main game loop
    while num_guesses < 6 and not correct_guess:
        # Count number of each letter in word to handle cases with duplicate letters correctly
        num_letters = {}
        for letter in word:
            if letter in num_letters:
                num_letters[letter] += 1
            else:
                num_letters[letter] = 1

        user_word = prompt_five_letter_word(words)
        num_guesses += 1
        colors = get_colors(user_word, word, num_letters)
        print_guess(colors, user_word, num_guesses)
        if user_word == word:
            correct_guess = True
    
    # Output final result
    if correct_guess:
        print(f"Congratulations! You guessed the word '{word}' in {num_guesses} guesses.")
    else:
        print(f"Sorry, you've used all 6 guesses. The word was '{word}'.")