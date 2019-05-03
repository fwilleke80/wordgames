#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from wordgamelib import wordgamelib as gamelib

HANGMANGFX = [
    """








----------
""",
    """

|
|
|
|
|
|
|
+---------
""",
    """
+-------
|
|
|
|
|
|
|
+---------
""",
    """
+-------
|      |
|      |
|
|
|
|
|
+---------
""",
    """
+-------
|      |
|      |
|      @
|
|
|
|
+---------
""",
    """
+-------
|      |
|      |
|      @
|      |
|
|
|
+---------
""",
    """
+-------
|      |
|      |
|      @
|      |
|     /
|
|
+---------
""",
    """
+-------
|      |
|      |
|      @
|      |
|     / \\
|
|
+---------
""",
    """
+-------
|      |
|      |
|      @
|     /|
|     / \\
|
|
+---------
""",
    """
+-------
|      |
|      |
|      @
|     /|\\
|     / \\
|
|
+---------
"""]

FAILLIMIT = len(HANGMANGFX) - 1


def parse_args(args):
    if len(args) == 0:
        return 'de'
    else:
        return args[0].lower()


def default_gamestate(theWord, langCode):
    return {
        'solved': False,
        'lost': False,
        'theWord': theWord,
        'display': ['_'] * len(theWord),
        'alreadyChecked': set(),
        'wrong': set(),
        'lastResult': '',
        'letter': '',
        'guessRound': 1,
        'langCode': langCode
    }


def draw_gamestate(gamestate):
    print('Hangman / Galgenraten 1.0 (' + gamestate['langCode'] + ')')
    print('==============================')
    print('')
    if gamestate['lost']:
        print(HANGMANGFX[len(HANGMANGFX) - 1])
    else:
        print(HANGMANGFX[len(gamestate['wrong'])])
    print('')
    print('This is guess no. ' + str(gamestate['guessRound']) + '.')
    print('You had ' + ('no' if len(gamestate['wrong']) == 0 else (
        str(len(gamestate['wrong'])) + '/' + str(FAILLIMIT))) + ' misses so far.')
    if gamestate['letter'] != '':
        print('Your last guess was "' + gamestate['letter'] +
              '" and it was ' + gamestate['lastResult'] + '.')
    print('')
    wordDisplay(gamestate['display'])


def draw_game_results(gamestate):
    if gamestate['solved']:
        # Won!
        print('Yeah, you won! The word is "' + gamestate['theWord'] + '"!')
        print('You took ' + str(gamestate['guessRound']) +
              ' guesses, including ' + str(len(gamestate['wrong'])) + ' fails (failrate: ' + "{0:2f}".format(float(gamestate['wrong']) / float(gamestate['guessRound'])) + '))!')
    elif gamestate['lost']:
        # Lost!
        print('Oops, you screwed up!')
        print('The word was "' + gamestate['theWord'] + '", by the way.')


def draw_stats(words, langCode):
    numWords = len(words)
    wordLen = 0
    for word in words:
        wordLen += len(word)
    wordLen /= float(numWords)
    print('Dictionary lang.: ' + langCode)
    print('Number of words : ' + str(numWords))
    print('Avg. word length: ' + '{0:2f}'.format(wordLen))


def ask_player_for_letter():
    return unicode(str(raw_input('Guess your letter: ')).decode('utf-8'))[0].upper()


def wordDisplay(s):
    d = ''
    for c in s:
        d = d + c + ' '
    print(d)


def main():
    # Handle args
    args = sys.argv[1:]
    langCode = parse_args(args)

    # Load words list
    words = gamelib.read_text_file('words/' + langCode + '.txt')
    if words is None or len(words) == 0:
        sys.exit('No words loaded.')

    # Draw statistics
    if len(args) > 1 and args[1].lower() == 'stats':
        draw_stats(words, langCode)
        sys.exit()

    # Play game until user has enough
    go_on = True
    while go_on:
        # Prepare a new game
        gamestate = default_gamestate(
            gamelib.get_random_word(words).upper(), langCode)

        # Round after round until game is lost or won
        while not gamestate['solved'] and not gamestate['lost']:
            # Display game state
            gamelib.clear_screen()
            draw_gamestate(gamestate)

            # Ask user for letter
            print('')
            gamestate['letter'] = ask_player_for_letter()

            # Check input
            if gamestate['letter'] in gamestate['alreadyChecked']:
                # Letter has been tried before
                gamestate['lastResult'] = 'something you had guessed before'
            elif gamestate['letter'] in gamestate['theWord']:
                # Letter is in word
                gamestate['lastResult'] = 'correct'
                for i in range(len(gamestate['theWord'])):
                    if gamestate['letter'] == gamestate['theWord'][i]:
                        gamestate['display'][i] = gamestate['letter']
            else:
                # Letter is not in word
                gamestate['lastResult'] = 'wrong'
                gamestate['wrong'].add(gamestate['letter'])
            gamestate['alreadyChecked'].add(gamestate['letter'])

            # Check for win
            if gamestate['theWord'] == ''.join(gamestate['display']):
                # Won!
                gamestate['solved'] = True
            elif len(gamestate['wrong']) >= FAILLIMIT:
                # Lost!
                gamestate['lost'] = True
            else:
                gamestate['guessRound'] += 1

        # Display game state
        gamelib.clear_screen()
        draw_gamestate(gamestate)
        print('')
        draw_game_results(gamestate)

        # Does player want to play another game?
        go_on = str(
            raw_input('\nDo you want to try your luck one more time? [Y/N] ')).upper() == 'Y'


if __name__ == '__main__':
    try:
        print('')
        main()
        print('')
    except KeyboardInterrupt:
        print('Cancelled')
