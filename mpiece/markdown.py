"""
	mpiece.markdown
	~~~~~~~~~~~~~~~

	Main class and exception classes.

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""


class MPieceException(Exception):
	""" Base MPiece exception
	"""

	def __str__(self):
		return self.message


class RenderFunctionNotFound(MPieceException):
	"""	Render function not found in renderer class.
	"""

	def __init__(self, function_name, class_name):
		self.message = 'Function "render_%s" not found in the %s class' % (function_name, class_name)


class ParseFunctionNotFound(MPieceException):
	""" Parse function not found in Lexer class.
	"""

	def __init__(self, function_name, class_name):
		self.message = 'Function "parse_%s" not found in the "%s" lexer.' % (function_name, class_name)


class RegexNotFound(MPieceException):
	""" Regex expression not found in Lexer class.
	"""

	def __init__(self, regex_name, class_name):
		self.message = 'Regular expression "regex_%s" not found in the "%s" lexer class. ' % (regex_name, class_name)


class InvalidData(MPieceException):
	""" Parse function in lexer returns an invalid data.
	"""

	def __init__(self, function_name, class_name):
		self.message = (
			'Function "%s.parse_%s" returns an invalid data. The function should return a Token object, list\'s '
			'Token object or a string.' % (class_name, function_name)
		)


class Token:
	"""
		Token class.
		:param str render_func: Render function name which the token will use.
			NOTE: all render function name start with the `render_` prefix. You shoul add the function name without
			include this prefix.
		:param str text: markdown text
		:param dict extras: extra data to render function.
		:param [str] order: Markdown  elements which will be parsed in the Token text.
		:param dict extras_to_children: Extra data used in the children parse functions.

	"""

	def __init__(self, render_func, text=None, extras={}, order=[], extras_to_children={}):
		self.render_func = render_func
		self.has_text = text is not None
		self.text = text or ''
		self.extras = extras
		self.order = order
		self.render_text = ''
		self.extras_to_children = extras_to_children


class MPiece(object):
	""" Tranform the markdown text.
	"""

	TOKEN_STR = '////TOKENMDA//%d////'

	def parse(self, text, lexer, renderer):
		""" Transform markdown text.
			:param str text: Markdown text.
			:param lexer.LexerBase lexer: lexer.LexerBase subclass.
			:param renderer.Renderer renderer: renderer.Renderer subclass.
			:return: Depend of renderer subclass.
		"""
		self.lexer = lexer
		self.renderer = renderer
		self.token_list = []
		self.token_list_length = 0

		# preprocess text
		text = self.lexer.pre_process_text(text)

		# Parse footnotes
		if 'footnotes' not in self.lexer.exclude:
			text = self.lexer.parse_footnotes(text)

		main_token = self.lexer.get_main_token(text)
		main_token = self.parse_str_token(main_token)
		text = self.parse_token_str(main_token.text)
		output = self.lexer.post_process_text(text)

		return output

	def parse_str_token(self, token):
		text = token.text

		# Token hasn't text
		if not token.has_text:
			return token

		# Get the extras to the children.
		father_extras = token.extras_to_children

		for element in token.order:
			if element in self.lexer.exclude:
				continue

			try:
				regex = self.lexer.all_regex[element]

			except KeyError:
				raise RegexNotFound(element, self.lexer.__class__.__name__)

			text = regex.sub(self.replace_str_token(element, father_extras), text)

		token.text = text
		return token

	def replace_str_token(self, element, extras_to_children):

		def _replace_regex(mo):
			try:
				if not extras_to_children:
					result = self.lexer.all_parse_func[element](mo)
				else:
					result = self.lexer.all_parse_func[element](mo, **extras_to_children)

				if isinstance(result, str):
					return result
			except KeyError:
				raise ParseFunctionNotFound(element, self.lexer.__class__.__name__)

			if isinstance(result, Token):
				result = [result]

			if not isinstance(result, (list, tuple)):
				raise InvalidData(self.lexer.get_parse_func(element).__name__, self.lexer.__class__.__name__)

			str_r = ''
			for r in result:
				# parse token text
				r = self.parse_str_token(r)

				# Render token
				try:
					render_func = self.renderer.all_render_funcs[r.render_func]
				except KeyError:
					raise RenderFunctionNotFound(r.render_func, self.__class__.__name__)

				if r.has_text:
					r.render_text = render_func(text=r.text, **r.extras)
				else:
					r.render_text = render_func(**r.extras)

				str_r += self.TOKEN_STR % self.token_list_length
				self.token_list_length += 1
				self.token_list.append(r)

			return str_r
		return _replace_regex

	def replace_token_str(self, mo):
		return self.token_list[int(mo.group('number'))].render_text

	def parse_token_str(self, text):

		replace_func = self.replace_token_str
		regex = self.lexer.regex_token
		text, changes = regex.subn(replace_func, text)
		while changes > 0:
			text, changes = self.lexer.regex_token.subn(replace_func, text)

		return text
