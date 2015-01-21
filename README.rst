.. image:: https://travis-ci.org/python-openxml/python-docx.svg?branch=master
   :target: https://travis-ci.org/python-openxml/python-docx

*python-docx* is a Python library for creating and updating Microsoft Word
(.docx) files.

More information is available in the `python-docx documentation`_.

This fork adds a proof of concept for using docx documents as templates. 
Two templating engines (django and jinja) are supported.
Template instructions can be written directly in Word or handcrafted in the document.xml
If written in Word, Block-Level tags must have a style named "TEMPLATE_BLOG" attached.
Color, font, etc. of TEMPLATE_BLOG are left to your liking (I use Courier, Green, 4pt).
Usage is simple:

```python
from docx import Document
d = Document("in.docx")
d.save( "out.docx", {'name':"Holli"}, "jinja" )
```

will replace every instance of the text {{ name }} in in.docx with "Holli" and saves it to out.docx

For more information about template languages see the respective engine documentation.

.. _`python-docx documentation`:
   https://python-docx.readthedocs.org/en/latest/
