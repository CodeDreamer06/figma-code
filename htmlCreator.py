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

def create_html_template(title, elements):
	html_template = None
	with open('Data/html_template.html', "r") as template:
		html_template = template.readlines()

	with open(f'{title}/index.html', "w") as html:
		# Find [title] and replace with title
		html_template = [(html_template[count].replace('[title]', title)) for count, line in enumerate(html_template)]
		# Finding navbar and nav-items
		nav_items = []
		for element in elements:
			nav_position = find_navbar(element)
			if nav_position != None:
				with open("global_variables.txt", "a") as file:
					file.write('\n' + nav_position)
			if 'li' in element.text:
				nav_items.append(element.text)

		nav_items = ['\t\t<li class="nav-item"><a href="#' + nav_item.strip('-li') + '">' + nav_item.strip('-li') + '</a></li>' for nav_item in nav_items if 'Home' not in nav_item]
		html_template = [(html_template[count].replace('[body]', '\t<ul id="nav"> [body]')) for count, line in enumerate(html_template)]
		html_template = [(html_template[count].replace('[body]', '\n'.join(nav_items) + '\n\t</ul>' + '\n[body]')) for count, line in enumerate(html_template)]
		# Add Sections
		sections = [element.text for element in elements if 'section' in element.text]
		html_section = '\n\t\t<section id="[section-name]">\n\t\t\t\n\t\t</section>'
		html_sections = [html_section.replace('[section-name]', section) for section in sections]
		html_template = [(html_template[count].replace('[body]', ''.join(html_sections))) for count, line in enumerate(html_template)]
		html.writelines(html_template)
