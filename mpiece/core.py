"""
	mpiece.markdown
	~~~~~~~~~~~~~~~

	MPiece core

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""

from mpiece.lexer import Token


class MPieceException(Exception):
	""" Base MPiece exception
	"""

	def __str__(self):
		return self.message


class RenderFunctionNotFoundException(MPieceException):
	"""	Render function not found in renderer class.
	"""

	def __init__(self, function_name, class_name):
		self.message = 'Function "render_%s" not found in the %s class' % (function_name, class_name)


class ParseFunctionNotFoundException(MPieceException):
	""" Parse function not found in Lexer class.
	"""

	def __init__(self, function_name, class_name):
		self.message = 'Function "parse_%s" not found in the "%s" lexer.' % (function_name, class_name)


class RegexNotFoundException(MPieceException):
	""" Regex expression not found in Lexer class.
	"""

	def __init__(self, regex_name, class_name):
		self.message = 'Regular expression "regex_%s" not found in the "%s" lexer class. ' % (regex_name, class_name)


class InvalidDataException(MPieceException):
	""" Parse function in Lexer class returns an invalid data.
	"""

	def __init__(self, function_name, class_name):
		self.message = (
			'Function "%s.%s" returns an invalid data. The function should return a Token object, string or list\'s '
			'of Token objects/string.' % (class_name, function_name)
		)


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
		output = self.renderer.post_process_text(text)

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
				raise RegexNotFoundException(element, self.lexer.__class__.__name__)

			text = regex.sub(self.replace_str_token(element, father_extras), text)

		token.text = text
		return token

	def replace_str_token(self, element, extras_to_children):

		def _replace_regex(mo):
			try:
				parse_func = self.lexer.all_parse_func[element]
			except KeyError:
				raise ParseFunctionNotFoundException(element, self.lexer.__class__.__name__)

			if not extras_to_children:
				# parse function without extra for childrens.
				result = parse_func(mo)
			else:
				# parse function with extras for children.
				result = parse_func(mo, **extras_to_children)

			if not isinstance(result, (list, tuple)):
				result = [result]

			str_r = ''
			for r in result:

				if isinstance(r, str):
					# r is str add to main str and continue.
					str_r += r
					continue

				if isinstance(r, Token):
					# r is token. It is parsed.
					r = self.parse_str_token(r)
				else:
					# r isn't a str or a Token
					raise InvalidDataException(parse_func.__name__, self.lexer.__class__.__name__)

				# Render token
				try:
					render_func = self.renderer.all_render_funcs[r.render_func]
				except KeyError:
					raise RenderFunctionNotFoundException(r.render_func, self.renderer.__class__.__name__)

				if r.has_text:
					# render with text.
					r.render_text = render_func(text=r.text, **r.extras)
				else:
					# render without text
					r.render_text = render_func(**r.extras)

				# add token to token list
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
