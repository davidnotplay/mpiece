Make markdown Grammar
=====================

Token
-----

.. autoclass:: mpiece.lexer.Token

Grammar order
-------------

This diagram show the order of the lexer to time parse the markdown grammar.
It is important if you want add new grammar.

.. image:: _static/main_order.png
	:alt: main_order
	:target: _static/main_order.png


:class:`mpiece.lexer.Lexer` has 3 main order attrs:
    - :attr:`mpiece.lexer.Lexer.order_block`
    - :attr:`mpiece.lexer.Lexer.order_inline`
    - :attr:`mpiece.lexer.Lexer.order_initial`

When you make a new grammar you should modify the one of this attributes for add the new grammar to the lexer.


Setps to make a new grammar
---------------------------

To make new grammar for our markdown lexer is necessary 5 steps:

	1. Define a unique name.
	2. Make a regular expression.
	3. Make a parser function in our lexer class.
	4. Define the order of our grammar in the lexer class.
	5. Make a render function in our Renderer class.

Make new grammar. Example 1
---------------------------

Objective
~~~~~~~~~
Make a markdown grammar to change the color in a text string.

.. code::

	Normal string. #f00 String with different color.##
	Normal string.
	#0000dd Another string with different color.##
	#1b70b0 **bold text**, *italic text*, _underline text_, ~strike text~, `no code inline text`.##


This markdown text will transform in

.. code:: html

	<p>
		Normal string. <span style="color:#f00">String with different color.</span> Normal string.
		<span style="color:#0000dd">Another string with different color.</span>
		<span style="color:#1b70b0">
			<strong>bold text</strong>, <em>italic text</em>, <ins>underline text</ins>, <del>strike text</del>,
			`no code inline text`
		</span>
	</p>

1. Define a name
~~~~~~~~~~~~~~~~

The name for this examples is ``color``

2. Make the regular expression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The regular expression for the `color grammar`

.. code::
	
	#(?P<color>[0-9a-fA-F]{3}|[0-9a-fA-F]{6}) (?P<text>.+?)##


Making a custom lexer class and add the regular expression.

.. code:: python

    from mpiece.lexer import Lexer
    import re

    class CustomLexer(Lexer):
        # The regular expression
        regex_color = re.compile(r'#(?P<color>[0-9a-fA-F]{3}|[0-9a-fA-F]{6}) (?P<text>.+?)##')

The name of the regular expression in the lexer class should be ``regex_`` prefix + the name selected. In this
case ``regex_color``


3. Make the parse function
~~~~~~~~~~~~~~~~~~~~~~~~~~

The parse function process the result of the python function ``re.sub`` in our regular expression.

.. code:: python

    from mpiece.lexer import Lexer, Token
    import re

    class CustomLexer(Lexer):
        # The regular expression
        regex_color = re.compile(r'#(?P<color>[0-9a-fA-F]{3}|[0-9a-fA-F]{6}) (?P<text>.+?)##')

        def parse_color(self, mo):
            """ mo is a python Match object.
            	mo is the result of ``re.sub`` using the regular expression ``regex_color``.

            	This parse function always should return:
            		- Token object
            		- string
            		- List|tuple of objects and/or strings.
            """
            color = mo.group('color')
            text = mo.group('text')
            order = ['bold', 'italic', 'underline', 'strike']

            # 'color': Is the name of the render function witouth the prefix ``render_``
            # text: The text obtained in the color grammar. This text will be re-parsed to finding more markdown grammar.
            # extras: Extra arguments for the render function.
            # order: Grammar elements which the lexer will search inside of the text.
            return Token('color', text, extras={'color': color}, order=order)


In the example the text inside of the color grammar will be re-parsed finding the grammar of the variable ``order``. The parse function name should be ``parse_`` prefix + the name selected. In this case ``parse_color``.

4. Define order
~~~~~~~~~~~~~~~

Define the order using the function ``Lexer.define_order()`` method.

.. code:: python

    from mpiece.lexer import Lexer, Token
    import re

    class CustomLexer(Lexer):
        # The regular expression
        regex_color = re.compile(r'#(?P<color>[0-9a-fA-F]{3}|[0-9a-fA-F]{6}) (?P<text>.+?)##')

        # Define the order and insert the color grammar.
        def define_order(self):
        	# add color grammar to the ``order_inline`` variable.
        	# it is important doing before to call the father function.
    	    self.order_inline.insert(1, 'color')
    	    # call the father function.
    	    super(CustomLexer, self).define_order()

        def parse_color(self, mo):
            """ mo is a python Match object.
            	mo is the result of ``re.sub`` using the regular expression ``regex_color``.

            	This parse function always should return:
            		- Token object
            		- string
            		- List|tuple of objects and/or strings.
            """
            color = mo.group('color')
            text = mo.group('text')
            order = ['bold', 'italic', 'underline', 'strike']

            # 'color': Is the name of the render function witouth the prefix ``render_``
            # text: The text obtained in the color grammar. This text will be re-parsed to finding more markdown grammar.
            # extras: Extra arguments for the render function.
            # order: Grammar elements which the lexer will search inside of the text.
            return Token('color', text, extras={'color': color}, order=order)




5. Make renderer function
~~~~~~~~~~~~~~~~~~~~~~~~~~

We want convert the markdown text in html code, so, we will use the ``HtmlRenderer`` class as the father of our renderer class.

.. code:: python

    from mpiece.lexer import Lexer, Token
    from mpiece.renderer import HtmlRenderer
    import re

    class CustomLexer(Lexer):
        # The regular expression
        regex_color = re.compile(r'#(?P<color>[0-9a-fA-F]{3}|[0-9a-fA-F]{6}) (?P<text>.+?)##')

        # Define the order and insert the color grammar.
        def define_order(self):
        	# add color grammar to the ``order_inline`` variable.
        	# it is important doing before to call the father function.
    	    self.order_inline.insert(1, 'color')
    	    # call the father function.
    	    super(CustomLexer, self).define_order()

        def parse_color(self, mo):
            """ mo is a python Match object.
            	mo is the result of ``re.sub`` using the regular expression ``regex_color``.

            	The parse function always should return:
            		- Token object
            		- string
            		- List|tuple of objects and/or strings.
            """
            color = mo.group('color')
            text = mo.group('text')
            order = ['bold', 'italic', 'underline', 'strike']

            # 'color': Is the name of the render function witouth the prefix ``render_``
            # text: The text obtained in the color grammar. This text will be re-parsed to finding more markdown grammar.
            # extras: Extra arguments for the render function.
            # order: Grammar elements which the lexer will search inside of the text.
            return Token('color', text, extras={'color': color}, order=order)

    class CustomRenderer(HtmlRenderer):

    	# Render function for the color grammar.
    	def render_color(self, text, color):
    		# convert html characters
    		text = self.escape(text)
    		return '<span class="color:#%s">%s</span>' % (color, text)


With this code, the example is complete. Now you can use this new lexer and renderer to convert markdown text in html
code.

Make new grammar example 2
--------------------------

Objective
~~~~~~~~~
Add emojis in the markdown text.

.. code:: text
	
	Markdown text :emoji1: continue :XD: continue :not_exists: end.

.. code:: html

    <p>
        Markdown text <span class="css-emoji1"></span> continue <span class="emojis-emoji-smiley"></span>
       :not_exists: end.
    </p>



1. Define a name
~~~~~~~~~~~~~~~~

The name for this examples is ``emojis``

2. Make the regular expression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The regular expression for this example:

.. code:: 
	
    :(?P<emoji>[a-zA-Z0-9_]+):


Now starting making the lexer.

.. code:: python

    from mpiece.lexer import Lexer
    import re


    class EmojiLexer(Lexer):
        regex_emojis = re.compile(r':(?P<emoji>[a-zA-Z0-9_]+):')


3. Make the parse function
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from mpiece.lexer import Lexer, Token
    import re


    class EmojiLexer(Lexer):
        # emoji list
        emoji_list = {
            'emoji1': 'css-emoji1',
            'XD': 'emojis-emoji-smiley'
        }


        regex_emojis = re.compile(r':(?P<emoji>[a-zA-Z0-9_]+):')

        def parse_emojis(self, mo):
            emoji = mo.group('emoji')
            emoji_css = self.emoji_list.get(emoji, False)
            
            # check if the emoji exists
            if not emoji_css:
            	# emoji doesn't exits. return the same string
            	return ':%s:' % emoji

            # emoji exists
            return Token(extras={'emoji_css_class': emoji_css}, order=[])

4. Define order
~~~~~~~~~~~~~~~

Emoji grammar is added to the end of order_inline.

.. code:: python

    from mpiece.lexer import Lexer, Token
    import re


    class EmojiLexer(Lexer):
        # emoji list
        emoji_list = {
            'emoji1': 'css-emoji1',
            'XD': 'emojis-emoji-smiley'
        }


        regex_emojis = re.compile(r':(?P<emoji>[a-zA-Z0-9_]+):')

        def define_order(self):
            self.order_inline.append('emojis')
            super(EmojiLexer, self).define_order()

        def parse_emojis(self, mo):
            emoji = mo.group('emoji')
            emoji_css = self.emoji_list.get(emoji, False)
            
            # check if the emoji exists
            if not emoji_css:
            	# emoji doesn't exits. return the same string
            	return ':%s:' % emoji

            # emoji exists
            return Token(extras={'emoji_css_class': emoji_css}, order=[])


5. Make renderer function
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from mpiece.lexer import Lexer, Token
    from mpiece.renderer import HtmlRenderer
    import re


    class EmojiLexer(Lexer):
        # Private attribute.
        # list with all emojis and his css class
        emoji_list = {
        	'emoji1': 'css-emoji1',
        	'XD': 'emojis-emoji-smiley'
        }

        regex_emojis = re.compile(r':(?P<emoji>[a-zA-Z0-9_]+):')

        def define_order(self):
            self.order_inline.append('emojis')
            super(EmojiLexer, self).define_order()

        def parse_emojis(self, mo):
            emoji = mo.group('emoji')
            emoji_css = self.emoji_list.get(emoji, False)
            
            # check if the emoji exists
            if not emoji_css:
                # emoji doesn't exits. return the same string
                return ':%s:' % emoji

            # emoji exists
            return Token('emojis', extras={'emoji_css_class': emoji_css}, order=[])


    class EmojiRenderer(HtmlRenderer):
        def render_emojis(self, emoji_css_class):
            return '<span class="%s"></span>' % emoji_css_class

    
