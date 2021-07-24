from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from general import init, wait, create_folder, log
import fontFinder
import htmlCreator, cssCreator

# Start Chrome
options = init()
driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.get('https://www.figma.com/file/2LwEexu4O1HaYEdl5wqMYv/Portfolio?node-id=6%3A3')
actions = ActionChains(driver)
log('Web Page Loaded', 'cyan')
project_name = driver.title.split('–')[0].strip()

with open("global_variables.txt", "w") as file:
	file.write(project_name)
	create_folder(project_name)

text_styles = []
unknown = []

wait(driver)

def find_variables():
	color_keys = []
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

log('Finding Fonts...', 'cyan')
fontFinder.find_fonts(driver.page_source)

log('Finding Variables...', 'cyan')
colors = find_variables()

# Reopening with the main frame selected
driver.get('https://www.figma.com/file/2LwEexu4O1HaYEdl5wqMYv/Portfolio?node-id=6%3A4')
wait(driver)

actions.send_keys(Keys.ENTER).perform()
actions.send_keys(Keys.ENTER).perform()

log('Creating html template', 'cyan')
sidebar_elements = driver.find_elements_by_css_selector('span.object_row--rowText--2tEqb.ellipsis--ellipsis--1RWY6')
htmlCreator.create_html_template(project_name, sidebar_elements)

log('Creating CSS template', 'cyan')
cssCreator.create_css_template(project_name, colors, None)
