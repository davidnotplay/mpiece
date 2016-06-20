"""
	mpiece.__init__
	~~~~~~~~~~~~~~~

	This file has a MarkdownInit object, called markdown. it is used to transform the markdown text easily.

	Example:
		.. code:: python

			from mpiece import markdown
			result = markdown(markdown_text)
			print(result)

		..code:: python

			from mpiece import Markdown
			markdown = Markdown()
			result = markdown(markdown_text)
			print(result)

	:license: BSD, see LICENSE for details
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""

from mpiece.core import MPiece
from mpiece.lexer import Lexer
from mpiece.renderer import HtmlRenderer

__version__ = '0.2.3'
__author__ = 'David Casado Martinez <dcasadomartinez@gmail.com>'
__all__ = ['__version__', '__author__', 'Markdown', 'markdown']


class Markdown(object):
	"""
		Class to transform the markdown text easily.

		:Example:
			.. code:: python

				from mpiece import Markdown
				from mpiece.lexer import Lexer
				from mpiece.renderer import HtmlRenderer

				markdown = Markdown()
				markdown.lexer = Lexer()
				markdown.renderer = HtmlRenderer()

				result = markdown(text_markdown)
	"""

	def __init__(self):
		self.lexer = None
		self.renderer = None

	def __call__(self, text, lexer=None, renderer=None):
		"""
			Transform markdown text.

			:param str text: Markdown text.
			:param mpiece.lexer.Lexer lexer: Lexer subclass.
			:param mpiece.renderer.Renderer renderer: Renderer subclass.
			:return: It depends of the renderer class.
			:exception: :class:`mpiece.core.RenderFunctionNotFoundException`
			:exception: :class:`mpiece.core.ParseFunctionNotFoundException`
			:exception: :class:`mpiece.core.RegexNotFoundException`
			:exception: :class:`mpiece.core.InvalidDataException`

		"""
		self.lexer = lexer or self.lexer or Lexer()
		self.renderer = renderer or self.renderer or HtmlRenderer()
		return MPiece().parse(text, self.lexer, self.renderer)


def markdown(text, lexer=None, renderer=None):
	"""
		Transform the markdown text easily.

		:param str text: Markdown text.
		:param mpiece.lexer.Lexer lexer: Lexer subclass.
		:param mpiece.renderer.Renderer renderer: Renderer subclass.
		:return: It depends of the renderer class.
		:exception: :class:`mpiece.core.RenderFunctionNotFoundException`
		:exception: :class:`mpiece.core.ParseFunctionNotFoundException`
		:exception: :class:`mpiece.core.RegexNotFoundException`
		:exception: :class:`mpiece.core.InvalidDataException`
	"""
	return Markdown()(text, lexer, renderer)
