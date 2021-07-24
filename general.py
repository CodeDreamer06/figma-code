from termcolor import colored
import colorama
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import mkdir
from shutil import rmtree

def create_folder(name, folder_count=1):
	try:
		mkdir(name)
	except FileExistsError:
		# Remove the folder instead of naming it as (2)
		rmtree(name)
		create_folder(name)
		# create_folder(name + f' ({folder_count})', folder_count+1)

def init():
	colorama.init()
	options = Options()
	options.add_argument(r"--user-data-dir=C:\Users\abhi\AppData\Local\Google\Chrome\User Data")
	options.add_argument(r'--profile-directory=Profile 2')
	options.add_argument('log-level=3')
	return options

def log(text, color):
	print(colored(text, color))

def wait(driver):
	element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pages_panel--pagesPanelContent--2qjss")))