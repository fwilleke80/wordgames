# Word Games
Command line games with words

## Hangman
Usage:  
`python hangman.py [lang]`

* "lang" must be the name of one of the .txt files in subfolder "words", e.g. "de" or "en". Default is "de".

A classic hangman game.

You have to solve a word by guessing its letters, while the hangman is drawn, but you only have a certain number of tries until the hangman hangs.

## Wheel of Fortune
Usage:  
`python wheeloffortune.py [lang]`

* "lang" must be the name of one of the .txt files in subfolder "words", e.g. "de" or "en". Default is "de".

An implementation of the classic Wheel of Fortune game.

You have to solve a word by guessing its letters. If you choose to guess a consonant, you can roll the wheel. If you roll money and correctly guess a consonant, you'll get the money for every occurrence of that consonant. If you roll BANKRUPT, you loose all your money.

You can also buy vowels. Buying vowels costs $ 250, regardless of how often the vowel actually ocurrs in the word.

Finally, you can also choose to solve the word (if you already think you know what it is, and want to avoid rolling BANKRUPT).

## Word files
You can add your own word files. They must be plain text (ASCII or UTF-8) files and go into the subfolder "words". Whatever the filename is can be used as "lang" command line parameter.

For example, create a file with French words, save it as "/words/fr.txt" and use it by typing `python hangman.py fr`or `python wheeloffortune.py fr`.

## Credits
Credits and thanks for the word lists go to:

* Josh Kaufman  
https://github.com/first20hours  
For the English word list

* David Kleuker  
https://github.com/davidak
For the German word list