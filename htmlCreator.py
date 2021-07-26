from general import log

def find_navbar(element):
	if 'Navbar' in element.text:
		if 'center' in element.text:
			log('Center NavBar', 'yellow')
			return 'nav-center'
		if 'start' in element.text:
			log('Start NavBar', 'yellow')
			return 'nav-start'
		if 'end' in element.text:
			log('End NavBar', 'yellow')
			return 'nav-end'

def set_hero(title, subtitle=None, img_source=None, grid=True):
	grid_hero = '''
	<div class="container col-xxl-8 px-4 py-5">
    	<div class="row flex-lg-row-reverse align-items-center g-5 py-5">
      		<div class="col-10 col-sm-8 col-lg-6"><img src="[img-source]" class="d-block mx-lg-auto img-fluid" alt="" width="700" height="500" loading="lazy"></div>
  		<div class="col-lg-6">
			<h1 class="display-5 fw-bold lh-1 mb-3">[hero-title]</h1>
			<p class="lead">[hero-description]</p>
		<div class="d-grid gap-2 d-md-flex justify-content-md-start">
			<button type="button" class="btn btn-primary btn-lg px-4 me-md-2">[hero-button]</button>
		</div>
		</div>
	</div>
	</div>
	'''
	center_hero = '''
	<div class="px-4 py-5 my-5 text-center">
		<img class="d-block mx-auto mb-4" src="[img-source]" alt="">
		<h1 class="display-5 fw-bold">[hero-title]</h1>
    	<div class="col-lg-6 mx-auto">
      		<p class="lead mb-4">[hero-description]</p>
      		<div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
        		<button type="button" class="btn btn-primary btn-lg px-4 gap-3">[Primary button]</button>
        		<button type="button" class="btn btn-outline-secondary btn-lg px-4">[Secondary]</button>
      		</div>
    	</div>
  	</div>
	'''
	# Todo: add functionality for center hero.
	if grid and title != '0':
		grid_hero = grid_hero.replace('[hero-title]', title.strip('Title-'))
		grid_hero = grid_hero.replace('[hero-description]', subtitle.strip('Subtitle-'))
		if img_source:
			grid_hero = grid_hero.replace('[img-source]', img_source)
		return grid_hero

def create_html_template(title, elements):
	html_template = None
	with open('Data/html_template.html', "r") as template:
		html_template = template.readlines()

	with open(f'{title}/index.html', "w") as html:
		# Find [title] and replace with title
		html_template = [(html_template[count].replace('[title]', title)) for count, line in enumerate(html_template)]
		# Finding navbar and nav-items
		nav_items = []
		hero_title, hero_description = None, None
		hero_html = None
		for element in elements:
			nav_position = find_navbar(element)
			if nav_position != None:
				with open("global_variables.txt", "a") as file:
					file.write('\n' + nav_position)
			if 'li' in element.text:
				nav_items.append(element.text)
			if 'Hero' in element.text and 'grid' in element.text:
				log('Grid Hero', 'yellow')
			if 'Title' in element.text and hero_title != '0':
				hero_title = element.text
			if 'Subtitle' in element.text and hero_description != '0':
				hero_description = element.text
			if hero_title and hero_description:
				temp_hero = set_hero(hero_title, hero_description, grid=True)
				if temp_hero != None:
					hero_html = temp_hero
				hero_title, hero_description = '0', '0'
			if 'Hero' in element.text and 'center' in element.text:
				log('Center Hero', 'yellow')

		nav_items = ['\t\t<li class="nav-item"><a href="#' + nav_item.strip('-li') + '">' + nav_item.strip('-li') + '</a></li>' for nav_item in nav_items if 'Home' not in nav_item]
		html_template = [(html_template[count].replace('[body]', '\t<ul id="nav"> [body]')) for count, line in enumerate(html_template)]
		html_template = [(html_template[count].replace('[body]', '\n'.join(nav_items) + '\n\t</ul>' + '\n[body]')) for count, line in enumerate(html_template)]
		# Add Hero
		html_template = [(html_template[count].replace('[body]', hero_html + '\n[body]')) for count, line in enumerate(html_template)]
		# Add Sections
		sections = [element.text for element in elements if 'section' in element.text]
		html_section = '\n\t\t<section id="[section-name]">\n\t\t\t\n\t\t</section>'
		html_sections = [html_section.replace('[section-name]', section) for section in sections if 'Hero' not in section]
		html_template = [(html_template[count].replace('[body]', ''.join(html_sections))) for count, line in enumerate(html_template)]
		html.writelines(html_template)
