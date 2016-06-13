Modify output
=============

You can modify the output of the markdown text making a renderer subclass.

List of renderer methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a list of methods for a renderer class, all this methods are necessary to the ``mpiece.lexer.Lexer``
class runs correctly. Depending of the lexer object, the renderer methods maybe change.

- ``render_bold(str text)``
- ``render_italic(str text)``
- ``render_underline(str text)``
- ``render_strike(str text)``
- ``render_code_inline(str text)``
- ``render_link(str text, str href, str title='')``
- ``render_image(self, src, alt, str title='')``
- ``render_new_line(str text)``
- ``render_olist(str text, int start)``
- ``render_olist_item(str text)``
- ``render_ulist(str text, str start)``
- ``render_blockquote(str text)``
- ``render_header(str text, int level)``
- ``render_fenced_code(str code, str lang='', str title='')``
- ``render_break_line(str symbol)``
- ``render_table(str text)``
- ``render_table_header(str text)``
- ``render_table_header_cell(str text)``
- ``render_table_body(str text)``
- ``render_table_body_row(str text)``
- ``render_table_body_cell(str text, str align='')``



Usage examples
--------------

Make new subclass of :class:`HtmlRenderers` to converts the ``**text**`` markdown and ``_text_`` markdown in custom html code.

.. code:: python

    from mpiece.renderer import HtmlRenderer
    from mpiece import markdown

    class CustomHtmlRenderer(HtmlRenderer):

        def render_bold(self, text):
            return '<strong class="custom-class">%s</text>' % self.escape(text)

        def render_underline(self, text):
            # self.use_underline is an attribute to decide if the ``_text_``
            # grammar will converts in underline or italic
            if self.use_underline:
                return '<ins class="custom-class">%s</ins>' % self.escape(text)

            else:
            # self.use_underline is False. ``_text_`` will be a italic text.
                return self.render_italic(text)


    renderer = CustomHtmlRenderer()
    text_md = '**bold text** and _underline text_'

    result = markdown(text_md, renderer=renderer)
    print(result)
    # output: <p><strong class="custom-class">bold text</strong> and <ins class="custom-class>underline_text</ins></p>


Rendering the lists and images.

.. code:: python

    from mpiece.renderer import HtmlRenderer
    from mpiece import markdown

    class CustomHtmlRenderer(HtmlRenderer):

    	def render_ulist(self, text, start):
            cssclass = 'class-a' if start == '*' else 'class-b'
            return '<ul class="%s">%s</ul>' % (cssclass, self.escape(text))

        def render_ulist_item(self, text):
            return '<li class="li-item">%s</li>' % self.escape(text)

        def render_olist(self, text, start):
            return '<ol start="%d" class="c-class">%s</ol>' % (start, self.escape(text))

        def render_olist_item(self, text):
            return '<li class="li-item">%s</li>' % self.escape(text)

        def render_image(self, src, alt, title=''):
            src = self.escape_link(src)
            alt, title = self.escape_args(alt, title)

            return '<span class="image"><img src="%s" alt="%s" title="%s"></span>' %( src, alt, title)


    text_md = """

    - item 1
    - item 2
    - item 3
      continue item 
    
      new line item 3 ![image](src)
    
    1. item 1
    2. item 2
    """
    
    renderer = CustomHtmlRenderer()
    result = markdown(text_md, renderer=renderer)
    
    print(result)
    
    """
    output: 

    <ul class="class-b"><li class="li-item"><p>item 1</p>
    </li><li class="li-item"><p>item 2</p>
    </li><li class="li-item"><p>item 3</p>
    <p>continue item</p>
    <p>new line item 3 <span class="image"><img src="src" alt="image" title="None"></span></p></li></ul>
    <ol start="1" class="c-class"><li class="li-item"><p>item 1</p></li><li class="li-item"><p>item 2</p></li></ol>
    """


Make new subclass for use pygmentize package in the fenced code markdown.

.. code:: python

    from mpiece.renderer import HtmlRenderer
    from mpiece import markdown

    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import html

    class CodeHtmlRenderer(HtmlRenderer):
 
    def render_code(self, code, lang='', title=''):

           if not lang:
            return '<pre>%s</pre>' % self.escape(code)

        # Using pygmentize to parser code
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)

.. warning::

    If you want modify the html code output. **You should be escape the html characters in the text.**
    You can use :func:`HtmlRenderer.escape()` and :func:`HtmlRenderer.escape_args()` methods.

    Also you should escape the image and links urls to avoid dangerous schemes: ``data``, ``javasript``, ``vbscript``. You can use ``HtmlRenderer.escape_link()`` method for this task.
