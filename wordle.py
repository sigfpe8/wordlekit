"""
	This script has two interactive functions:

	* play() -> plays a Wordle clone in character mode

	* solve() -> given your guesses in encoded format, suggest words that may help you solve a Wordle puzzle

	Convention to encode letter colors in words:
	  Green  -> uppercase (letter in correct position)
	  Yellow -> ?anycase (letter in wrong position)
	  Black  -> lowercase (letter not in word)

	Example: Ar?os?e (A->green, rs->black, oe->yellow)
	
	Global variables
	   green  -> string with green letters so far (e.g. "A____")
	   yellow -> dictionary with positions where key appeared as yellow (e.g. {'O' : [2], 'E' : [4]})
	   black  -> string of black letters so far (e.g. 'RS')
"""

import time
import random

green = 5*' '
yellow = {}
black = ''
word_list = []

def get_guess():
	"""Enter a guess word (called by play())."""
	while True:
		guess = input("Your guess: ")
		gl = len(guess)
		if (gl == 0) or (gl == 5 and guess.isalpha()):
			break
		print("Guess word must have 5 letters")
	return guess.upper()

def get_encoded_guess():
	"""Enter a guess word in encoded format (called by solve())."""
	while True:
		guess = input("Your encoded guess: ")
		if len(guess) == 0:
			break
		nguess = guess.replace('?','')
		if len(nguess) == 5 and nguess.isalpha():
			break
		print("Guess word must have 5 letters")
	return guess

def update_colors(guess):
	global black, green, yellow
	pi = 0
	# pi = "physical" index (0 to len(guess)-1)
	# li = "logical" index (0 to 4)
	for li in range(5):
		l = guess[pi]
		if l.isupper():	# Green
			if green[li] != l:
				green = green[:li]+l+green[li+1:]
		elif l.islower(): # Black
			l = l.upper()
			if l not in black and l not in green and l not in yellow:
				black = black + l
		else:	# Must be ?letter (Yellow)
			pi += 1
			l = guess[pi].upper()
			if l not in yellow:
				yellow[l] = [li]
			else:
				yellow[l].append(li)

		pi += 1

def valid_green(w):
	"""Return True if all green characters are in the same position in the word."""
	for i in range(5):
		if green[i] != ' ' and green[i] != w[i]:
			return False
	return True

def valid_black(w):
	"""Return True if word contains no black letter."""
	for b in black:
		if b in w:
			return False
	return True

def valid_yellow(w):
	"""Return True if word contains all yellow letters but in different positions."""
	for y in yellow:
		if y not in w:
			return False
		# x = list of positions where letter y appeared as yellow
		x = yellow[y]
		for li in range(5):
			if w[li] == y and li in x:
				return False

	return True

def update_words(words):
	new_words = []
	for w in words:
		if valid_green(w) and valid_black(w) and valid_yellow(w):
			new_words.append(w)
	return new_words

def read_word_list(fname):
	wfile = open(fname, "r")

	for line in wfile:
		if len(line) == 6:	# 5 letters + newline
			word_list.append(line[:5].upper())

	wfile.close()

def colorize_word(word, spaces=False):
	"""Given an encoded word, print it with corresponding colors."""
	sgr_normal = "\033[0m"
	# Normal colors
	#white_fg = "\033[37m"
	#black_bg = "\033[40m"
	#green_bg  = "\033[42m"
	#yellow_bg  = "\033[43m"
	# Bright colors
	white_fg = "\033[97m"
	black_bg = "\033[100m"
	green_bg  = "\033[102m"
	yellow_bg  = "\033[103m"
	ansi_str = sgr_normal + white_fg + "     "
	sgr = sgr_normal
	pi = 0
	# pi = "physical" index (0 to len(word)-1)
	# li = "logical" index (0 to 4)
	for li in range(5):
		l = word[pi]
		if l.isupper():	# Green
			if sgr != green_bg:
				ansi_str = ansi_str + green_bg
				sgr = green_bg
		elif l.islower(): # Black
			if sgr != black_bg:
				ansi_str = ansi_str + black_bg
				sgr = black_bg
			l = l.upper()
		else:	# Must be ?letter (Yellow)
			pi += 1
			l = word[pi].upper()
			if sgr != yellow_bg:
				ansi_str = ansi_str + yellow_bg
				sgr = yellow_bg

		pi += 1
		ansi_str = ansi_str + l
	
		if spaces:	# Add a space after each letter
			ansi_str = ansi_str + sgr_normal + white_fg + " "
			sgr = sgr_normal

	print(ansi_str + sgr_normal)

def encode_word(word,guess):
	"""
	Given a plain-text guess word, compare it to the secret
	word and return the encoded (colorized) version of the guess.
	"""
	new = ''

	for i in range(5):
		l = guess[i]
		if not l in word:		# Black = lowercase
			new += l.lower()
		elif word[i] == l:		# Green = uppercase
			new += l
		else:
			new += '?'+l		# Yellow = ?anycase

	return new

def guess(word):
	guess = ''
	my_words = []

	while guess != word and len(my_words) < 6:
		guess = get_guess()
		if guess == '':
			break
		if guess in word_list:
			my_words.append(encode_word(word,guess))
		else:
			print("This word is not in the dictionary")

		for w in my_words:
			colorize_word(w)

	if guess == word:
		print("Congratulations, you found the word!")
	else:
		print("\nThe secret word was", word)

def solve():
	"""
	Interactive function to help find a Wordle word.

	Enter the encoded version of Wordle's response to your guess
	   Green letters  -> uppercase
	   Yellow letters -> ?anycase (e.g. ?e or ?E)
	   Black letters  -> lowercase
	"""
	global black, green, yellow
	green = 5*' '
	yellow = {}
	black = ''

	if word_list == []:
		read_word_list("wordlist.txt")

	words = word_list
	my_words = []

	while ' ' in green:
		nwords = len(words)
		if nwords <= 20:
			if nwords == 0:
				print("I'm out of words!")
				break
			print("Possible words:", words)
		else:
			print(nwords, "possible words")

		guess = get_encoded_guess()

		if guess == '':
			print("I give up!")
			break

		my_words.append(guess)
		update_colors(guess)
		#print("g=",green,"y=",yellow,"b=",black)
		words = update_words(words)
		for w in my_words:
			colorize_word(w)

	
	if not ' ' in green:
		print("The word is", green)

def play():
	"""Interactive function to play Wordle in character mode."""
	if word_list == []:
		read_word_list("wordlist.txt")

	while True:
		# Select a random word from the dictionary
		print("\nLet me think of a 5-letter word...")
		word = word_list[random.randrange(len(word_list))]
		time.sleep(2)
		# Guess it
		print("Ok, try to guess it!\n")
		guess(word)
		# More fun?
		yesno = input("Play another game? [Y/n] ")
		if len(yesno) > 0 and yesno.upper()[0] == 'N':
			break

if __name__ == '__main__':
	play()
