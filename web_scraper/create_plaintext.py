""" Takes all of the files generated with Worm_downloader, and removes the text on the front and back, as well
	as removing the stupid '~' I put in in place of non ascii characters.
	Who knew that an apostrophe wasn't an ascii character?
"""

from pickle import dump, load


def fix_tilde(text):
	revised = []
	for char in text:
		if char != '~':
			revised.append(char)
	return "".join(revised)


def strip_non_story(filename):
	chapter = open(filename, 'r+')


	
if __name__ == '__main__':
