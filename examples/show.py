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
import re


dir_base = os.path.join(os.path.dirname(os.path.abspath(__file__)))

help_str = """Transform the markdown in html code and show the result in a web browser.
show.py filepath|--help
- filepath: filename inside of example/data directory or absoulte filepath
"""

try:
	from mpiece import markdown
	from mpiece.lexer import Lexer, Token
	from mpiece.renderer import HtmlRenderer

except ImportError:
	sys.path.insert(0, os.path.join(dir_base, '../'))
	from mpiece import markdown
	from mpiece.lexer import Lexer, Token
	from mpiece.renderer import HtmlRenderer


def get_file_text(filename):
	with open(filename, 'r') as f:
		content = f.read()

	return content


def print_help():
	print(help_str)


class CustomLexer(Lexer):
	"""
		Custom lexer to makes 2 differents grammars:
		- Text color: `#color_hex text color changed##`
		- Add emoji: `Normal text, :emoji:, continue text.
	"""

	#: Emoji list with all emojis used in the markdown grammar.
	#: Key is the emojin name in markdown. Value is the emoji css class.
	EMOJI_LIST = {
		'smile': 'smile',
		'XD': 'laughing',
		'love': 'heart-eyes',
	}

	#: Regular expression to color text grammar.
	regex_color = re.compile(r'#(?P<color>[0-9a-fA-F]{3}|[0-9a-fA-F]{6}) (?P<text>.+?)##')
	#: Regular expression to emoji grammar.
	regex_emoji = re.compile(r':(?P<emoji>[a-zA-Z0-9]+):')

	def define_order(self):
		"""
			Add the new grammar elements to in the order ot the default grammar elements.
		"""
		# Add color grammar
		self.order_inline.insert(1, 'color')
		# add emoji grammar.
		self.order_inline.append('emoji')
		super(CustomLexer, self).define_order()

	def parse_color(self, mo):
		""" Parse function that process the regular expression for the color grammar.
		"""
		color = mo.group('color')
		text = mo.group('text')
		order = ['bold', 'italic', 'underline', 'strike']
		return Token('color', text, extras={'color': color}, order=order)

	def parse_emoji(self, mo):
		""" Parse function that process the regular expression for the color grammar.
		"""
		emoji = self.EMOJI_LIST.get(mo.group('emoji'), False)
		if not emoji:
			return mo.group(0)
		return Token('emoji', extras={'emoji_name': emoji})


class CustomRenderer(HtmlRenderer):

	def render_fenced_code(self, code, lang, title):
		""" Transform the fenced code token in html code
		"""
		title, code = self.escape_args(title, code)
		html = '<div class="code-fenced"><div class="title">%s</div><pre>%s</pre></div>'
		title = title if title else 'Código'

		return html % (title, code)

	def render_color(self, text, color):
		""" Transform the color token in html code
		"""
		text = self.escape(text)
		return '<span style="color:#%s">%s</span>' % (color, text)

	def render_emoji(self, emoji_name):
		""" Transform the emoji token in html code
		"""
		return '<span class="twa twa-lg twa-%s"></span>' % emoji_name


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

	text = markdown(text, renderer=CustomRenderer(), lexer=CustomLexer())

	style_filename = 'file://%s' % os.path.join(dir_base, 'data/style.css')
	html = (
		'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>MPiece - markdown parser.</title>'
		'<link href="%s" rel="stylesheet" type="text/css"></head>'
		'<body>%s</body>'
	) % (style_filename, text)

	with open(os.path.join(dir_base, 'index.html'), 'w') as f:
		f.write(html)

	webbrowser.open('file://%s' % os.path.join(dir_base, 'index.html'))
