from .util import Registry
from .common import HasProps
from .element import Element


class Package(Element, HasProps):

  def __init__(self, context, name, props):
    Element.__init__(self, context, name, '{name}')
    HasProps.__init__(self, props)

    self._types = Registry()
    self._constants = Registry()
    self._identifiers = Registry()

    self.context.packages.register(self.name, self)
    self.context.identifiers.register(self.identifier, self)

  def __str__(self):
    return self.name

  @property
  def has_role(self):
    return False

  @property
  def types(self):
    return self._types

  @property
  def constants(self):
    return self._constants

  @property
  def identifiers(self):
    return self._identifiers


