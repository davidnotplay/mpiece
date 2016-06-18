Lexers
======

The lexers define the markdown grammar.

Usage
-----

There are two ways to add a lexer class:

.. code:: python

	from mpiece.lexer import Lexer
	from mpiece import markdown

	text_md="**Hello world!!!**"

	result = markdown(text, lexer=Lexer())

	#output <p><strong>Hello world!!!</strong></p>

or 

.. code:: python

	from mpiece.lexer import Lexer
	from mpiece import Markdown

	text_md="**Hello world!!!**"

	markdown = Markdown()
	markdown.lexer = Lexer()
	result = markdown(text, lexer=lexer)

	#output <p><strong>Hello world!!!</strong></p>


Lexers list
-----------

.. autoclass:: mpiece.lexer.Lexer
	:members: define_order, pre_process_text

