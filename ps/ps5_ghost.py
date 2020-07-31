# Problem Set 5: Ghost
# Name: 
# Collaborators: 
# Time: 
#

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

# TO DO: your code begins here!
def can_be_word(sequence, word_list):
    """
    Checks if a aequence of letters can form a word by adding more letters.
    sequence is a string.
    Will return True if possible.
    """
    flag = False
    for word in word_list:
        if word[0:len(sequence)] == string.lower(sequence):
            flag = True
            break
    return flag

def is_word(sequence, word_list):
    """
    Checks if a sequence of letters is a word in the wordlist.
    sequence is a string.
    Will return True if it is.
    """
    flag = False
    for word in word_list:
        if word == string.lower(sequence):
            flag = True
            break
    return flag

def letter_input():
    """
    Determines whether the input is an alphabetic character.
    Will return the input letter as a string.
    """
    PlayerInput = str(raw_input("Enter a letter: "))
    if (len(PlayerInput) == 1) and (PlayerInput in string.ascii_letters):
        return PlayerInput
    else:
        print "Please type in one alphabetic character only."
        letter_input()

def P12(count):
    """
    Determines which player is currently active.
    """
    if count % 2 == 0:
        P12 = 2
    else:
        P12 = 1
    return P12

def ghost():
    """
    Main body of the game.
    """
    count = 1
    CurrentFrag = ''
        
    print "Welcome to Ghost!"
    print "Player 1 goes first."
    print "Current word fragment: ''"

    while True:
        inputLetter = string.upper(letter_input())
        CurrentFrag += inputLetter
        string.upper(CurrentFrag)
        if count > 3 and is_word(CurrentFrag, wordlist):
            print "Player %d loses because %s is a word!" % (P12(count), CurrentFrag)
            print "Player %d wins!" % (3 - P12(count))
            break
        if count > 1 and (not can_be_word(CurrentFrag, wordlist)):
            print "Player %d loses because no word begins with %s!" % (P12(count), CurrentFrag)
            print "Player %d wins!" % (3 - P12(count))
            break
        print "Player %d says letter: %s\n" % (P12(count), inputLetter)
        print "Current word fragment: ",CurrentFrag
        count += 1
        print "Player %d's turn." % (P12(count))


if __name__ == '__main__':
    ghost()
    


