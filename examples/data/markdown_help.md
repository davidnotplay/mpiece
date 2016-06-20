Help
====

Styles
------
MPiece allows the use of inline styles for the fonts. For example:

-	Use `**text**` grammar for makes bold text: **This is a bold text**.
-	Use `*text*` grammar for makes italic text: *This is an italic text*.
-	Use `_text_` grammar form makes underline text: _This is an underline text._
	You can modify the `HtmlRenderer` params for transforms the underline text in italic text, as the conventional markdown grammar.
-	Use `~text~`grammar for makes strike text: ~This is a strike text~.
-	Use `\`text\`` grammar for makes code inline text: `Code inline`.
-	You can mix all previous styles. **bold *italic and ~strike~* _underline and *italic*_  `code inline`**

You can use the styles in other markdown structures as **links**, **blockquote**, **lists** and **headers**

Links
-----

```"links"
[link text 1](link_url)
[link text 2](link_url "optional title")
```

#### Result
[link text 1](link_url)
[link text 2](link_url "optional title")

You can use styles in the link text.

```"links with style"
[**bold link**](link_url)
[*italic link*](link_url "optional title")

```

#### Result
[**bold link**](link_url)
[*italic link*](link_url "optional title")

You can use the links in **headers**, **blockquotes** and **lists**.

Images
------

```"Images"
![image alt text](src_link, "optional title")
```

#### Result
![image alt text](src_link, "optional title")


You can mix links and images.
```"Image inside link"
[![alt image text](http://src1)](http://link1)
```


#### Result
[![alt image text](http://src1)](http://link1)


New line
--------

New line in text
~~~~~~~~~~~~~~~~
MPiece separates text lines in paragraph when it finds 2 break lines `\n\n`.
```"New line in markdown"
paragraph 1
continue paragraph 1

new paragraph 2
continue paragraph 2
```
#### Result
paragraph 1
continue paragraph 1

new paragraph 2
continue paragraph 2

New line in list
~~~~~~~~~~~~~~~~

In lists or blockquote the new lines in markdown grammar make new paragraphs.

```"New lines in lists or blockquote"
*	item 1
	new paragraph item 1
*	item 2
	new paragraph item 2

> paragraph 1
> paragraph 2
```

#### Result
*	item 1
	new paragraph item 1
*	item 2
	new paragraph item 2

> paragraph 1
> paragraph 2



Break lines
~~~~~~~~~~~

```"Break lines"

***
---
___


```

#### Result

***

---
___


Lists
-----

Ordered lists
~~~~~~~~~~~~~

``` "Ordered lists in markdown"
1. item 1
2. item 2
	1. sub item 1
	2. sub item 2
		1. sub sub item 1
		2. sub sub item 2
	3. sub item 3
3. item 3
4. item 4
```

#### Result
1. item 1
2. item 2
	1. sub item 1
	2. sub item 2
		1. sub sub item 1
		2. sub sub item 2
	3. sub item 3
3. item 3
4. item 4


Unordered lists
~~~~~~~~~~~~~~~

```"Unordered list"
* item 1
* item 2
* item 3
	* sub item 1
	* sub item 2
```

other way:

```"Alternative unordered list"
- item 1
- item 2
	- sub item 1
	- sub item 2
- item 3

```

#### Result

* item 1
* item 2
* item 3
	* sub item 1
	* sub item 2

other way:

- item 1
- item 2
	- sub item 1
	- sub item 2
- item 3


Headers
-------

There 2 ways to use headers.

The first:

```"Headers, way 1"
Header 1
========

Header 2
--------

Header 3
~~~~~~~~
```

#### Result
Header 1
========

Header 2
--------

Header 3
~~~~~~~~

The second way:
```"Headers, way 2"
# Header 1
## Header 2 ##
### Header 3
#### Header 4 ####
##### Header 5
###### Header 6 #######
.
.
.
```

#### Result ####

# Header 1
## Header 2 ##
### Header 3
#### Header 4 ####
##### Header 5
###### Header 6 ######

There isn't limit to the header level. The characters `#` in the end of header text is optional.

Blockquotes
-----------

```"Blockquotes"
> block 1
> new line block 1
> new line block 1

> block 2
> > sub block 1
> > new line sub block 1
> new line block 2
> new line block 2

> # Header 1
> block 3
> new line block 3
> new line **with style**

```

#### Result
> block 1
> new line block 1
> new line block 1

> block 2
> > sub block 1
> > new line sub block 1
> new line block 2
> new line block 2

> # Header 1
> block 3
> new line block 3
> new line **with style**

There isn't limit in sub blockquotes inside a blockquote.

Fenced code
-----------

```"Fenced code"
\```language "title of code"
code
\```
```

#### Result
```language "title of code"
code
```

The parameter *language* and *title of code* is optional. The `HtmlRenderer` class doesn't show the title. You should modify
the **fenced code** output to add the code title. You can she the file `example/show.py` or
the [official documentation](http://mpiece.readthedocs.io/en/latest/) for more information.


Tables
------

```"Tables"
|header 1 | header 2 | header 3 |
|:--------|:--------:|---------:|
| cell 1  | cell 2   | celll 3  |
| cell 4  | cell 5   | celll 6  |
```

#### Result

|header 1 | header 2 | header 3 |
|:--------|:--------:|---------:|
| cell 1  | cell 2   | celll 3  |
| cell 4  | cell 5   | celll 6  |


The second lines of the code is the align of the column: *left*, *center*, *right*. This is is line is required if not the
table code no run.


Footnotes
---------

```"Make footnoes"

\[^note1\]: *single line*

\[^note2\]: 
	note in multiple lines.
	**It is necessary to add the indent space for this notes type.**
```

```"Use footnotes"

Normal text: add a note 1 \[^note1\].

New paragraph and add \[^note2\]

```

#### Result
[^note1]: *single line*

[^note2]: 
	note in multiple lines.
	**It is necessary to add the indent space for this notes type.**

Normal text: add a note 1 [^note1].

New paragraph and add note 2 [^note2]

**IMPORTANT**: The character `\\` is necessary for that the fenced_code shows the notes markdown grammar. You shouldn't
use the character `\\` if you want use the footnotes.

