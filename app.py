from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setup Chrome
options = Options()
options.add_argument(r'--user-data-dir=C:\Users\abhi\AppData\Local\Google\Chrome\User Data')
options.add_argument('--profile-directory=Profile 2')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('log-level=3')

# Load web page
driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.get('https://www.figma.com/file/2LwEexu4O1HaYEdl5wqMYv/Portfolio?node-id=6%3A3')
print('Web Page Loaded')

# Initiating variables
project_name = driver.title.split('–')[0].strip()
webpage = driver.page_source


