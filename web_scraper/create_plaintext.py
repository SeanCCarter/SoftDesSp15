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
	text = chapter.readlines()
	chapter.close

	while 'Category Archives:' not in text[0] and "Last Chapter~~~~~~~~~~~~" not in text[0] and 'Last Chapter~ ~ ~ ~ ~ ~' not in text[0]:
	 	text = text[1:]

 	line = 1
	while 'Read & Participate' not in text[line] and '~~~~~~~~~~~~~~~~~~'  not in text[line] and '~ ~ ~ ~ ~ ~ ~ ~ ~ ~' not in text[line]:
		line += 1

	full_text = text[0:line+1]

	for position, line in enumerate(full_text):
		full_text[position] = fix_tilde(line)

	chapter = open(filename, 'w')
	chapter.write("".join(full_text))
	chapter.close()


if __name__ == '__main__':
	data = open('!Filenames.txt', 'r+')
	filenames = load(data)
	#strip_non_story(filenames[0] + '.txt')
	for name in filenames:
		print name
		strip_non_story(name + '.txt')

