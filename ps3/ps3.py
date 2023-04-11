# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Lucca Rodrigues
# Collaborators : N/A
# Time spent    : -

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

        The score for a word is the product of two components:

        The first component is the sum of the points for letters in the word.
        The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

        Letters are scored as in Scrabble; A is worth 1, B is
        worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    score_component_1 = sum(
        [SCRABBLE_LETTER_VALUES[letter]
            for letter in word.lower() if letter != '*']
    )

    score_component_2 = max((7 * len(word) - 3 * (n - len(word))), 1)

    return score_component_1 * score_component_2

#
# Make sure you understand how this function works and what it does!
#


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    hand['*'] = 1

    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()

    # use letters from hand
    for letter in word.lower():
        if (letter in new_hand):
            new_hand[letter] -= 1

    # Remove letters with negative counts
    # note: uses dictionary comprehension!
    new_hand = {k: v for (k, v) in new_hand.items() if v > 0}

    return new_hand

#
# Problem #3: Test word validity
#


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    # if word contains a wildcard, test all vowel substitutions
    if ('*' in word.lower()):
        for vowel in VOWELS:
            new_word = word.replace('*', vowel)
            if (new_word in word_list):
                return True

    if (word.lower() not in word_list):
        return False

    # now check hand of letters
    new_hand = hand.copy()

    for letter in word.lower():
        if (letter not in new_hand):
            return False

        new_hand[letter] -= 1

        # check if we ran out of letters
        if (new_hand[letter] < 0):
            return False

    return True


#
# Problem #5: Playing a hand
#


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """

    return len(hand)


def play_hand(hand, word_list):

    # word_list = load_words()
    # hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd': 1, 'w': 1, 'e': 2}
    # hand = {'a': 1, 'j': 1, 'e': 1, 'f': 1, '*': 1, 'r': 1, 'x': 1}
    # hand = {'a': 1, 'c': 1, 'f': 1, 'i': 1, '*': 1, 't': 1, 'x': 1}
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    total_score = 0
    current_hand = hand.copy()

    # As long as there are still letters left in the hand:
    while calculate_handlen(current_hand) > 0:

        # Display the hand
        print('\nCurrent hand:', end=' ')
        display_hand(current_hand)

        # Ask user for input
        input_word = input(
            "Please enter a word or '!!' to indicate you are done: "
        )

        # If the input is two exclamation points:
        if (input_word == '!!'):
            # End the game (break out of the loop)
            break

        # Otherwise (the input is not two exclamation points):

        # If the word is valid:
        if is_valid_word(input_word, current_hand, word_list):
            word_score = get_word_score(
                input_word, calculate_handlen(current_hand)
            )
            total_score += word_score
            # Tell the user how many points the word earned,
            # and the updated total score
            print(
                f'"{input_word}" earned {word_score} points. Total: {total_score} points'
            )

        # Otherwise (the word is not valid):
        else:
            # Reject invalid word (print a message)
            print('That is not a valid word. Please choose another word.')

        # update the user's hand by removing the letters of their inputted word
        current_hand = update_hand(current_hand, input_word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print()
    if (calculate_handlen(current_hand) <= 0):
        print(f'Ran out of letters')

    print(f'Total score for this hand: {total_score} points')

    # Return the total score as result of function
    return total_score

#
# Problem #6: Playing a game
#


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    new_hand = hand.copy()

    # letter not in hand -> keep hand intact
    if (letter not in new_hand.keys()):
        return new_hand

    # find a replacement letter
    new_letter = random.choice(VOWELS + CONSONANTS)
    new_hand[new_letter] = new_hand[letter]

    # remove original letter from hand
    del new_hand[letter]

    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    num_hands = int(input('Enter total number of hands: '))

    # initialize game state
    letter_substituted = False
    hand_replayed = False
    first_play = True
    total_score = 0
    hands_used = 0
    hand = {}

    while hands_used <= num_hands:

        # prompt user to replay a hand
        if (not hand_replayed and not first_play):
            replay_input = input('Would you like to replay the hand? ')

            # don't replay the previous hand
            if (replay_input == 'no'):

                # first check if the user has run out of hands
                if (hands_used == num_hands):
                    continue

                # deal a new hand
                else:
                    hands_used += 1
                    hand = deal_hand(HAND_SIZE)

            # replay the previous hand
            if (replay_input == 'yes'):
                hand_replayed = True
        else:
            # first check if the user has run out of hands
            if (hands_used == num_hands):
                break

            # deal a new hand
            else:
                hands_used += 1
                hand = deal_hand(HAND_SIZE)

        # show current hand
        print('Current hand:', end=' ')
        display_hand(hand)

        # prompt user to substitute a letter
        if (not letter_substituted):
            subs_input = input(
                'Would you like to substitute a letter? '
            )

            # substitute a letter
            if (subs_input == 'yes'):
                letter_to_replace = input(
                    'Which letter would you like to replace: '
                )
                hand = substitute_hand(hand, letter_to_replace)
                letter_substituted = True

            # don't substitute any letters
            if (subs_input == 'no'):
                pass

        total_score += play_hand(hand, word_list)
        print('----------')

        first_play = False

    print(f'Total score over all hands: {total_score} points')


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

# hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
# words_list = load_words()
