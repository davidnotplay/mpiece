Installation and Basic Usage
============================

Installation
------------


Installing mpiece with pip:

.. code::

  $ pip install mpiece


Basic Usage
-----------

.. code:: python
   
   from mpiece import markdown

   text_md = "**Hello world**"
   result = markdown(text_md)
   print(result)
   # output <p><strong>Hello world</strong></p>


MPiece core
---------------

.. autofunction:: mpiece.markdown

.. autoclass:: mpiece.Markdown
	:members: __call__
