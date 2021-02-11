from .base import Registry
from .common import Element


class Package(Element):

  def __init__(self, context, name, props):
    Element.__init__(self, context, name, '{name}')
    self._props = props
    self._types = Registry()
    self._identifiers = Registry()

    self.context.packages.register(self.name, self)
    self.context.identifiers.register(self.identifier, self)

  def __str__(self):
    return self.name

  @property
  def props(self):
    return self._props

  def __getattr__(self, key):
    if key.startswith('x_') and key[2:] in self._props:
      return self._props[key[2:]]
    else:
      raise AttributeError(key)

  @property
  def types(self):
    return self._types

  @property
  def identifiers(self):
    return self._identifiers


