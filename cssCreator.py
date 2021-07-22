from os import listdir

def create_css_template(title, colors, fonts):
	css_template = None
	with open('Data/css_template.css', "r") as template:
		css_template = template.readlines()

	with open(f'{title}/styles.css', "w") as css:
		# Set color variables
		css_color_variables = [color.split('color-')[1] for color in colors]
		css_color_values = [colors.get(color) for color in colors]
		css_colors = [f'\t--{variable}: {value};' for variable, value in zip(css_color_variables, css_color_values)]
		css_template = [(css_template[count].replace('[variables]', '\n'.join(css_colors))) for count, line in enumerate(css_template)]
		# Set Font Faces
		font_names = listdir(f'{title}/fonts/')
		font = font_names[0].split('.ttf')[0]
		css_template = [(css_template[count].replace('[font]', f'\'{font}\'')) for count, line in enumerate(css_template)]
		css_template = [(css_template[count].replace('[font-url]', font)) for count, line in enumerate(css_template)]
		css.writelines(css_template)
