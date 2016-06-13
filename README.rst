MPiece
======
Fast and very customizable markdown parser in pure Python.

Features
--------

- **Pure Python**.  Tested in Python 2.7+, Python 3.3+ and PyPy.
- **Very fast**.
- **Customizable**. You can add new markdown grammar and modify the output.
- **More**. Table, footnotes, fenced code.


Install
-------

Installing mpiece with pip:

.. code::

  $ pip install mpiece


Basic Usage
-----------

.. code:: python

   from mpiece import markdown

   md_text = "**Hello world!!!**"
   result = markdown(md_text)

   print(result)
   # output: <p><strong>Hello world!!!</strong></p>


Documentation
-------------

`Official documentation <http://mpiece.readthedocs.io/>`_

