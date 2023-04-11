# Problem Set 2, hangman.py
# Name: Lucca Rodrigues
# Collaborators: N/A
# Time spent: 3h00

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word_letters = set(secret_word)

    for letter in secret_word_letters:
        if (letter not in letters_guessed):
            return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''

    for char in secret_word:
        if (char in letters_guessed):
            guessed_word += char
        else:
            guessed_word += '_ '

    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    for letter in string.ascii_lowercase:
        if (letter not in letters_guessed):
            available_letters += letter

    return available_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''

    # game state
    guesses = 6
    warnings = 3
    letters_guessed = []

    # start prompt
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')

    while (guesses > 0 and not is_word_guessed(secret_word, letters_guessed)):
        print('-------------')
        print(f'You have {guesses} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')

        # get user input
        input_char = input('Please guess a letter: ').lower()

        # check if the input is invalid
        if (not str.isalpha(input_char) or len(input_char) != 1):
            if (warnings > 0):
                warnings -= 1
                print(
                    f'Oops! That is not a valid letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}'
                )
                continue

            else:
                guesses -= 1
                print(
                    f'Oops! That is not a valid letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}'
                )
                continue

        # check if letter is available
        if (input_char in get_available_letters(letters_guessed)):
            letters_guessed.append(input_char)
        # letter already guessed before
        else:
            if (warnings > 0):
                warnings -= 1
                print(
                    f"Oops! You've already guessed that letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}"
                )
                continue

            else:
                guesses -= 1
                print(
                    f"Oops! You've already guessed that letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}"
                )
                continue

        # incorrect letter
        if (input_char not in secret_word):
            # vowel     -> deduct two guesses
            # consonant -> deduct one guess
            vowels = ['a', 'e', 'i', 'o', 'u']
            if (input_char in vowels):
                guesses -= 2
            else:
                guesses -= 1

            print(
                f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}'
            )

        # correct letter
        else:
            print(
                f'Good guess: {get_guessed_word(secret_word, letters_guessed)}'
            )

    # user guessed word correctly
    if (is_word_guessed(secret_word, letters_guessed)):
        print('------------')
        print('Congratulations, you won!')
        print(
            f'Your total score for this game is: {guesses * len(set(secret_word))}')
        return

    # user ran out of guesses
    if (guesses <= 0):
        print('------------')
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.')
        return


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_chars = []
    for char in list(my_word):
        if (char != ' '):
            my_word_chars.append(char)

    other_word_chars = list(other_word)

    if (len(my_word_chars) != len(other_word_chars)):
        return False

    for i in range(len(my_word_chars)):
        char = my_word_chars[i]
        if (char == '_'):
            my_word_chat_set = set(
                [letter for letter in my_word_chars if letter != '_'])
            if (other_word_chars[i] in my_word_chat_set):
                return False
        else:
            if (char != other_word_chars[i]):
                return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    matches = []

    for word in wordlist:
        if (len(word) != my_word):
            pass

        if (match_with_gaps(my_word, word)):
            matches.append(word)

    if (len(matches) > 0):
        return ' '.join(matches)
    else:
        return 'No matches found'


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 

    Follows the other limitations detailed in the problem write-up.
    '''

    # game state
    guesses = 6
    warnings = 3
    letters_guessed = []

    # start prompt
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')

    while (guesses > 0 and not is_word_guessed(secret_word, letters_guessed)):
        print('-------------')
        print(f'You have {guesses} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed)}')

        # get user input
        input_char = input('Please guess a letter: ').lower()

        if (input_char == '*'):
            print('Possible word matches:')
            print(show_possible_matches(
                get_guessed_word(secret_word, letters_guessed)))
            continue

        # check if the input is invalid
        if (not str.isalpha(input_char) or len(input_char) != 1):
            if (warnings > 0):
                warnings -= 1
                print(
                    f'Oops! That is not a valid letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}'
                )
                continue

            else:
                guesses -= 1
                print(
                    f'Oops! That is not a valid letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}'
                )
                continue

        # check if letter is available
        if (input_char in get_available_letters(letters_guessed)):
            letters_guessed.append(input_char)
        # letter already guessed before
        else:
            if (warnings > 0):
                warnings -= 1
                print(
                    f"Oops! You've already guessed that letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}"
                )
                continue

            else:
                guesses -= 1
                print(
                    f"Oops! You've already guessed that letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}"
                )
                continue

        # incorrect letter
        if (input_char not in secret_word):
            # vowel     -> deduct two guesses
            # consonant -> deduct one guess
            vowels = ['a', 'e', 'i', 'o', 'u']
            if (input_char in vowels):
                guesses -= 2
            else:
                guesses -= 1

            print(
                f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}'
            )

        # correct letter
        else:
            print(
                f'Good guess: {get_guessed_word(secret_word, letters_guessed)}'
            )

    # user guessed word correctly
    if (is_word_guessed(secret_word, letters_guessed)):
        print('------------')
        print('Congratulations, you won!')
        print(
            f'Your total score for this game is: {guesses * len(set(secret_word))}')
        return

    # user ran out of guesses
    if (guesses <= 0):
        print('------------')
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.')
        return


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # secret_word = 'lawyer'
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    secret_word = 'apple'
    hangman_with_hints(secret_word)
