import re

from .context import Context



_InnerNewline = re.compile(r'(\r|\r?\n)(?=.)')
_TrailingNewline = re.compile(r'\r|\r?\n$')
def _indent(string, indent, eat_trailing=False):
  if indent:
    string = _InnerNewline.sub(r'\1{}'.format(indent), string)
  if eat_trailing:
    string = _TrailingNewline.sub('', string)
  return string


class LiteralToken:

  def __init__(self, string):
    self._string = string

  def render_with(self, context):
    return self._string


class ValueToken: # {{key}} {{&key}}

  def __init__(self, key, indent, verbatim=False):
    self.key = key
    self.indent = indent
    self.verbatim = verbatim

  def render_with(self, context):
    string = context.get_string(self.key, self.verbatim)
    return _indent(string, self.indent)


class IndirectToken: # {{*key}}

  def __init__(self, key, indent, parser):
    self.key = key
    self.indent = indent
    self.parser = parser

  def render_with(self, context):
    template_string = context.get_string(self.key, True)
    template = self.parser.parse(template_string)
    string = template.render_with(context)
    return _indent(string, self.indent)


class PartialToken: # {{>name}}

  def __init__(self, name, indent):
    self.name = name
    self.indent = indent

  def render_with(self, context):
    template = context.get_partial(self.name)
    if template is not None:
      string = template.render_with(context)
      return _indent(string, self.indent, eat_trailing=True)
    return ''


class SectionToken: # {{#key}}...{{/key}} {{#key}}...{{|key}}...{{/key}} {{^key}}...{{/key}}

  def __init__(self, key, truthy_content, falsey_content):
    self.key = key
    self.truthy_content = truthy_content
    self.falsey_content = falsey_content

  def render_with(self, context):
    output = list()
    section = context.get_section(self.key)
    if self.truthy_content:
      for item in section:
        context.push(item)
        for token in self.truthy_content:
          output.append(token.render_with(context))
        context.pop()
    if self.falsey_content:
      if not section:
        for token in self.falsey_content:
          output.append(token.render_with(context))
    return ''.join(output)


class Template:

  def __init__(self, content, name=None):
    self._content = content
    self._name = name or '<string>'

  def render_with(self, context):
    output = list()
    for token in self._content:
      output.append(token.render_with(context))
    return ''.join(output)

  def render(self, *context_items, **context_kwargs):
    context = Context(*context_items, **context_kwargs)
    return self.render_with(context)

