"""
	mpiece.__init__
	~~~~~~~~~~~~~~~

	This file has a MarkdownInit object, called markdown. it is used to transform the markdown text easily.

	Example:
	```
		from mpiece import markdown

		result = markdown(markdown_text)
		print(result)
	```

	:package: markdown_advance
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""

from mpiece.markdown import MPiece
from mpiece.lexer import Lexer
from mpiece.renderer import HtmlRenderer

__version__ = '0.1.0'
__author__ = 'David Casado Martinez <dcasadomartinez@gmail.com>'
__all__ = [
	'__version__', '__author__',
	'markdown', 'MarkdownAdvance', 'Lexer', 'HtmlRenderer'
]


class MarkdownInit(object):
	"""
		Class to transform the markdown text easily.
	"""

	def __init__(self):
		self.lexer = None
		self.renderer = None

	def __call__(self, text, lexer=None, renderer=None):
		"""
			Transform markdown text.
			:param str text: Markdown text.
			:param lexer.LexerBase lexer: lexer.LexerBase subclass.
			:param renderer.Renderer renderer: renderer.Renderer subclass.
			:return: Depend of renderer subclass.
		"""
		self.lexer = lexer or self.lexer or Lexer()
		self.renderer = renderer or self.renderer or HtmlRenderer()
		return MPiece().parse(text, self.lexer, self.renderer)


#: Variable used to converts the markdown text.
markdown = MarkdownInit()
