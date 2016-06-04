"""
	mpiece.lexer
	~~~~~~~~~~~~~~~

	Lexer classes.

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""

import re
from mpiece.markdown import Token


class LexerBase(object):
	"""
		Converts the markdown text in tokens.
		All lexer classes should be subclasses of this class.

		This class and their subclass are used in the ``__init__.markdown()`` function or
		in the ``MPiece.parse()`` method.

		:param set exclude: The markdown tags name which you want exclude in the markdown text.
		:param int tab_size: Tabulators size. Default is 4.
		:param str escape_chars:
			Characters escaped if they have the have the `\` character before. This string is added
			to the characters `*~`_[]()\\`
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
	regex_olist = re.compile(r'(?P<list>^(?P<start>[0-9]+)\.[ ].*?)\n(?=\n|$)', re.S | re.M)
	regex_olist_item = re.compile(
		r'^(?P<iden>[ ]*)[0-9]+\.[ ](?P<item>.*?(?:\n|$)(?:(?P=iden)(?![0-9]+\.).*?(?:\n|$))*)',
		re.M
	)
	regex_osublist = re.compile(r'^(?P<list>(?P<iden>[ ]+)(?P<start>[0-9]+)\.[ ](?:.*\n(?=(?P=iden)))*[^\n]+)', re.M)
	regex_ulist = re.compile(r'(?P<list>^(?P<start>[*-])[ ].*?)\n(?=\n|$)', re.S | re.M)
	regex_ulist_item = re.compile(r'^(?P<iden>[ ]*)[*-][ ](?P<item>.*?(?:\n|$)(?:(?P=iden)(?![*-]).*?(?:\n|$))*)', re.M)
	regex_usublist = re.compile(r'^(?P<list>(?P<iden>[ ]+)(?P<start>[*-])[ ](?:.*\n(?=(?P=iden)))*[^\n]+)', re.M)
	regex_blockquote = re.compile(r'(?P<blockquote>^(?:[ ]*\>[^\n]*\n?)+)', re.M)
	regex_header = re.compile(r'^[ ]*(?P<level>#+) (?P<text>.*?)(?:[ ](?P=level))?$', re.M)
	regex_header2 = re.compile(r'^(?P<text>[^\n]+)\n(?P<sym>[\-=]{3,})$', re.M)
	regex_code = re.compile(
		r'[ ]*`{3}[ ]*(?P<lang>[^\n"]+?)?(?: ?(?!\\)"(?P<title>[^\n]+)(?!\\)")?\n(?P<code>.*?)\n[ ]*`{3}',
		re.S
	)
	regex_break_line = re.compile(r'^([*\-_]{3,})$', re.M)
	regex_footnotes = re.compile(
		r'^\[\^(?P<name>.+)\]:[ ]*(?P<value>[^\n]*(?=\n)(?:\n(?P<ind>[ ]+)[^\n]*(?=\n))?(?:\n(?P=ind)[^\n]*(?=\n))*)',
		re.M
	)
	regex_apply_footnotes = re.compile(r'\[\^(?P<name>.+)\]')

	# main orders
	order_block = ['code', 'ulist', 'olist', 'blockquote', 'header', 'header2', 'break_line', 'new_line']
	order_inline = ['image', 'link', 'code_inline', 'bold', 'italic', 'bold', 'underline', 'strike']

	# other variables
	escape_chars = '*~`_[]()\\'

	def __init__(self, exclude=set(), tab_size=4, escape_chars=''):
		self.tab_size = tab_size
		self.escape_chars += escape_chars
		self.exclude = getattr(self, 'exclude', set()) | exclude

		self.all_regex = {}
		self.all_parse_func = {}
		for item in dir(self):
			if item.startswith('regex_'):
				self.all_regex[item[6:]] = getattr(self, item)

			if item.startswith('parse_'):
				self.all_parse_func[item[6:]] = getattr(self, item)

		self.define_order()

	def define_order(self):
		# list
		self.order_ulist = ['ulist_item']
		self.order_subulist = ['ulist_item']
		self.order_ulist_item = list(self.order_block)
		try:
			# Replace u/olist to u/osublist
			self.order_ulist_item[self.order_ulist_item.index('ulist')] = 'usublist'
			self.order_ulist_item[self.order_ulist_item.index('olist')] = 'osublist'
		except ValueError:
			# ulist or/and olist are excluded and they don't exists in order_block list.
			pass

		self.order_olist = ['olist_item']
		self.order_subolist = ['olist_item']
		self.order_olist_item = list(self.order_ulist_item)

		# Blockquote
		self.order_blockquote = list(self.order_block)

		# header
		self.order_header = list(self.order_inline)
		self.order_header.remove('image')

		# new line
		self.order_new_line = list(self.order_inline)

		# styles
		try:
			self.order_link = list(self.order_inline)
			self.order_bold = list(self.order_inline)
			self.order_bold.remove('bold')
			self.order_italic = list(self.order_inline)
			self.order_italic.remove('italic')
			self.order_underline = list(self.order_inline)
			self.order_underline.remove('underline')
			self.order_strike = list(self.order_inline)
			self.order_strike.remove('strike')
		except ValueError:
			pass

		# initial order
		self.order_initial = ['escape_backslash'] + self.order_block

	# Parse functions
	def parse_code(self, mo):
		lang = mo.group('lang')
		title = mo.group('title')
		code = mo.group('code')
		return Token('code', extras={'code': code, 'lang': lang, 'title': title})

	def parse_break_line(self, mo):
		sym = mo.group(0)[0]
		return Token('break_line', extras={'symbol': sym})

	def parse_header(self, mo):
		text = mo.group('text')
		level = len(mo.group('level'))
		return Token('header', text, extras={'level': level}, order=self.order_header)

	def parse_header2(self, mo):
		text = mo.group('text')
		level = 1 if mo.group('sym').startswith('=') else 2
		return Token('header', text, extras={'level': level}, order=self.order_header)

	def parse_olist(self, mo):
		start = mo.group('start')
		l = mo.group('list').strip()
		return Token('olist', l, extras={'start': start}, order=self.order_olist)

	def parse_olist_item(self, mo):
		item = mo.group('item').strip()
		return Token('olist_item', item, order=self.order_olist_item)

	def parse_osublist(self, mo):
		start = mo.group('start')
		l = mo.group('list')
		return Token('olist', l, extras={'start': start}, order=self.order_subolist)

	def parse_new_line(self, mo):
		text = mo.group('text').strip()
		if text == '':
			return text

		return Token('new_line', text, order=self.order_new_line)

	def parse_ulist(self, mo):
		start = mo.group('start')
		l = mo.group('list').strip()
		return Token('ulist', l, extras={'start': start}, order=self.order_ulist)

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
			return Token('_only_text', mo.group('char'))

		return '\\' + char

	def parse_blockquote(self, mo):
		blockquote = mo.group('blockquote')
		blockquote = '\n'.join([l.strip()[2:] for l in blockquote.split('\n')])
		return Token('blockquote', blockquote, order=self.order_blockquote)

	def parse_bold(self, mo):
		return Token('bold', mo.group('text'), order=self.order_bold)

	def parse_italic(self, mo):
		return Token('italic', mo.group('text'), order=self.order_italic)

	def parse_underline(self, mo):
		return Token('underline', mo.group('text'), order=self.order_underline)

	def parse_strike(self, mo):
		return Token('strike', mo.group('text'), order=self.order_strike)

	def parse_code_inline(self, mo):
		return Token('code_inline', extras=mo.groupdict())

	def parse_image(self, mo):
		extras = mo.groupdict()
		del extras['quote']
		return Token('image', extras=extras)

	def parse_link(self, mo):
		text = mo.group('text')
		extras = {'title': mo.group('title'), 'href': mo.group('href')}
		return Token('link', text, extras, order=self.order_link)

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
		text = text.replace('\r\n', '\n').replace('\r', '\n').expandtabs(self.tab_size)
		return '\n' + text + '\n\n'

	def post_process_text(self, text):
		return text.strip()


class LexerTable(LexerBase):
	""" Allows table tags in the markdown text.


		Example of Markdown table tag:

		| table head1 | table head2 | table head3 |
		| :---------- | :---------: | ----------: | <-- NOTE: Align col1 left, align col2 center, align col3 right
		| table cell1 | table cell2 | table cell3 |
		| table cell1 | table cell2 | table cell3 |

	"""
	regex_table = re.compile(r'(?<=\n)(?P<table>\|[^\n]*\n\|[ \|\-:]+\n(?:\|[^\n]+\n?)*)(?=\n|$)', re.S)
	regex_table_header = re.compile(r'^(?P<head>\|[^\n]+)')
	regex_table_header_cell = re.compile(r'^(?P<cells>\|[^\n]+?)\|?$')

	regex_table_body = re.compile(r'^^(?P<align>[| \-:]+?)\|?\n(?P<body>.*)', re.S | re.M)
	regex_table_body_row = re.compile(r'^(?P<row>\|[^\n]+)', re.M)
	regex_table_body_cell = re.compile(r'^(?P<cells>\|[^\n]+?)\|?$')

	def define_order(self):
		self.order_block.insert(1, 'table')
		super(LexerTable, self).define_order()

		self.order_table = ['table_header', 'table_body']
		self.order_table_header = ['table_header_cell']
		self.order_table_header_cell = list(self.order_inline)

		self.order_table_body = ['table_body_row']
		self.order_table_body_row = ['table_body_cell']
		self.order_table_body_cell = list(self.order_inline)

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


class Lexer(LexerTable):
	"""	Default lexer. it use in the  ``__init__.markdown()`` function or ``MPiece().parse()``
	"""
	pass
