import re
import collections
from shutil import copyfile
from pathlib import Path
from fileDownload import download
from termcolor import colored

project_name = None

def find_fonts(data):
	with open("global_variables.txt", "r+") as file:
		project_name = file.read()
	# Finding font urls in the data
	font_start_positions = [m.start() for m in re.finditer('webfont', data)]
	font_end_positions = [m.start() for m in re.finditer('.woff2', data)]

	# Slicing Font file name from url
	fonts = []
	for start_position, end_position in zip(font_start_positions, font_end_positions):
		fonts.append(data[start_position+10:end_position])

	# Removing the last font (because it belongs to figma)
	fonts.pop()

	# Remove all the italic fonts
	fonts = [font for font in fonts if 'Italic' not in font]

	# Find the Font Family
	words = '-'.join(fonts).split('-')
	word_counts = collections.Counter(words)
	highest_count, highest_count_word = 0, None
	for word, count in sorted(word_counts.items()):
		if count > highest_count:
			highest_count, highest_count_word = count, word

	print(colored('Font Family:', 'green'), colored(highest_count_word, 'green'))

	# Take a shortcut if font is inter
	if highest_count_word == 'Inter':
		Path(project_name + '/fonts/').mkdir(parents=True, exist_ok=True)
		copyfile('Data/common/fonts/Inter.ttf', project_name + '/fonts/Inter.ttf')
	else:
    	# Download the fonts
		download('https://fonts.google.com/download?family=' + highest_count_word)
	return fonts