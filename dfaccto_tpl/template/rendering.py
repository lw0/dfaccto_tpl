import re
from enum import Enum, auto

from .context import Context
from .errors import ParserError



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


class ValueToken:
  # {{key}}
  # {{&key}}
  def __init__(self, key, indent, verbatim=False):
    self.key = key
    self.indent = indent
    self.verbatim = verbatim

  def render_with(self, context):
    string = context.get_string(self.key, self.verbatim)
    return _indent(string, self.indent)


class IndirectToken:
  # {{*key}}
  def __init__(self, key, indent, parser):
    self.key = key
    self.indent = indent
    self.parser = parser

  def render_with(self, context):
    template_string = context.get_string(self.key, True)
    template = self.parser.parse(template_string)
    string = template.render_with(context)
    return _indent(string, self.indent)


class PartialToken:
  # {{>name}}
  def __init__(self, name, indent):
    self.name = name
    self.indent = indent

  def render_with(self, context):
    template = context.get_partial(self.name)
    if template is not None:
      string = template.render_with(context)
      return _indent(string, self.indent, eat_trailing=True)
    return ''


class SectionToken:
  # {{#key}}...[{{|key}}...]{{/key}} (mode=Loop)
  # {{=key}}...[{{|key}}...]{{/key}} (mode=Enter)
  # {{?key}}...[{{|key}}...]{{/key}} (mode=Check)
  # {{!key}}...[{{|key}}...]{{/key}} (mode=Exist)
  # {{^key}}...{{/key}}              (mode=Loop)
  def __init__(self, key, truthy_content, falsey_content, mode):
    """
      mode
        Loop: Render truthy content with items of iterable-coerced key-value, and if empty falsey content with original context
        Enter: Render truthy content with key-value directly if present, and if absent falsey content with original context
        Check: Render truthy content with original context if key-value is truthy, and if falsey or absent render falsey content with original context
        Exist: Render truthy content with original context if key-value is present, and if absent render falsey content with original context
    """
    self.key = key
    self.truthy_content = truthy_content
    self.falsey_content = falsey_content
    self.mode = mode
    if mode == 'Loop':
      self._get_iterable = True
      self._get_value = False
      self._get_exists = False
      self._do_push = True
    elif mode == 'Enter':
      self._get_iterable = False
      self._get_value = False
      self._get_exists = True
      self._do_push = True
    elif mode == 'Check':
      self._get_iterable = False
      self._get_value = True
      self._get_exists = False
      self._do_push = False
    elif mode == 'Exist':
      self._get_iterable = False
      self._get_value = False
      self._get_exists = True
      self._do_push = False
    else:
      raise ParserError('Invalid section mode "{}" must be Loop, Enter, Check or Exist'.format(mode))

  def _render_truthy(self, context, item):
    if self.truthy_content:
      if self._do_push:
        context.push(item)
      for token in self.truthy_content:
        yield token.render_with(context)
      if self._do_push:
        context.pop()

  def _render_falsey(self, context):
    if self.falsey_content:
      for token in self.falsey_content:
        yield token.render_with(context)

  def render_with(self, context):
    output = list()
    if self._get_iterable:
      iterable = context.get_iterable(self.key)
      for item in iterable:
        output.extend(self._render_truthy(context, item))
      if not iterable:
        output.extend(self._render_falsey(context))
    elif self._get_value:
      value = context.get_value(self.key)
      if value:
        output.extend(self._render_truthy(context, value))
      else:
        output.extend(self._render_falsey(context))
    elif self._get_exists:
      if context.has_value(self.key):
        item = context.get_value(self.key)
        output.extend(self._render_truthy(context, item))
      else:
        output.extend(self._render_falsey(context))
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

