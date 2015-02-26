from pattern.en import *
from pickle import dump, load

def  analize_chapter(filename, averager):
	""" Takes in the filename for a chapter, and then outputs
		the average of the n most positive and n most negative
		sentence.
	"""
	chapter = open(filename, 'r')
	lines = chapter.readlines()
	chapter.close()
	text = " ".join(lines)
	text = text.split(".")

	sentiments = []

	for line in text:
		sentiments.append(sentiment(line)[0])

	sentiments.sort()
	if len(sentiments) >= 2*averager:
		negative = sum(sentiments[0:averager])/averager
		positive = sum(sentiments[len(sentiments)-averager:])/averager
		return (positive, negative)
	else:
		return (max(sentiments), min(sentiments))


if __name__ == '__main__':

	data = open('!Filenames.txt', 'r+')
	filenames = load(data)

	sentiments = []
	for name in filenames:
		print name
		sentiments.append(analize_chapter(name+'.txt', 30))
		print sentiments[-1]

	data = open("Sentiments_2.txt", 'w')
	dump(sentiments, data)