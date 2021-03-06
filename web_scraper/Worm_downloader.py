"""This is meant to download and save the entire text of Worm as a series of text files, based on chapter."""

from pattern.web import *
from string import printable
from bs4 import BeautifulSoup
from pickle import dump, load

def get_links(url):
	"""Gets all of the links from a webpage. In this case, that would be the table of contents"""
	table_of_contents = URL(url).download()
	unsorted_urls = find_urls(table_of_contents)
	return unsorted_urls


def sort_urls(urls, formats):
	"""Takes a list of URLs, and returns the ones which include any entry from the list of acceptable formats"""
	accepted_urls = []
	for url in urls:
		for option in formats:
			if option in url and not accepted_urls:
				accepted_urls.append(url)
			elif option in url and accepted_urls[-1] != url:
				accepted_urls.append(url)
	return accepted_urls


def print_urls(urls):
	"""Takes a list of urls, and deletes the unprintable characters"""
	revised_urls = []
	for url in urls:
		for position, character in enumerate(url):
			if character not in printable:
				url = url[:position] + '~()~' + url[position+1:]
		revised_urls.append(url)
	for url in revised_urls:
		print url


def create_text_files(urls):
	counter = 0
	filenames = []
	for url in urls:
		page = URL(url).download()
		soup = BeautifulSoup(page)
		texts = soup.get_text()
		text = remove_non_Ascii(texts)
		url = url.split('/')
		filename = remove_non_Ascii(url[-2])
		filenames.append(filename)

		text_file = open('./text_files/'+filename + '.txt', 'w')
		text_file.write(text)
		text_file.close()
		print 'Finished processing: ' + filename
		counter += 1

	list_of_filenames = open('filenames.txt', 'w')
	dump(filenames, list_of_filenames)


def remove_non_Ascii(text): 
	"""	There are serious issues with Worm's use of the 1/2 symbol, that breaks interpreters. This 
		is how I chose to fix it: stripping out anythin that isn't ascii, substituting '~'.
	"""
	revised = []
	for char in text:
		if ord(char)<128:
			revised.append(char)
		else:
			revised.append('~')
	return "".join(revised)

if __name__ == '__main__':
	urls = get_links("https://parahumans.wordpress.com/table-of-contents/")
	formats = ['https://parahumans.wordpress.com/category/stories', 'https://parahumans.wordpress.com/2012/', 'https://parahumans.wordpress.com/2013/']
	urls = sort_urls(urls, formats)
	

	create_text_files(urls)

	#print_urls(urls)

	#This bit is 'cause I messed up the code with pickle, and just wanted the filenames.
	#The reason that the filenames aren't a simple interator is for human readability. I
	#actually know what the filenames mean, and if I want to do something more complicated than
	#this project, I can use the names to help classify the text by the actuall name of the chapter.

	# filenames = []
	# for url in urls:
	# 	url = url.split("/")
	# 	filename = remove_non_Ascii(url[-2])
	# 	filenames.append(filename)
	# all_filenames = open('filenames.txt', 'w')
	# dump(filenames, all_filenames)


