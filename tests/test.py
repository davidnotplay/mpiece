"""
	Test classes

	:license: BSD, see LICENSE for details.
	:author: David Casado Martinez <dcasadomartinez@gmail.com>
"""


import os
import unittest
from mpiece import markdown, Lexer, HtmlRenderer
import re

no_space = re.compile('\s+')


class MdaTest(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None
		self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

	def get_file_text(self, filename):
		with open(os.path.join(self.test_dir, filename), 'r') as f:
			content = f.read()

		return content

	def transform_text(self, text):
		return (
			re.sub('\s+', ' ', text)
			.replace('> ', '>')
			.replace(' <', '<')
			.strip()
		)

	def compare(self, html_filename, md_filename, lexer=None, renderer=None):
		html = self.get_file_text(html_filename)

		text = self.get_file_text(md_filename)

		lexer = lexer or Lexer()
		renderer = renderer or HtmlRenderer()
		text = markdown(text, lexer=lexer, renderer=renderer)

		html = self.transform_text(html)
		text = self.transform_text(text)
		self.assertEqual(text, html)

	def test_styles(self):
		self.compare('test_styles.html', 'test_styles.md')

	def test_blockquote(self):
		self.compare('test_blockquote.html', 'test_blockquote.md')

	def test_code(self):
		self.compare('test_code.html', 'test_code.md')

	def test_footnotes(self):
		self.compare('test_footnotes.html', 'test_footnotes.md')

	def test_header(self):
		self.compare('test_header.html', 'test_header.md')

	def test_link_and_images(self):
		self.compare('test_links_and_images.html', 'test_links_and_images.md')

	def test_list(self):
		self.compare('test_list.html', 'test_list.md')

	def test_exclude(self):
		lexer = Lexer(exclude={'ulist', 'link'})
		self.compare('test_exclude.html', 'test_exclude.md', lexer=lexer)

	def test_table(self):
		self.compare('test_table.html', 'test_table.md')

	def test_escape(self):
		self.compare('test_escape.html', 'test_escape.md')

	def test_no_escape(self):
		renderer = HtmlRenderer(escape_html=False)
		self.compare('test_no_escape.html', 'test_no_escape.md', renderer=renderer)
