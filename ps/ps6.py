# Problem Set 5: 6.00 Word Game
# Name: 
# Collaborators: 
# Time: 
#

import random
import string
import copy
import time

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
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
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
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------
def get_words_to_points(word_list):
    """
        Return a dict that maps every word
        in word_list to its point value.
    """
    points_dict = {}
    for word in word_list:
        points_dict[word] = 0
        for i in word:
            points_dict[word] += SCRABBLE_LETTER_VALUES[i]
    return points_dict

def sort_list(wordtemp):
    for i in range(0, len(wordtemp)-1):
        MinId = i
        MinVal = wordtemp[i]
        for j in range(i+1, len(wordtemp)):
            if wordtemp[j] < MinVal:
                MinId = j
                MinVal = wordtemp[j]
        temp = wordtemp[i]
        wordtemp[i] = wordtemp[MinId]
        wordtemp[MinId] = temp
    return wordtemp

def get_word_rearrangements(word_list):
    rearr = {}
    for word in word_list:
        wordtemp = []
        for letter in word:
            wordtemp.append(letter)
        wordtemp = sort_list(wordtemp)
        wordsorted = ''
        for i in range(0,len(wordtemp)):
            wordsorted += wordtemp[i]
        rearr[wordsorted] = word
    return rearr

#
# Problem #1: Scoring a word
#
def get_word_score(word, n , total_time):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO ...
    scores = 0
    time = total_time
    for letter in word:
        scores += SCRABBLE_LETTER_VALUES[letter]
    if len(word) == n:
        scores += 50
    if time >= 1.0:
        scores = scores / time * 100
    else:
        scores = scores * (2 - time) * 100
    return scores
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
    displayed = []
    for letter in hand.keys():
        for j in range(hand[letter]):
            displayed.append(letter),
            print letter,               # print all on the same line
    #print                              # print an empty line
    return ' '

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # TO DO ...
    for letter in word:
        for key in hand.keys():
            if letter == key:
                hand[key] -= 1
    for key in hand.keys():
        if hand[key] == 0:
            del hand[key]
    return hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, POINTS_DICT):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # TO DO ..
    handtemp = copy.deepcopy(hand)
    flag1 = True
    flag2 = True
    # Check if every letter in the word is also in the hand.
    for letter in word:
        try:
            handtemp[letter]
        except KeyError:
            flag1 = False
            break
        handtemp[letter] -= 1
    # Check the numbers a letter used.
    for key in handtemp.keys():
        if handtemp[key] < 0:
            flag1 = False
            break 
    # Check the word is in the wordlist.
    try:
        POINTS_DICT[word]
    except KeyError:
        flag2 = False
    
    if flag1 and flag2:
        return True
    else:
        return False

def get_time_limit(POINTS_DICT, k):
    """
    Return the time limit for the computer player as a function of the
    multiplier k.
    points_dict should be the same dictionary that is created by
    get_words_to_points.
    """
    start_time = time.time()
    # Do some computation. The only purpose of the computation is so we can
    # figure out how long your computer takes to perform a known task.
    for word in POINTS_DICT:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE, 1)
    end_time = time.time()
    return (end_time - start_time) * k

def TimeLimit():
    #computer play
    time_limit = get_time_limit(POINTS_DICT, 1)
    return time_limit
    #Man play
##    while True:
##        try:
##            time_limit = float(raw_input("Enter time limit in seconds for players: "))
##            break
##        except:
##            print "Invalid input."
##    if time_limit > 0:
##        return time_limit
##    else:
##        print "Input number must be larger than 0."
##        TimeLimit()

def pick_best_word(hand, POINTS_DICT):
    """ Return the highest scoring word from points_dict
        that can be made with the given hand.
        Return '.' if no words can be made with the given hand.
    """
    #Sum points in hand
    SumPtsInHand = 0
    for key in hand.keys():
        SumPtsInHand += SCRABBLE_LETTER_VALUES[key] * hand[key]
    #create a list with all words which value has no more points in hand.
    OptionalWords = []
    for key in POINTS_DICT.keys():
        if POINTS_DICT[key] <= SumPtsInHand:
            OptionalWords.append(key)
    #Check if words in the list can be formed from letter in hand.
    #if can, add them to a new list.
    WordsUCanUse = []
    for word in OptionalWords:
        handtemp = copy.deepcopy(hand)
        flag = True
        for letter in word:
            try:
                handtemp[letter]
            except KeyError:
                flag = False
                break
            handtemp[letter] -= 1
        for key in handtemp.keys():
            if handtemp[key] < 0:
                flag = False
                break
        if flag:
            WordsUCanUse.append(word)
    if WordsUCanUse == []:
        return '.'
    #find the word with the most scores.
    bestWord = WordsUCanUse[0]
    for word in WordsUCanUse:
        if POINTS_DICT[word] > POINTS_DICT[bestWord]:
            bestWord = word
    return bestWord

def subset(fromlist,tolist):
    """
    Find all subsets of a list.
    """
    n = len(fromlist)
    for i in range(1, 2**n):
        bi = bin(i)
        templist = []
        for j in range(-len(bi)+2, 0):
            if bi[j] == '1':
                templist.append(fromlist[j])
        tolist.append(templist)
    return tolist
                
def pick_best_word_faster(hand, rearrange_dict, POINTS_DICT):
    letterlist = []
    WordsCanUse = []
    for letter in hand.keys():
        for i in range(0,hand[letter]):
            letterlist.append(letter)
    letterlist = sort_list(letterlist)
    templist = subset(letterlist, [])
    for combi in templist:
        temp = ''
        for i in combi:
            temp += i
        try:
            rearrange_dict[temp]
        except KeyError:
            continue
        WordsCanUse.append(temp)
    if WordsCanUse == []:
        return '.'
    bestWord = rearrange_dict[WordsCanUse[0]]
    for word in WordsCanUse:
        if POINTS_DICT[rearrange_dict[word]] > POINTS_DICT[bestWord]:
            bestWord = rearrange_dict[word]
    return bestWord
   
#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    # TO DO ...
    def InputWord():
        print "Enter word, or a . to indicate that you are finished: ",
        start_time = time.time()
        #Input = str(raw_input()) #Man play.
        #Input = pick_best_word(CurrentHand, POINTS_DICT) #Computer play.
        Input = pick_best_word_faster(CurrentHand, rearrange_dict, POINTS_DICT) #Computer fast play.
        end_time = time.time()
        total_time = end_time - start_time
        print '\n',Input
        return Input, total_time

    def displayCurrentHand():
        print "Current Hand: ",display_hand(CurrentHand)
        return ' '

    CurrentHand = hand
    ScoreLast = 0
    ScoreTotal = 0
    Word = ' '
    time_limit = TimeLimit()
    
    while True:
        displayCurrentHand()
        Word, total_time = InputWord()
        time_limit = time_limit - total_time
        if (not is_valid_word(Word, CurrentHand, POINTS_DICT)) and Word != '.':
            print "Invalid word, please try again. %.2f seconds wasted." % total_time
            if time_limit < 0:
                print 'Total time exceed %.2f seconds.' % abs(time_limit)
                break
            continue
        elif Word == '.':
            break
        print 'It took %.2f seconds to provide an answer.' % total_time
        if time_limit < 0:
            print 'Total time exceed %.1f seconds.' % abs(time_limit)
            break
        print 'You have %.2f seconds remaining.' % time_limit
        ScoreLast = int(get_word_score(Word, HAND_SIZE, total_time))
        ScoreTotal += ScoreLast
        print "%s earned %d points. Total: %d points." % (Word, ScoreLast, ScoreTotal)
        CurrentHand = update_hand(CurrentHand, Word)
        # if all letters are used
        if CurrentHand == {}:
            break
        Word = ' '
    print "Total Score: %d points." % ScoreTotal


#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO ...
    ## uncomment the following block of code once you've completed Problem #4
    hand = deal_hand(HAND_SIZE) # random init
    while True:
        cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'r':
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'e':
            break
        else:
            print "Invalid command."


# Build data structures used for entire session and play game

if __name__ == '__main__':
    word_list = load_words()
    POINTS_DICT = get_words_to_points(word_list)
    rearrange_dict = get_word_rearrangements(word_list)
    play_game(word_list)
