Custom Grammar
==============

With **MPiece** you can modify the output and the grammar markdown easily. For example, changing the text color using
the custom grammar:
```"Custom grammar change color"
#f00 Text in red color.## Continue normal text. #00f Text in blue color.##
```

Result
~~~~~~
#f00 Text in red color.## Continue normal text. #00f Text in blue color.##

This only is a examples, This grammar isn't part of the default MPiece grammar. If you want makes your custom grammar, you should see the [official documentation](http://mpiece.readthedocs.io/en/latest/)  or see the code in the file `examples/show.py`
for more information.

Another Example
---------------

This example using markdown grammar to show emojis.

```"Add emojis"
Smiley :smile: ahahaha :XD:. Another more :love: Continue and :invalidEmoji:
```

Result
~~~~~~
Smiley :smile: ahahaha :XD:. Another more :love: Continue and :invalidEmoji:

How the previous examples, this grammar isn't part of the default MPiece grammar.