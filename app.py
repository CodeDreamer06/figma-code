from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from general import init, wait, create_folder, log, find_variables
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

wait(driver)

log('Finding Fonts...', 'cyan')
fontFinder.find_fonts(driver.page_source)

log('Finding Variables...', 'cyan')
colors = find_variables(driver)

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
