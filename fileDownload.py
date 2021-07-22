import urllib.request as urllib2
import zipfile
from os import listdir, remove, mkdir, rename
from os.path import isfile, join
from termcolor import colored
from shutil import rmtree

project_name = None

def download(url):
	with open("global_variables.txt", "r+") as file:
		project_name = file.read()

	file_name = url.split('=')[-1] + '.zip'
	file_download = urllib2.urlopen(url)
	with open(file_name, 'wb') as file:
		file.write(file_download.read())
	extract(file_name, project_name)
	if "Variable" in' '.join(get_files(project_name + '/temp-fonts/')):
		print(colored('Downloaded Variable Font', 'cyan'))
	keep_only_font(project_name)

def extract(zip_name, file_name):
	destination_directory = str(file_name) + '/temp-fonts'
	with zipfile.ZipFile(zip_name, 'r') as zip_ref:
		zip_ref.extractall(destination_directory)

	try:
		remove(zip_name)
	except OSError:
		print(colored('Unable to find a ZIP font file', 'red'))

def get_files(mypath):
	return [f for f in listdir(mypath) if isfile(join(mypath, f))]

def keep_only_font(main_folder_name):
	font_folder = get_files(main_folder_name + '/temp-fonts')
	mkdir(main_folder_name + '/fonts')
	font_folder = [font for font in font_folder if font.endswith('.ttf')]
	old_path = main_folder_name + '/temp-fonts/' + font_folder[0]
	new_path = main_folder_name + '/fonts/' + font_folder[0].split('-Variable')[0] + '.ttf'
	rename(old_path, new_path)
	rmtree(main_folder_name + '/temp-fonts')
