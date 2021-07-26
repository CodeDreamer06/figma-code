from termcolor import colored
import colorama
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import mkdir
from shutil import rmtree

def find_variables(driver):
	text_styles, color_keys, unknown = [], [], []
	for element in driver.find_elements_by_css_selector('p.styles--name--RhNAx'):
		if 'color' in element.text:
			color_keys.append(element.text)
		elif 'text' in element.text:
			text_styles.append(element.text)
		else:
			unknown.append(element.text)

	log('Found ' + str(len(color_keys)) + ' Colors', 'green')
	log('Found ' + str(len(text_styles)) + ' Text Styles', 'green')
	if unknown:
		print('Unkown variables: ', unknown)

	color_values = []
	for element in driver.find_elements_by_css_selector("div.style_icon--styleIcon--3-PzQ.styles--thumb--19_d9.style_icon--fillIcon--2kZ-_ > div > div > div > svg > circle"):
		if element.get_attribute("fill") != "none":
			color_values.append(element.get_attribute("fill"))

	return dict(zip(color_keys, color_values))

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