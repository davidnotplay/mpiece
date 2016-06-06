#!/bin/python

"""
	show.py
	~~~~~~~

	Script to converts markdown text in html code and show it in a web browser.

	This script only is use to show the markdown text in a web browser.
	This script isn't necessary to use mpiece package.

	Command options:
		- Show help:
			- $ show.py --help

		- Converts filename in html code and show it in a web browser.
			- $ show.py "filename_inside data directory".
			- $ show.py "absolute_filename".

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""


import sys
import os
import webbrowser


dir_base = os.path.join(os.path.dirname(os.path.abspath(__file__)))

help_str = """Transform the markdown in html code and show the result in a web browser.
show.py filepath|--help
- filepath: filename inside of example/data directory or absoulte filepath
"""


def get_file_text(filename):
	with open(filename, 'r') as f:
		content = f.read()

	return content


def print_help():
	print(help_str)


try:
	from mpiece import markdown

except ImportError:
	sys.path.insert(0, os.path.join(dir_base, '../'))
	from mpiece import markdown


if __name__ == "__main__":
	if len(sys.argv) == 1 or sys.argv[1] == '--help':
		print_help()
		exit()

	filename = os.path.join(dir_base, 'data', sys.argv[1])
	try:
		text = get_file_text(filename)
	except FileNotFoundError:
		try:
			text = get_file_text(sys.argv[1])
		except:
			print('filename %s not found' % sys.argv[1])
			exit()

	text = markdown(text)

	style_filename = 'file://%s' % os.path.join(dir_base, 'data/style.css')
	html = (
		'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Markdown Advance</title>'
		'<link href="%s" rel="stylesheet" type="text/css"></head>'
		'<body>%s</body>'
	) % (style_filename, text)

	with open(os.path.join(dir_base, 'index.html'), 'w') as f:
		f.write(html)

	webbrowser.open('file://%s' % os.path.join(dir_base, 'index.html'))
