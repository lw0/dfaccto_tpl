from copy import copy
from enum import Enum

from .common import HasProps, PackageElement
from .util import DFACCTOAssert


class Type(PackageElement, HasProps):
  def __init__(self, package, name, role, props):
    HasProps.__init__(self, props)
    PackageElement.__init__(self, package, name, 't_{name}{vec}{dir}', has_vector=True)
    self._role = role
    self.package.types.register(self.name, self)
    if self.role.is_simple:
      self.package.identifiers.register(self.identifier, self)
      self.package.identifiers.register(self.identifier_v, self)
    elif self.role.is_complex:
      self.package.identifiers.register(self.identifier_ms, self)
      self.package.identifiers.register(self.identifier_sm, self)
      self.package.identifiers.register(self.identifier_v_ms, self)
      self.package.identifiers.register(self.identifier_v_sm, self)
    self._derived_from = None
    self._derivates = {self.role: self}

  def __str__(self):
    return '({}).t{}_{}'.format(self.package, self.role, self.name)

  def derive(self, role):
    DFACCTOAssert(self._derived_from is None,
      'Can not derive from already derived type {}'.format(self))
    DFACCTOAssert(self.role.is_compatible(role),
      'Can not derive incompatible role {} from type {}'.format(role, self))
    if role in self._derivates:
      return self._derivates[role]
    derivate = copy(self)
    derivate._role = role
    derivate._derived_from = self
    self._derivates[role] = derivate
    return derivate

  def is_compatible(self, other):
    if self.name != other.name:
      return False
    return self._role.is_compatible(other._role)

  @property
  def is_definite(self):
    return True

  @property
  def has_role(self):
    return True

  @property
  def role(self):
    return self._role

  @property
  def base(self):
    if self._derived_from is None:
      return self
    return self._derived_from

  @property
  def is_signal(self):
    return self._role.is_signal

  @property
  def is_port(self):
    return self._role.is_port

  @property
  def is_input(self):
    return self._role.is_input

  @property
  def is_output(self):
    return self._role.is_output

  @property
  def is_simple(self):
    return self._role.is_simple

  @property
  def is_view(self):
    return self._role.is_view

  @property
  def is_pass(self):
    return self._role.is_pass

  @property
  def is_slave(self):
    return self._role.is_slave

  @property
  def is_master(self):
    return self._role.is_master

  @property
  def is_complex(self):
    return self._role.is_complex

  @property
  def mode(self):
    return self._role.mode

  @property
  def mode_ms(self):
    return self._role.mode_ms

  @property
  def mode_sm(self):
    return self._role.mode_sm

  @property
  def cmode(self):
    return self._role.cmode

  @property
  def cmode_ms(self):
    return self._role.cmode_ms

  @property
  def cmode_sm(self):
    return self._role.cmode_sm


