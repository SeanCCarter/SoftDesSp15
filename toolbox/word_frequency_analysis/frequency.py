""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	#Following code taken from the website: it removes the headers from project gutenburg ebooks
	#It also deals with non-gutenburg text files, like Worm, which I plan to use.
	f = open(file_name,'r')
	lines = f.readlines()
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1 and curr_line != len(lines) -1:
		curr_line += 1
	if curr_line+1 < len(lines):
		lines = lines[curr_line+1:]

	#Takes the full text, then splits it into words.
	text = remove_non_Ascii(''.join(lines))
	for char in string.punctuation:
		text.strip(char)
	text = text.lower()
	text = text.split()
	return text


def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""
	word_counter = {}
	for word in word_list:
		if word in word_counter:
			word_counter[word] += 1
		else:
			word_counter[word] = 1
	ordered_by_frequency = sorted(word_counter, key=word_counter.get, reverse=True)
	return ordered_by_frequency[0:n+1]


def remove_non_Ascii(text): 
	"""	There are serious issues with Worm's use of the 1/2 symbol, that breaks interpreters. This 
		is how I chose to fix it: stripping out anythin that isn't ascii, substituting '~'.
	"""
	revised = []
	for char in text:
		if ord(char)<128:
			revised.append(char)
	return "".join(revised)


if __name__ == '__main__':
	wordlist = get_word_list("Worm Book.txt")
	for i, word in enumerate(get_top_n_words(wordlist, 100)):
		print '#' + str(i) + ' ' + word
