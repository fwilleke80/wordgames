#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import random
from wordgamelib import wordgamelib as gamelib

DEBUGMODE = True

ROLLPHASES = 20
ROLLDELAY = 0.5
VOWEL_COST = 250

# Fields on the wheel
# Based on US Wheel of Fortune, syndicated 33rd season's version (2015-2016)
# Missing are fields that only make sense with multiple players.
WHEEL = [
    2500,
    600,
    700,
    600,
    650,
    500,
    700,
    'B',
    600,
    550,
    500,
    600,
    'B',
    650,
    700,
    800,
    500,
    650,
    500,
    900,
    'B'
]


def parse_args(args):
    if len(args) == 0:
        return 'de'
    else:
        return args[0].lower()


def default_gamestate(theWord, langCode):
    return {
        'solved': False,
        'theWord': theWord,
        'display': ['_'] * len(theWord),
        'langCode': langCode,
        'balance': 0,
        'wheel': 0
    }


def draw_gamestate(gamestate):
    print('Wheel of Fortune / Glücksrad 1.0 (' + gamestate['langCode'] + ')')
    print('=====================================')
    print('')
    if DEBUGMODE:
        print('DEBUG: ' + gamestate['theWord'])
        print('')
    wheelDisplay(gamestate['wheel'])
    print('')
    wordDisplay(gamestate['display'])
    print('')
    balanceDisplay(gamestate['balance'])


def indent(s):
    if len(s) < 6:
        return s + ' '
    return s


def wordDisplay(s):
    d = ''
    for c in s:
        d = d + c + ' '
    print(d)


def get_wheel_label(wheelPos, short=0):
    wheelValue = WHEEL[wheelPos]
    if type(wheelValue) == int:
        return '$ ' + str(wheelValue)
    elif type(wheelValue) == str:
        if wheelValue == 'B':
            if short == 1:
                return 'RUPT!'
            elif short == 2:
                return 'BANKR'
            else:
                return 'BANKRUPT'
    return ''


def wheelDisplay(wheelPos):
    wheelPos = wheelPos % len(WHEEL)
    prevWheelPos = (wheelPos - 1) % len(WHEEL)
    nextWheelPos = (wheelPos + 1) % len(WHEEL)

    label = get_wheel_label(wheelPos)
    prevLabel = get_wheel_label(prevWheelPos, short=1)
    nextLabel = get_wheel_label(nextWheelPos, short=2)

    print('W H E E L  of  F O R T U N E')
    print('+--------+--------+--------+')
    print('|        |        |        |')
    if label != 'BANKRUPT':
        print('| ' + indent(prevLabel) + ' | ' +
              indent(label) + ' | ' + indent(nextLabel) + ' |')
    else:
        print('|     B A N K R U P T !    |')
    print('|        |        |        |')
    print('+--------+--------+--------+')


def balanceDisplay(balance):
    print('$ ' + str(balance))


def check_consonant_winnings(price, consonant, word):
    found = 0
    for c in word:
        if c.upper() == consonant.upper():
            found += 1
    return price * found


def update_display(gamestate, letter):
    theWord = gamestate['theWord']
    letter = letter.upper()
    for i in range(len(theWord)):
        if letter == theWord[i].upper():
            gamestate['display'][i] = letter


def main():
    # Handle args
    args = sys.argv[1:]
    langCode = parse_args(args)

    # Load words list
    words = gamelib.read_text_file('words/' + langCode + '.txt')
    if words is None or len(words) == 0:
        sys.exit('No words loaded.')

    # Play game until user has enough
    go_on = True
    while go_on:
        # Prepare a new game
        gamestate = default_gamestate(
            gamelib.get_random_word(words).upper(), langCode)

        # Round after round until game is lost or won
        while not gamestate['solved']:
            # Display game state
            gamelib.clear_screen()
            draw_gamestate(gamestate)

            # Ask player what to do
            if gamestate['balance'] < VOWEL_COST:
                promptStr = 'Do you want to guess a consonant (1) or solve (3)?'
                promptChoices = ['1', '3', 'q']
            else:
                promptStr = 'Do you want to guess a consonant (1), buy a vowel (2), or solve (3)?'
                promptChoices = ['1', '2', '3', 'q']

            userAction = ''
            while userAction not in promptChoices:
                userAction = str(raw_input('\n' + promptStr +
                                           ' ' + str(promptChoices) + ' '))

            # Player spins the wheel
            if userAction == '1':
                # Ask player to spin the wheel of fortune
                _ = raw_input('\nPress ENTER to spin the wheel!')

                # Spin the wheel, animate
                random.seed(time.time())
                currentRollPhases = int(ROLLPHASES * random.uniform(0.5, 1.0))
                rollDelay = ROLLDELAY / currentRollPhases
                for _ in range(currentRollPhases):
                    gamestate['wheel'] = (gamestate['wheel'] + 1) % len(WHEEL)
                    time.sleep(rollDelay)
                    gamelib.clear_screen()
                    draw_gamestate(gamestate)
                    rollDelay += ROLLDELAY / currentRollPhases

                # Rolled money
                if WHEEL[gamestate['wheel']] != 'B':
                    # How much money is there to win?
                    rollValue = WHEEL[gamestate['wheel']]

                    # User chooses consonant
                    userConsonant = ''
                    while userConsonant == '' or userConsonant not in gamelib.CONSONANTS:
                        userConsonant = str(
                            raw_input('\nChoose a consonant for $ ' + str(rollValue) + ': ')).upper()

                    # Check how much the user has won
                    price = check_consonant_winnings(
                        rollValue, userConsonant, gamestate['theWord'])
                    gamestate['balance'] += price

                    # Adjust display to show the new consonants
                    update_display(gamestate, userConsonant)

                    # Display results
                    gamelib.clear_screen()
                    draw_gamestate(gamestate)

                # Rolled bankruptcy!
                else:
                    # Take player's money
                    gamestate['balance'] = 0

                    # Display results
                    gamelib.clear_screen()
                    draw_gamestate(gamestate)

            # Player buys a vowel
            elif userAction == '2':
                # Ask player for vowel
                userVowel = ''
                while userVowel == '' or userVowel not in gamelib.VOWELS:
                    userVowel = str(raw_input(
                        'Buying a vowel costs $' + str(VOWEL_COST) + '. Select a vowel: ')).upper()

                # Buy a vowel
                gamestate['balance'] = max(
                    gamestate['balance'] - VOWEL_COST, 0)

                # Adjust display to show the new vowels
                update_display(gamestate, userVowel)

                # Display results
                gamelib.clear_screen()
                draw_gamestate(gamestate)

            # Player want to solve
            elif userAction == '3':
                # Ask player for complete word
                userWord = ''
                while userWord == '':
                    userWord = str(raw_input('Solve by typing the word: ')).upper()

                # Check if word is correct
                if userWord == gamestate['theWord']:
                    # Solve word
                    gamestate['display'] = list(userWord)

                # Display results
                gamelib.clear_screen()
                draw_gamestate(gamestate)

            # Player wants to quit
            elif userAction.upper() == 'Q':
                sys.exit('Hey, where are you going??')

            # Check if game has been solved
            if not '_' in gamestate['display']:
                gamestate['solved'] = True

                # Display final game state
                gamelib.clear_screen()
                draw_gamestate(gamestate)

                print('\nCongratulations, you have solved the game!')
                print('You take $ ' + str(gamestate['balance']) + ' home with you!!')
                if userAction == '3' and gamestate['balance'] == 0:
                    print('\nTo be honest, solving the word without having any money was kind of a stupid move.')

        # Does player want to play another game?
        go_on = str(raw_input(
            '\nDo you want to try your luck one more time? [Y/N] ')).upper() == 'Y'


if __name__ == '__main__':
    try:
        print('')
        main()
        print('')
    except KeyboardInterrupt:
        print('Cancelled')
