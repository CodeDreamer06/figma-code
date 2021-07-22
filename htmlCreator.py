def create_html_template(title):
	html_template = None
	with open('Data/html_template.html', "r") as template:
		html_template = template.readlines()

	with open(f'{title}/index.html', "w") as html:
		# Find [title] and replace with title
		html_template = [(html_template[count].replace('[title]', title)) for count, line in enumerate(html_template)]
		html.writelines(html_template)
