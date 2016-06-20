"""
	mpiece.lexer
	~~~~~~~~~~~~~~~

	Lexer classes.

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""

import re


class Token:
	""" The token save info about markdown grammar.
		They are used in the parse function in lexer class.

		:param str render_func:
			Render function name which the token will use.

			.. note::
				All render function name start with the `render_` prefix.
				You shoul add the function name without include this prefix.

		:param str text:
			Text inside of the markdown grammar.
			This text will be re-parsed to find more markdown grammar.

		:param dict extras:
			Extra data to render function.
			The dictionary elements will convert in arguments for the render function

		:param [str] order:
			Markdown grammar elements that the lexer will find in the token text.

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


class Lexer(object):
	"""
		Converts the markdown text in tokens.
		All lexer classes should be subclasses of this class.

		This class and their subclass are used in the :func:`mpiece.markdown()` function or
		in the :class:`mpiece.Markdown` class.

		:param set exclude: The markdown grammar name which you want exclude in the markdown text.
			The default list of markdown grammar names is:

			- fenced_code
			- table
			- ulist
			- olist
			- blockquote
			- header
			- header2
			- break_line
			- new_line
			- image
			- link
			- code_inline
			- bold
			- italic
			- underline
			- strike

		:param int tab_size: Tabulators size.
		:param str escape_chars:
			String with the characters escaped if they have the have the ``\\`` character before.
			This string is added to the string :attr:`Lexer.escape_chars`

		:Example:
			.. code:: python

				from mpiece.lexer import Lexer
				from mpiece import markdown

				text_md = '*italic*, **this is bold**, `this is a code inline`'

				# markdown normal
				result = markdown(text_md)
				print(result)
				# output: <p><em>italic</em>, <strong>this is bold</strong>, <code>this is a code inline</code></p>

				# markdown excluding bold and code inline
				lexer_exclude = Lexer(exclude=set({'bold', 'code_inline'}))
				result = markdown(text_md, lexer=lexer_exclude)
				print(result)
				# output: <p><em>italic</em>, **this is bold**, `this is a code inline`</p>

		:ivar str escape_chars:
			List of characters escaped if they has the character \ before.

			:Initial value:
				'\*~\`\_[]()\\>.'

		:ivar [str] order_inline:
			Order of the inline elements.

			:Initial value:
				['escape_backslash', 'code_inline', 'image', 'link', 'bold', 'italic', 'bold', 'underline', 'strike']

		:ivar [str] order_block:
			Order of the block elements.

			:Initial value:
				[fenced_code', 'table', 'ulist', 'olist', 'blockquote', 'header', 'header2', 'break_line', 'new_line']

		:ivar [str] initial_order:
			Define the initial order for the lexer class.

			:Initial value:
				self.order_block + self.order_inline
	"""

	# Main regular expression. Transform tokens in texts
	regex_token = re.compile('////TOKENMDA//(?P<number>[0-9]+)////')

	# Markdown regular expressions
	regex_escape_backslash = re.compile(r'\\(?P<char>.)', re.S)
	regex_bold = re.compile(r'\*\*(?P<text>[^*]+)\*\*')
	regex_italic = re.compile(r'(?<!(?<!\*)\*)\*(?P<text>[^*\n]+)\*(?!\*(?!\*))')
	regex_underline = re.compile(r'_(?P<text>[^_]+)_')
	regex_strike = re.compile(r'\~(?P<text>[^\~]+)\~')
	regex_code_inline = re.compile(r'`(?P<code>[^`]+)`')
	regex_link = re.compile(r'\[(?P<text>.+?)\]\((?P<href>.+?)(?:[ ](?P<quote>["\'])(?P<title>.*?)(?P=quote))?\)')
	regex_image = re.compile(r'\!\[(?P<alt>.+?)\]\((?P<src>.+?)(?:[ ](?P<quote>["\'])(?P<title>.*?)(?P=quote))?\)')
	regex_new_line = re.compile(
		r'^(?P<text>(?:(?!////TOKENMDA|\s+\n)[^\n]+\n)*(?!////TOKENMDA|\s+\n)[^\n]+)(?=\n|////TOKENMDA|$)',
		re.M
	)
	regex_simple_new_line = re.compile(r'^(?![ ]*////TOKENMDA)(?P<text>[^\n]+)$', re.M)
	regex_olist = re.compile(r'(?P<list>^(?P<start>[0-9]+)\.[ ].*?)\n(?=\n|$)', re.S | re.M)
	"""regex_olist = re.compile(
		r'(?P<list>^(?P<start>[0-9]+)\.[ ][^\n]+\n(?:(?:[0-9]+\.|[ ])[^\n]+\n?|\n(?!\n|[*\-]))*)',
		re.S | re.M
	)"""
	regex_olist_item = re.compile(
		r'^(?P<iden>[ ]*)[0-9]+\.[ ](?P<item>.*?(?:\n|$)(?:(?P=iden)(?![0-9]+\.).*?(?:\n|$))*)',
		re.M
	)
	regex_osublist = re.compile(r'^(?P<list>(?P<iden>[ ]+)(?P<start>[0-9]+)\.[ ](?:.*\n(?=(?P=iden)))*[^\n]+)', re.M)
	regex_ulist = re.compile(r'(?P<list>^(?P<start>[*-])[ ].*?)\n(?=\n|$)', re.S | re.M)
	"""regex_ulist = re.compile(
		r'(?P<list>^(?P<start>[*\-])[ ][^\n]+\n(?:(?:(?P=start)|[ ])[^\n]+\n?|\n(?!\n|[*\-]))*)',
		re.M | re.S
	)"""
	regex_ulist_item = re.compile(r'^(?P<iden>[ ]*)[*-][ ](?P<item>.*?(?:\n|$)(?:(?P=iden)(?![*-]).*?(?:\n|$))*)', re.M)
	regex_usublist = re.compile(r'^(?P<list>(?P<iden>[ ]+)(?P<start>[*-])[ ](?:.*\n(?=(?P=iden)))*[^\n]+)', re.M)
	regex_blockquote = re.compile(r'(?P<blockquote>^(?:[ ]*\>[^\n]*\n?)+)', re.M)
	regex_header = re.compile(r'^[ ]*(?P<level>#+) (?P<text>.*?)(?:[ ](?P=level))?$', re.M)
	regex_header2 = re.compile(r'^(?P<text>[^\n]+)\n(?P<sym>=+|-+|~+)$', re.M)
	regex_fenced_code = re.compile(
		r'[ ]*`{3}[ ]*(?P<lang>[^\n"]+?)?(?: ?(?!\\)"(?P<title>[^\n]+)(?!\\)")?\n(?P<code>.*?)\n[ ]*`{3}',
		re.S
	)
	regex_break_line = re.compile(r'^(?:-{3,}|\*{3,}|_{3,})$', re.M)
	regex_footnotes = re.compile(
		r'^\[\^(?P<name>.+)\]:[ ]*(?P<value>[^\n]*(?=\n)(?:\n(?P<ind>[ ]+)[^\n]*(?=\n))?(?:\n(?P=ind)[^\n]*(?=\n))*)',
		re.M
	)
	regex_apply_footnotes = re.compile(r'\[\^(?P<name>.+)\]')
	regex_table = re.compile(
		r'^[ ]*(?P<table>\|[^\n]*\n[ ]*\|[ \|\-:]+\n[ ]*(?:\|[^\n]+\n?)*)(?=\n|$)',
		re.S | re.M
	)
	regex_table_header = re.compile(r'^[ ]*(?P<head>\|[^\n]+)')
	regex_table_header_cell = re.compile(r'^(?P<cells>\|[^\n]+?)\|?$')
	regex_table_body = re.compile(r'^(?P<align>[| \-:]+?)\|?\n(?P<body>.*)', re.S | re.M)
	regex_table_body_row = re.compile(r'^[ ]*(?P<row>\|[^\n]+)', re.M)
	regex_table_body_cell = re.compile(r'^(?P<cells>\|[^\n]+?)\|?$')

	def __init__(self, exclude=set(), tab_size=4, escape_chars=''):
		self.tab_size = tab_size
		self.escape_chars = '*~`_[]()\\>.' + escape_chars
		self.exclude = getattr(self, 'exclude', set()) | exclude

		# Get al regex expressions and parse functions.
		self.all_regex = {}
		self.all_parse_func = {}
		for item in dir(self):
			if item.startswith('regex_'):
				self.all_regex[item[6:]] = getattr(self, item)

			if item.startswith('parse_'):
				self.all_parse_func[item[6:]] = getattr(self, item)

		self.order_inline = [
			'escape_backslash', 'code_inline', 'image', 'link', 'bold', 'italic', 'bold', 'underline', 'strike'
		]
		self.order_block = [
			'fenced_code', 'table', 'ulist', 'olist', 'blockquote', 'header', 'header2', 'break_line', 'new_line'
		]
		self.define_order()

	def define_order(self):
		""" Make the order of the grammar inside of the markdown elements.
		"""
		# list
		self.order_ulist = ['ulist_item']
		self.order_subulist = ['ulist_item']
		self.order_ulist_item = list(self.order_block)

		try:
			self.order_ulist_item.remove('fenced_code')
			self.order_ulist_item.remove('table')

			# Replace u/olist to u/osublist and new_line to simple_new_line
			self.order_ulist_item[self.order_ulist_item.index('ulist')] = 'usublist'
			self.order_ulist_item[self.order_ulist_item.index('olist')] = 'osublist'
			self.order_ulist_item[self.order_ulist_item.index('new_line')] = 'simple_new_line'

		except ValueError:
			# ulist or/and olist are excluded and they don't exists in order_block list.
			pass

		self.order_olist = ['olist_item']
		self.order_subolist = ['olist_item']
		self.order_olist_item = list(self.order_ulist_item)

		# Blockquote
		self.order_blockquote = list(self.order_block)
		try:
			self.order_blockquote.remove('table')
			self.order_blockquote.remove('fenced_code')
			self.order_blockquote[self.order_blockquote.index('new_line')] = 'simple_new_line'
		except:
			pass

		# header
		self.order_header = list(self.order_inline)
		self.order_header.remove('image')

		# tables
		self.order_table = ['table_header', 'table_body']
		self.order_table_header = ['table_header_cell']
		self.order_table_header_cell = list(self.order_inline)

		self.order_table_body = ['table_body_row']
		self.order_table_body_row = ['table_body_cell']
		self.order_table_body_cell = list(self.order_inline)

		# new line
		self.order_new_line = list(self.order_inline)
		self.order_simple_new_line = list(self.order_inline)

		# styles
		try:
			self.order_code_inline = []
			self.order_link = list(self.order_inline)
			self.order_link.remove('link')
			self.order_link.remove('image')
			self.order_link.remove('code_inline')
			self.order_link.remove('escape_backslash')
			self.order_bold = list(self.order_link)
			self.order_bold.remove('bold')
			self.order_bold.remove('bold')
			self.order_italic = list(self.order_bold)
			self.order_italic.remove('italic')
			self.order_underline = list(self.order_italic)
			self.order_underline.remove('underline')
			self.order_strike = list(self.order_underline)
			self.order_strike.remove('strike')

		except ValueError:
			pass

		# Define order initial.
		self.order_initial = self.order_block + self.order_inline

	# Parse functions
	def parse_fenced_code(self, mo):
		lang = mo.group('lang')
		title = mo.group('title')
		code = mo.group('code').replace('\`', '`')
		return Token('fenced_code', extras={'code': code, 'lang': lang, 'title': title})

	def parse_break_line(self, mo):
		sym = mo.group(0)[0]
		return Token('break_line', extras={'symbol': sym})

	def parse_header(self, mo):
		text = mo.group('text')
		level = len(mo.group('level'))
		return Token('header', text, extras={'level': level}, order=self.order_header)

	def parse_header2(self, mo):
		text = mo.group('text')
		sym = mo.group('sym')[0]

		if sym == '=':
			level = 1
		elif sym == '-':
			level = 2
		else:
			level = 3
		return Token('header', text, extras={'level': level}, order=self.order_header)

	def parse_olist(self, mo):
		start = mo.group('start')
		l = mo.group('list').strip()
		return Token('olist', l, extras={'start': int(start)}, order=self.order_olist)

	def parse_olist_item(self, mo):
		item = mo.group('item').strip()
		return Token('olist_item', item, order=self.order_olist_item)

	def parse_osublist(self, mo):
		start = mo.group('start')
		l = mo.group('list')
		return Token('olist', l, extras={'start': int(start)}, order=self.order_subolist)

	def parse_new_line(self, mo):
		text = mo.group('text').strip()
		return Token('new_line', text, order=self.order_new_line)

	def parse_simple_new_line(self, mo):
		text = mo.group('text').strip()
		return Token('new_line', text, order=self.order_simple_new_line)

	def parse_ulist(self, mo):
		start = mo.group('start')
		l = mo.group('list').strip()
		return [Token('ulist', l, extras={'start': start}, order=self.order_ulist), '\n']

	def parse_ulist_item(self, mo):
		item = mo.group('item')
		return Token('ulist_item', item, order=self.order_ulist_item)

	def parse_usublist(self, mo):
		start = mo.group('start')
		l = mo.group('list')
		return Token('ulist', l, extras={'start': start}, order=self.order_subulist)

	def parse_escape_backslash(self, mo):
		char = mo.group('char')
		# check if the char is a character escaped
		if char in self.escape_chars:
			return Token('escape_backslash', mo.group('char'))

		return '\\' + char

	def parse_blockquote(self, mo):
		blockquote = mo.group('blockquote')
		blockquote = '\n'.join([l.strip()[2:] for l in blockquote.split('\n')])
		return [Token('blockquote', blockquote, order=self.order_blockquote), '\n']

	def parse_bold(self, mo):
		return Token('bold', mo.group('text'), order=self.order_bold)

	def parse_italic(self, mo):
		return Token('italic', mo.group('text'), order=self.order_italic)

	def parse_underline(self, mo):
		return Token('underline', mo.group('text'), order=self.order_underline)

	def parse_strike(self, mo):
		return Token('strike', mo.group('text'), order=self.order_strike)

	def parse_code_inline(self, mo):
		return Token('code_inline', extras=mo.groupdict(), order=self.order_code_inline)

	def parse_image(self, mo):
		extras = mo.groupdict()
		del extras['quote']
		return Token('image', extras=extras)

	def parse_link(self, mo):
		text = mo.group('text')
		extras = {'title': mo.group('title'), 'href': mo.group('href')}
		return Token('link', text, extras, order=self.order_link)

	def parse_table(self, mo):
		return Token('table', mo.group('table').strip(), order=self.order_table)

	def parse_table_header(self, mo):
		return Token('table_header', mo.group('head'), order=self.order_table_header)

	def parse_table_header_cell(self, mo):
		cells = [cell.strip() for cell in mo.group('cells').split('|')][1:]
		cells_token = []

		for cell in cells:
			cells_token.append(Token('table_header_cell', cell, order=self.order_table_header_cell))

		return cells_token

	def parse_table_body(self, mo):
		align = [a.strip() for a in mo.group('align').split('|')][1:]
		align_token = []
		for a in align:
			if a.startswith(':') and a.endswith(':'):
				align_token.append('center')

			elif a.endswith(':'):
				align_token.append('right')
			else:
				align_token.append('left')

		body = mo.group('body')

		return Token('table_body', body, order=self.order_table_body, extras_to_children={'align': align_token})

	def parse_table_body_row(self, mo, align):
		return Token(
			'table_body_row', mo.group('row').strip(), order=self.order_table_body_row,
			extras_to_children={'align': align}
		)

	def parse_table_body_cell(self, mo, align):
		cells = [cell.strip() for cell in mo.group('cells').split('|')][1:]
		cells_token = []

		for i, cell in enumerate(cells):
			cells_token.append(Token(
				'table_body_cell', cell, order=self.order_table_body_cell,
				extras={'align': align[i]}
			))

		return cells_token

	def parse_footnotes(self, text):
		all_footnotes = {}

		# Get all foot notes
		def store_footnotes(mo):
			ind = mo.group('ind')

			if not ind:
				# footnote of one line
				value = mo.group('value')

			else:
				# footnote of some lines
				lines = mo.group('value').split('\n')
				indl = len(ind)  # indent length
				value_start = lines[0]
				del lines[0]

				# Get the rest of lines deleting the indent previously.
				value_rest = '\n'.join([l[indl:] for l in lines])
				value = '%s\n%s' % (value_start, value_rest)  # Make the value

			all_footnotes[mo.group('name')] = value
			return ''

		text = self.regex_footnotes.sub(store_footnotes, text)

		def replace_footnotes(mo):
			name = mo.group('name')
			return all_footnotes.get(name, '[^%s]' % name)

		for key, value in all_footnotes.items():
			all_footnotes[key] = self.regex_apply_footnotes.sub(replace_footnotes, value)

		text = self.regex_apply_footnotes.sub(replace_footnotes, text)
		return text

	# Other functions
	def get_main_token(self, text):
		return Token('_only_text', text, order=self.order_initial)

	def pre_process_text(self, text):
		""" Process the text before be rendered.

			:param str text: Markdown text.
			:return str: text post processed.
		"""
		text = text.replace('\r\n', '\n').replace('\r', '\n').expandtabs(self.tab_size)
		return '\n' + text + '\n\n'
