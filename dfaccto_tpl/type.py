from copy import copy
from enum import Enum

from .common import HasProps
from .util import DFACCTOAssert
from .role import Role


class Type(HasProps):
  def __init__(self, package, name, role, props, idents):
    HasProps.__init__(self, props)
    self.context = package.context
    self.package = package
    self.name = name
    self.role = role
    self.package.types.register(self.name, self)
    self.identifiers = list()
    if self.role.is_simple:
      self._dirs = ('',)
      self.identifier = 't_{}'.format(self.name)
      self.identifier_v = 't_{}_v'.format(self.name)
      self.identifiers.extend((self.identifier, self.identifier_v))
    elif self.role.is_complex:
      self._dirs = ('_ms', '_sm')
      self.identifier_ms = 't_{}_ms'.format(self.name)
      self.identifier_sm = 't_{}_sm'.format(self.name)
      self.identifier_v_ms = 't_{}_v_ms'.format(self.name)
      self.identifier_v_sm = 't_{}_v_sm'.format(self.name)
      self.identifiers.extend((self.identifier_ms, self.identifier_sm,
                               self.identifier_v_ms, self.identifier_v_sm))
    for name,pattern,use_dir in idents:
      for dir in (self._dirs if use_dir else ('',)):
        ident = pattern.format(name=self.name, dir=dir, role=str(self.role))
        self.identifiers.append(ident)
        self.props[name+dir] = ident
    for ident in self.identifiers:
      self.package.identifiers.register(ident, self)
    self.derived_from = None
    self.derivates = {self.role: self}

  def __str__(self):
    return '({}).t{}_{}'.format(self.package, self.role, self.name)

  def derive(self, role):
    DFACCTOAssert(self.derived_from is None,
      'Can not derive from already derived type {}'.format(self))
    DFACCTOAssert(self.role.is_compatible(role),
      'Can not derive incompatible role {} from type {}'.format(role, self))
    if role in self.derivates:
      return self.derivates[role]
    derivate = copy(self)
    derivate.role = role
    derivate.derived_from = self
    self.derivates[role] = derivate
    return derivate

  def is_compatible(self, other):
    if self.name != other.name:
      return False
    return self.role.is_compatible(other.role)

  @property
  def base(self):
    if self.derived_from is None:
      return self
    return self.derived_from

  @property
  def is_signal(self):
    return self.role.is_signal

  @property
  def is_port(self):
    return self.role.is_port

  @property
  def is_input(self):
    return self.role.is_input

  @property
  def is_output(self):
    return self.role.is_output

  @property
  def is_simple(self):
    return self.role.is_simple

  @property
  def is_view(self):
    return self.role.is_view

  @property
  def is_pass(self):
    return self.role.is_pass

  @property
  def is_slave(self):
    return self.role.is_slave

  @property
  def is_master(self):
    return self.role.is_master

  @property
  def is_complex(self):
    return self.role.is_complex

  @property
  def mode(self):
    return self.role.mode

  @property
  def mode_ms(self):
    return self.role.mode_ms

  @property
  def mode_sm(self):
    return self.role.mode_sm


