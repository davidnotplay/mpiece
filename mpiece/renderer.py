"""
	mpiece.renderer
	~~~~~~~~~~~~~~~~~~~~~~~~~

	Renderer Classes.

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""


class Renderer(object):
	"""
		Base renderer class.
		All renderer classes should be subclasses of this class.

		This class and their subclass are used in the ``__init__.markdown()`` function or
		in the ``MPiece.parse()`` method.

	"""

	def __init__(self):
		self.all_render_funcs = {}

		for item in dir(self):
			if item.startswith('render_'):
				self.all_render_funcs[item[7:]] = getattr(self, item)

	def render__only_text(self, text):
		return text


class HtmlRendererBase(Renderer):
	"""
		Transform the lexer tokens in html code.
		:param bool use_underline:
				- True: The markdown `_text_` will transform in `<ins>text</ins>`
				- False The markdown `_text_` will transform in  `<em>text</em>`
			Default True.

		:param bool use_paragraph:
				- True: The break line in the markdown text will transform in <p></p> html tag.
				- False: Thre break line in the markdown text will transform in <br> html tag.
			Default True.

		:param bool escape_html:
				- True: Escape the html tag in the markdown text.
				- False: No escape the html tag in the markdown text.
			Default True.
	"""

	# link scheme blacklist
	scheme_blacklist = ('javascript', 'data', 'vbscript')

	def __init__(self, use_underline=True, use_paragraph=True, escape_html=True):
		super(HtmlRendererBase, self).__init__()
		self.use_underline = use_underline
		self.use_paragraph = use_paragraph
		self.escape_html = escape_html

	def escape(self, text):
		""" Escape html characters.
			:param str text:
			:return: text escaped.

		"""
		if not self.escape_html or text is None:
			return text

		return (
			text.replace('&', '&amp;').replace('<', '&lt;')
			.replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
		)

	def escape_args(self, *args):
		""" Escape html characters of all arguments
			:param [str] *args:

			:return: list of all arguments escaped.
		"""
		return tuple((self.escape(arg) for arg in args))

	def escape_link(self, link, smart_amp=True):
		"""	Check if a link has an invalid scheme.
			Also transform the `&`character in `&amp; character.

			:param str link: Link checked.
			:param bool smart_amp: Transform the '&' characters in '&amp;' characters.
			:return: Return the link if the scheme is valid. If not return an empty string. Default True.
		"""
		data = link.split(':', 1)
		scheme = data[0]
		if scheme in self.scheme_blacklist:
			return ''

		if smart_amp:
			return link.replace('&', '&amp;')

		return link

	#
	# Render functions
	#
	def render_bold(self, text):
		return '<strong>%s</strong>' % self.escape(text)

	def render_italic(self, text):
		return '<em>%s</em>' % self.escape(text)

	def render_underline(self, text):
		if self.use_underline:
			return '<ins>%s</ins>' % self.escape(text)
		else:
			return self.use_italic(text)

	def render_strike(self, text):
		return '<del>%s</del>' % self.escape(text)

	def render_code_inline(self, code):
		return '<code>%s</code>' % self.escape(code)

	def render_link(self, text, href, title):
		text = self.escape(text)
		href = self.escape_link(href)

		if title:
			return '<a href="%s" title="%s">%s</a>' % (href, self.escape(title), text)

		return '<a href="%s">%s</a>' % (href, text)

	def render_image(self, src, alt, title):
		alt = self.escape(alt)
		src = self.escape_link(src)
		if title:
			title = self.escape(title)
			return '<img src="%s" alt="%s" title="%s">' % (src, alt, title)

		return '<img src="%s" alt="%s">' % (src, alt)

	def render_new_line(self, text):
		if self.use_paragraph:
			return '<p>%s</p>' % self.escape(text) if text else ''
		else:
			return '%s<br/>' % self.escape(text) if text else ''

	def render_olist(self, text, start):
		text, start = self.escape_args(text, start)
		return '<ol start="%s">%s</ol>' % (start, text)

	def render_olist_item(self, text):
		return '<li>%s</li>' % self.escape(text)

	def render_ulist(self, text, start):
		return '<ul>%s</ul>' % self.escape(text)

	def render_ulist_item(self, text):
		return '<li>%s</li>' % self.escape(text)

	def render_blockquote(self, text):
		return '<blockquote>%s</blockquote>' % self.escape(text)

	def render_header(self, text, level):
		return '<h{level}>{text}</h{level}>'.format(level=level, text=self.escape(text))

	def render_code(self, code, lang, title):
		lang, title, code = self.escape_args(lang, title, code)

		if lang and title:
			title = 'Code %s: %s' % (lang, title)
		elif lang:
			title = 'Code %s' % lang
		elif title:
			title = 'Code: %s' % title
		else:
			title = 'Code'

		return '<div>%s<pre>%s</pre></div>' % (title, code)

	def render_break_line(self, symbol):
		return '<hr/>'


class HtmlRendererTable(HtmlRendererBase):
	""" Transform the table tokens in html code.
	"""

	def render_table(self, text):
		return '<table>%s</table>' % text

	def render_table_header(self, text):
		return '<thead><tr>%s</tr></thead>' % text

	def render_table_header_cell(self, text):
		return '<th>%s</th>' % text

	def render_table_body(self, text):
		return '<tbody>%s</tbody>' % text

	def render_table_body_row(self, text):
		return '<tr>%s</tr>' % text

	def render_table_body_cell(self, text, align=''):
		if align and align != 'left':
			return '<td style="text-align:%s;">%s</td>' % (align, text)
		else:
			return '<td>%s</td>' % text


class HtmlRenderer(HtmlRendererTable):
	pass
