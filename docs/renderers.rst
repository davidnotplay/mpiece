Renderers
=========

The renderers define the output of the markdown text.

Usage
-----

There are two ways to add a renderer:


.. code:: python

	from mpiece.renderer import HtmlRenderer
	from mpiece import markdown

	class CustomRenderer(HtmlRenderer):
		pass

	renderer = CustomRenderer()
	text_md = "*Hello world*"
	result = markdown(text_md, renderer=renderer)

	# output: <p><em>Hello world</em></p>


or 

.. code:: python

	from mpiece.renderer import HtmlRenderer
	from mpiece import Markdown

	class CustomRenderer(HtmlRenderer):
		pass

	markdown = Markdown()
	markdown.renderer = CustomRenderer()
	text_md = "*Hello world*"
	result = markdown(text_md)

	# output: <p><em>Hello world</em></p>


Renderers list
--------------

.. autoclass:: mpiece.renderer.Renderer
	:members: post_process_text


.. autoclass:: mpiece.renderer.HtmlRenderer
	:members: scheme_blacklist, escape, escape_args, escape_link

