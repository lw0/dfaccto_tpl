from copy import copy
from enum import Enum

from .element import PackageElement
from .util import DFACCTOAssert, safe_str
from .role import Role


class Type(PackageElement):
  def __init__(self, package, name, is_complex):
    self._role = Role.Complex if is_complex else Role.Simple
    PackageElement.__init__(self, package, name, 't_{name}{vec}{dir}', has_vector=True)
    self.package.types.register(self.name, self)
    decl_name = self.package.declarations.unique_name(self.name) # Avoid collisions with constant names
    self.package.declarations.register(decl_name, self)
    if self.is_simple:
      self.package.identifiers.register(self.identifier, self)
      self.package.identifiers.register(self.identifier_v, self)
    elif self.is_complex:
      self.package.identifiers.register(self.identifier_ms, self)
      self.package.identifiers.register(self.identifier_sm, self)
      self.package.identifiers.register(self.identifier_v_ms, self)
      self.package.identifiers.register(self.identifier_v_sm, self)

  def __str__(self):
    try:
      return '({}).t{}_{}'.format(self.package, self._role.char, self.name)
    except:
      return safe_str(self)

  def __eq__(self, other):
    if isinstance(other, Type):
      return self._role == other._role and self.name == other.name
    else:
      return False

  @property
  def has_role(self):
    return True

  @property
  def role(self):
    return self._role


  @property
  def knows_complex(self):
    return self._role.knows_complex

  @property
  def is_complex(self):
    return self._role.is_complex

  @property
  def is_simple(self):
    return self._role.is_simple


