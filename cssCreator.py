from os import listdir
from htmlCreator import find_navbar

nav_template = '''
#nav {
	display: flex;
	justify-content: [nav_direction];
	font-weight: normal;
	margin: 0;
}

li {
	list-style: none;
}

#nav li {
	margin-top: 30px;
}

.nav-item a {
	text-decoration: none;
	font-size: 2rem;
	color: black;
	margin-right: 5rem;
}
'''

def create_css_template(title, colors, fonts):
	css_template = None
	with open('Data/css_template.css', "r") as template:
		css_template = template.readlines()

	with open(f'{title}/styles.css', "w") as css:
		# Set color variables
		css_color_values = [colors.get(color) for color in colors]
		css_colors = [f'\t--{variable}: {value};' for variable, value in zip(colors, css_color_values)]

		# Set Font Faces
		font_names = listdir(f'{title}/fonts/')
		font = font_names[0].split('.ttf')[0]

		# Get navbar details
		nav_position = None
		with open("global_variables.txt", "r") as file:
			for line in file:
				if 'nav' in line:
					nav_position = line

		navbar_html = nav_template.replace('[nav_direction]', nav_position.strip('nav-'))

		for count, line in enumerate(css_template):
			current_line = css_template[count]
			if '/*[variables]*/' in line:
				css_template[count] = current_line.replace('/*[variables]*/', '\n'.join(css_colors))
			if '/*[font]*/' in line:
				css_template[count] = current_line.replace('/*[font]*/', f'\'{font}\'')
			if '/*[font-url]*/' in line:
				css_template[count] = current_line.replace('/*[font-url]*/', font + '.ttf')
			if '/*[Navbar]*/' in line:
				css_template[count] = current_line.replace('/*[Navbar]*/', navbar_html)
		css.writelines(css_template)
