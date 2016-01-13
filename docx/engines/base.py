import logging, re, os
logger = logging.getLogger(__name__)
from lxml import etree

class Engine():
    tag_re = None
    
    namespaces = {
        "o":    "urn:schemas-microsoft-com:office:office",
        "r":    "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "v":    "urn:schemas-microsoft-com:vml",
        "w":    "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "w10":  "urn:schemas-microsoft-com:office:word",
        "wp":   "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
        "wps":  "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
        "wpg":  "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
        "mc":   "http://schemas.openxmlformats.org/markup-compatibility/2006",
        "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
        "w14":"  http://schemas.microsoft.com/office/word/2010/wordml"
    }
    
    def render(self, template, context):
        return template

    def fix_tag_gaps(self, xml):
        logger.info("""base.Engine._fix_tag_gaps()""")
       
        def repl(matchobject):
            return self.replace_junk(matchobject.group(1))
        
        logger.debug("""base.Engine._fix_tag_gaps.xml: xml before %s """ % xml)
        
        xml = re.sub(self.tag_re, repl, xml, flags=re.DOTALL) 
        
        logger.debug("""base.Engine._fix_tag_gaps.xml: xml after %s """ % xml)
        
        return xml

    def replace_junk(self, text):
        logger.info("""base.Engine.replace_junk()""")
        logger.debug("""base.Engine._fix_tag_gaps.repl: text %s """ % text)
        
        text = re.sub("^[\t\s]*<", "<", text, flags=re.DOTALL|re.MULTILINE)
        
        logger.debug("""base.Engine._fix_tag_gaps.repl: removed whitespace %s """ % text)
        
        text = re.sub("<[^>]+>", "", text, flags=re.DOTALL)
        
        logger.debug("""base.Engine._fix_tag_gaps.repl: removed tags %s """ % text)
        
        text = os.linesep.join([s for s in text.splitlines() if s])
        text = re.sub("\n", "", text, flags=re.DOTALL|re.MULTILINE)
        text = re.sub("\r", "", text, flags=re.DOTALL|re.MULTILINE)
        
        logger.debug("""base.Engine._fix_tag_gaps.repl: removed blank lines %s """ % text)

        return text
        
        
    def fix_block_tags(self, xml):
        logger.info("""TemplateReader._fix_block_gaps()""")
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring( bytes(bytearray(xml)), parser=parser)
        if root is None:
            return None
        for xpath in [".//w:pStyle[@w:val='TEMPLATEBLOCK']", ".//w:rStyle[@w:val='TEMPLATEBLOCKChar']"]:
            nodelist = root.xpath(xpath, namespaces=self.namespaces)
            logger.debug("""TemplateReader._fix_block_tags: found %s container-elements""" % len(nodelist))
        
            for node in nodelist:
                paragraph = node.getparent().getparent()
                textnodes = paragraph.xpath('.//w:t', namespaces=self.namespaces)
                text = "".join( x.text for x in textnodes)
                logger.debug("""TemplateReader._fix_block_tags: found %s t-elements""" % len(textnodes))
                logger.debug("""TemplateReader._fix_block_tags: text %s""" % text)
                
                p = paragraph.getprevious()
                if p is None:
                    p = paragraph.getparent()
                    p.text = text
                    p.remove(paragraph)
                else:
                    p.tail = p.tail + text if p.tail else text
                    paragraph.getparent().remove(paragraph)
            
        xml = etree.tostring(root, pretty_print=False, encoding="UTF-8")
        logger.debug("""TemplateReader._fix_block_tags: ends with xml %s""" % xml)
        return xml