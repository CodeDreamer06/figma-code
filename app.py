from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from general import init, create_folder, log
import fontFinder
import htmlCreator, cssCreator

# Start Chrome
options = init()
driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.get('https://www.figma.com/file/2LwEexu4O1HaYEdl5wqMYv/Portfolio?node-id=6%3A3')
log('Web Page Loaded', 'cyan')

project_name = driver.title.split('–')[0].strip()

with open("global_variables.txt", "w") as file:
	file.write(project_name)
	create_folder(project_name)

text_styles = []
unknown = []

sleep(16)
soup = BeautifulSoup(driver.page_source, "html.parser")

def find_variables():
	color_keys = []
	for element in soup(class_="styles--name--RhNAx"):
		if 'color' in element.getText():
			color_keys.append(element.getText())
		elif 'text' in element.getText():
			text_styles.append(element.getText())
		else:
			unknown.append(element.getText())

	log('Found ' + str(len(color_keys)) + ' Colors', 'green')
	log('Found ' + str(len(text_styles)) + ' Text Styles', 'green')
	if unknown:
		print('Unkown variables: ', unknown)

	color_values = []
	for element in soup.find_all("svg", class_="style_icon--fillPositionedContainer--2CRE_"):
		if element.circle["fill"] != "none":
			color_values.append(element.circle["fill"])

	return dict(zip(color_keys, color_values))

log('Finding Fonts...', 'cyan')
fontFinder.find_fonts(driver.page_source)

log('Finding Variables...', 'cyan')
colors = find_variables()

log('Creating html template', 'cyan')
htmlCreator.create_html_template(project_name)

log('Creating CSS template', 'cyan')
cssCreator.create_css_template(project_name, colors, None)
