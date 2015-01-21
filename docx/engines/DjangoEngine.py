import os
import django
from django.conf import settings; settings.configure()
from docx.engines.base import Engine as base
from django.template import Template
from django.template import Template, Context

"""
Engine for Django
"""
class Engine(base):
    def __init__(self):
        self.tag_re = "(\{[^\}]+?\}\}?)"
        
    """
    Fix the template and feed it to the engine
    """
    def render(self, template, context):
        django.setup()
        self._register_filters()
        xml = self.fix_tag_gaps(template)
        xml = self.fix_block_tags(xml)
        self.template = Template(xml)
        return self.template.render(Context(context)).encode("utf8")
    
    """
    Load custom template filters from docx/engines/filters/django/*.py
    """
    def _register_filters(self):
        path = os.path.join(os.path.dirname(__file__), "filters", "django")
        for file in os.listdir(path):
            if file.endswith(".py") and file != "__init__.py":
                module =  "filters.django.%s" % file.replace(".py", "")
                __import__(module, globals(), locals() )
                