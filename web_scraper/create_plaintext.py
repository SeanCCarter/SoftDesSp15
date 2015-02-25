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
	print filename
	chapter = open(filename, 'r+')
	start = chapter.tell()
	text = chapter.readlines()

	#The archives an reand & participate are something that I noticed always occurs
	while 'Category Archives:' or "Last Chapter~~~~~~~~~~~~" not in text[0]:
	 	text = text[1:]

	# line = 0
	# while 'Read & Participate' or 'Last Chapter~~~~~~~~~~~~' not in text[line]:
	# 	line += 1
		
	# text = text[:line]

	for position, line in enumerate(text):
		text[position] = fix_tilde(line)

	chapter.seek(start)
	for line in text:
		chapter.write(line)
	chapter.close


if __name__ == '__main__':
	print 'hi'
	data = open('!Filenames.txt', 'r+')
	filenames = load(data)
	for name in filenames:
		print name
		strip_non_story(name.encode('ascii') + '.txt')
