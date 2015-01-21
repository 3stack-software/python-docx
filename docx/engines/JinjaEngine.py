import os, importlib
from jinja2 import Template, Environment
from docx.engines.base import Engine as base

"""
Engine for Jinja
"""
class Engine(base):
    def __init__(self):
        self.tag_re = "(\{[^\}]+?\}\}?)"
      
    """
    Fix the template and feed it to the engine
    """      
    def render(self, template, context):
        xml = self.fix_tag_gaps(template)
        xml = self.fix_block_tags(xml)
        self.template = Template(xml.decode("utf8"))
        self._register_filters()
        return self.template.render(context).encode("utf8")
    
    """
    Load custom template filters from docx/engines/filters/django/*.py
    """
    def _register_filters(self):
        path = os.path.join(os.path.dirname(__file__), "filters", "jinja")
        for file in os.listdir(path):
            if file.endswith(".py") and file != "__init__.py":
                module = "docx.engines.filters.jinja.%s" % file.replace(".py", "")
                module = importlib.import_module(module, package=None)
                for name, val in module.__dict__.iteritems():  # iterate through every module's attributes
                    if callable(val):                          # check if callable (normally functions)
                        self.template.environment.filters[name] = val