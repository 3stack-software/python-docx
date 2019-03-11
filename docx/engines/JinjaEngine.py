import logging
import re

import jinja2
import lxml.etree as et

logger = logging.getLogger(__name__)
_namespaces = {
    "o": "urn:schemas-microsoft-com:office:office",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w10": "urn:schemas-microsoft-com:office:word",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "w14": "  http://schemas.microsoft.com/office/word/2010/wordml"
}


class Engine(object):
    """
    Fix the template and feed it to the engine
    """

    def render(self, template, context):
        '''
        :type template: bytes
        :type context: dict
        :rtype: bytes
        '''
        bs = fix_tag_gaps(template)
        bs = fix_block_tags(bs)
        if not bs:
            return template
        obj = jinja2.Template(bs.decode('utf-8'))
        return obj.render(context).encode('utf-8')


def fix_tag_gaps(bs):
    logger.info("""base.Engine._fix_tag_gaps()""")

    def repl(matchobject):
        return replace_junk(matchobject.group(1))

    logger.debug("""base.Engine._fix_tag_gaps.xml: xml before %s """, bs)

    bs = re.sub(rb"({[^\}]+?\}\}?)", repl, bs, flags=re.DOTALL)

    logger.debug("""base.Engine._fix_tag_gaps.xml: xml after %s """, bs)

    return bs


def replace_junk(bs):
    logger.info("""base.Engine.replace_junk()""")
    logger.debug("""base.Engine._fix_tag_gaps.repl: text %s """, bs)

    bs = re.sub(rb"^\s*<", b"<", bs, flags=re.MULTILINE)

    logger.debug("""base.Engine._fix_tag_gaps.repl: removed whitespace %s """, bs)

    bs = re.sub(rb"<[^>]+>", b"", bs)

    logger.debug("""base.Engine._fix_tag_gaps.repl: removed tags %s """, bs)

    # bs = os.linesep.join([s for s in bs.splitlines() if s])
    bs = re.sub(rb"[\n\r]*", b"", bs)

    logger.debug("""base.Engine._fix_tag_gaps.repl: removed blank lines %s """, bs)

    return bs


def fix_block_tags(bs):
    logger.info("""TemplateReader._fix_block_gaps()""")
    parser = et.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = et.fromstring(bs, parser=parser)
    if root is None:
        return None
    for xpath in [".//w:pStyle[@w:val='TEMPLATEBLOCK']", ".//w:rStyle[@w:val='TEMPLATEBLOCKChar']"]:
        nodelist = root.xpath(xpath, namespaces=_namespaces)
        logger.debug("""TemplateReader._fix_block_tags: found %d container-elements""", len(nodelist))

        for node in nodelist:
            paragraph = node.getparent().getparent()
            textnodes = paragraph.xpath('.//w:t', namespaces=_namespaces)
            text = "".join(x.text for x in textnodes)
            logger.debug("""TemplateReader._fix_block_tags: found %d t-elements""", len(textnodes))
            logger.debug("""TemplateReader._fix_block_tags: text %s""", text)

            p = paragraph.getprevious()
            if p is None:
                p = paragraph.getparent()
                p.text = text
                p.remove(paragraph)
            else:
                p.tail = p.tail + text if p.tail else text
                paragraph.getparent().remove(paragraph)

    return et.tostring(root, pretty_print=False, encoding="UTF-8")
