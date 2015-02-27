from pattern.en import *
from pickle import dump, load

def  analize_chapter(filename, averager):
	""" Takes in the filename for a chapter, and then outputs
		the average of the n most positive and n most negative
		sentence.
	"""
	#Split the chapter into sentances, instead of lines
	chapter = open(filename, 'r')
	lines = chapter.readlines()
	chapter.close()
	text = " ".join(lines)
	text = text.split(".")

	#Creates a rating from -1 to +1 for how happy the sentance is
	sentiments = []
	for sentance in text:
		sentiments.append(sentiment(sentance)[0])

	#Picks out and averages the n most positive and n most negatives sentances,
	#to get a feel for how emotionally charged a chapter was.
	sentiments.sort()
	if len(sentiments) >= 2*averager:
		negative = sum(sentiments[0:averager])/averager
		positive = sum(sentiments[len(sentiments)-averager:])/averager
		return (positive, negative)
	else:
		return (max(sentiments), min(sentiments))


if __name__ == '__main__':

	data = open('filenames.txt', 'r+')
	filenames = load(data)

	sentiments = []
	for name in filenames:
		sentiments.append(analize_chapter('./text_files/'+name+'.txt', 30))

	data = open("Sentiments.txt", 'w')
	dump(sentiments, data)