from .parser import Parser, ParserError
from .rendering import Template, LiteralToken, ValueToken, IndirectToken, PartialToken, SectionToken
from .key import Key
from .context import Context
from .errors import TemplateError, ParserError, AbsentError


_default_parser = Parser()
def parse(string, name=None):
  return _default_parser.parse(string, name)


def render(template, *context_items, **context_kwargs):
  tpl = parse(template)
  return tpl.render(*context_items, **context_kwargs)
