If you are a Wordle fan as I am, you can use this simple Python script in two ways.

First, in *play mode* it can be used to play a character-based Wordle clone. The user interface is minimal and at this point statistics are not being collected. It uses a word list of about 3200 words which, unfortunately, contains some plurals and verb conjugations that are not nice to appear in this kind of game.

![Play mode]()

Second, there is a *help mode* that can be useful when you're playing the real Wordle and feel you need some additional help. While in the *play mode* you enter your guess as regular text, in the *help mode* you enter an encoded version of the colored Wordle response. The script starts with the full word list and after each guess it removes the words that don't match the colored letters revealed by Wordle. During the initial guesses it just tells you the lenght of the list. When the list contains less than 20 words, all the words are revealed so that you can make a better choice the next time.

To colorize the letters in Wordle style the script uses standard ANSI escape sequences. It was tested only on macOS with the native Terminal app, but should work with any terminal emulator that supports ANSI sequences.
