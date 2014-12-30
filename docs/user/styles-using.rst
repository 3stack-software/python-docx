
Working with Styles
===================

This page uses concepts developed in the prior page without introduction. If
a term is unfamiliar, consult the prior page :ref:`understandingstyles` for
a definition.


Access a style
--------------

Styles are accessed using the :attr:`.Document.styles` attribute::

    >>> document = Document()
    >>> styles = document.styles
    >>> styles
    <docx.styles.styles.Styles object at 0x10a7c4f50>

The |Styles| object provides dictionary-style access to defined styles by
name::

    >>> styles['Normal']
    <docx.styles.style._ParagraphStyle object at <0x10a7c4f6b>

.. note:: Built-in styles are stored in a WordprocessingML file using their
   English name, e.g. 'Heading 1', even though users working on a localized
   version of Word will see native language names in the UI, e.g. 'Kop 1'.
   Because |docx| operates on the WordprocessingML file, style lookups must
   use the English name. A document available on this external site allows
   you to create a mapping between local language names and English style
   names:
   http://www.thedoctools.com/index.php?show=mt_create_style_name_list

   User-defined styles, also known as *custom styles*, are not localized and
   are accessed with the name exactly as it appears in the Word UI.

The |Styles| object is also iterable. By using the identification properties
on |Style|, various subsets of the defined styles can be generated. For
example, this code will produce a list of the defined paragraph styles::

   >>> from docx.enum.style import WD_STYLE_TYPE
   >>> styles = document.styles
   >>> paragraph_styles = [
   ...     s for s in styles if s.type == WD_STYLE_TYPE.PARAGRAPH
   ... ]
   >>> for style in paragraph_styles:
   ...     print(style.name)
   ...
   Normal
   Body Text
   List Bullet


Apply a style
-------------

The |Paragraph|, |Run|, and |Table| objects each have a :attr:`style`
attribute. Assigning a |Style| object to this attribute applies that style::

    >>> document = Document()
    >>> paragraph = document.add_paragraph()
    >>> paragraph.style
    <docx.styles.style._ParagraphStyle object at <0x11a7c4c50>
    >>> paragraph.style.name
    'Normal'
    >>> paragraph.style = document.styles['Heading 1']
    >>> paragraph.style.name
    'Heading 1'

A style name can also be assigned directly, in which case |docx| will do the
lookup for you::

    >>> paragraph.style = 'List Bullet'
    >>> paragraph.style
    <docx.styles.style._ParagraphStyle object at <0x10a7c4f84>
    >>> paragraph.style.name
    'List Bullet'

A style can also be applied at creation time using either the |Style| object
or its name::

    >>> paragraph = document.add_paragraph(style='Body Text')
    >>> paragraph.style.name
    'Body Text'
    >>> body_text_style = document.styles['Body Text']
    >>> paragraph = document.add_paragraph(style=body_text_style)
    >>> paragraph.style.name
    'Body Text'


Add or delete a style
---------------------

A new style can be added to the document by specifying a unique name and
a style type::

    >>> from docx.enum.style import WD_STYLE_TYPE
    >>> styles = document.styles
    >>> style = styles.add_style('Citation', WD_STYLE_TYPE.PARAGRAPH)
    >>> style.name
    'Citation'
    >>> style.type
    PARAGRAPH (1)

Use the :attr:`~.BaseStyle.base_style` property to specify a style the new
style should inherit formatting settings from::

    >>> style.base_style
    None
    >>> style.base_style = styles['Normal']
    >>> style.base_style
    <docx.styles.style._ParagraphStyle object at 0x10a7a9550>
    >>> style.base_style.name
    'Normal'

A style can be removed from the document simply by calling its
:meth:`~.BaseStyle.delete` method::

    >>> styles = document.styles
    >>> len(styles)
    10
    >>> styles['Citation'].delete()
    >>> len(styles)
    9

.. note:: The :meth:`.Style.delete` method removes the style's definition
   from the document. It does not affect content in the document to which
   that style is applied. Content having a style not defined in the document
   is rendered using the default style for that content object, e.g.
   'Normal' in the case of a paragraph.


Control how a style appears in the Word UI
------------------------------------------

The properties of a style fall into two categories, *behavioral properties*
and *formatting properties*. Its behavioral properties control when and where
the style appears in the Word UI. Its formatting properties determine the
formatting of content to which the style is applied, such as the size of the
font and its paragraph indentation.

There are five behavioral properties of a style:

* :attr:`~.Style.hidden`
* :attr:`~.Style.unhide_when_used`
* :attr:`~.Style.priority`
* :attr:`~.Style.quick_style`
* :attr:`~.Style.locked`

The key notion to understanding the behavioral properties is the *recommended
list*. In the style pane in Word, the user can select which list of styles
they want to see. One of those is named *Recommended*. All five behavior
properties affect some aspect of the style's appearance in this list and in
the style gallery.

In brief, a style appears in the recommended list if its `hidden` property is
|False|. If a style is not hidden and its `quick_style` property is |True|,
it also appears in the style gallery. The style's `priority` value (|int|)
determines its position in the sequence of styles. If a styles's `locked`
property is |True| and formatting restrictions are turned on for the
document, the style will not appear in any list or the style gallery and
cannot be applied to content.


Working with Latent Styles
--------------------------

... describe latent styles in Understanding page ...

Let's illustrate these behaviors with a few examples.
