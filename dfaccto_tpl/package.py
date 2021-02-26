from .util import Registry, safe_str
from .common import HasProps
from .element import Element
from .type import Type
from .constant import Constant


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
    try:
      return self.name
    except:
      return safe_str(self)

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

  def add_type(self, name, role, props):
    return Type(self, name, role, props)

  def add_constant(self, name, type, size_name, value, props):
    return Constant(self, name, type, size_name, value, props=props)


