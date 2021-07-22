from termcolor import colored
import colorama
from selenium.webdriver.chrome.options import Options
from os import mkdir

def create_folder(name, folder_count=1):
	try:
		mkdir(name)
	except FileExistsError:
		create_folder(name + f' ({folder_count})', folder_count+1)

def init():
	colorama.init()
	options = Options()
	options.add_argument(r"--user-data-dir=C:\Users\abhi\AppData\Local\Google\Chrome\User Data")
	options.add_argument(r'--profile-directory=Profile 2')
	options.add_argument('log-level=3')
	return options

def log(text, color):
	print(colored(text, color))