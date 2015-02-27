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
	''' All of the chapters come with extraneous junk, that my download function doesn't quite take care of
		when stripping outu all text. Some of the chapters also have comments, which can interfere with
		the sentiment analysis. This rather ugly looking function will still find all of the standard
		formating things, and strip them out.
	'''
	chapter = open(filename, 'r+')
	text = chapter.readlines()
	chapter.close

	while 'Category Archives:' not in text[0] and "~~~~~~~~~~~~" not in text[0] and '~ ~ ~ ~ ~ ~ ~' not in text[0]:
	 	text = text[1:]

	#Bizzare nature of lines below is because chapter interlude-27b was four words long. I hate formatting.
	#I ran out of time before I could find an elegant way of doing this.
 	line = 1
 	print filename
 	if filename != './text_files/interlude-27b.txt':
		while 'Read & Participate' not in text[line] and '~~~~~~~~~~~~~~'  not in text[line] and '~ ~ ~ ~ ~ ~ ~' not in text[line] or line < 25:
			line += 1
	else:
		while 'Read & Participate' not in text[line] and '~~~~~~~~~~~~~~'  not in text[line] and '~ ~ ~ ~ ~ ~ ~' not in text[line]:
			line += 1

	full_text = text[0:line+1]

	for position, line in enumerate(full_text):
		full_text[position] = fix_tilde(line)

	chapter = open(filename, 'w')
	chapter.write("".join(full_text))
	chapter.close()


if __name__ == '__main__':
	data = open('filenames.txt', 'r+')
	filenames = load(data)
	status = "{0} has been processed as file #{1}"
	counter = 0
	for name in filenames:
		strip_non_story('./text_files/'+ name + '.txt')
		print status.format(name, str(counter))
		counter += 1

