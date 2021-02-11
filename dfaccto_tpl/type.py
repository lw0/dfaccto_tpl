from copy import copy
from enum import Enum

from .base import DFACCTOAssert
from .role import Role


class Type():
  def __init__(self, package, name, role, **props):
    self.context = package.context
    self.package = package
    self.name = name
    self.role = role
    self.package.types.register(self.name, self)
    self.props = props
    if self.role.is_simple:
      self.identifier = 't_{}'.format(self.name)
      self.identifier_v = 't_{}_v'.format(self.name)
      self.package.identifiers.register(self.identifier, self)
      self.package.identifiers.register(self.identifier_v, self)
    elif self.role.is_complex:
      self.identifier_ms = 't_{}_ms'.format(self.name)
      self.identifier_sm = 't_{}_sm'.format(self.name)
      self.identifier_v_ms = 't_{}_v_ms'.format(self.name)
      self.identifier_v_sm = 't_{}_v_sm'.format(self.name)
      self.const_null_ms = 'c_{}Null_ms'.format(self.name)
      self.const_null_sm = 'c_{}Null_sm'.format(self.name)
      self.package.identifiers.register(self.identifier_ms, self)
      self.package.identifiers.register(self.identifier_sm, self)
      self.package.identifiers.register(self.identifier_v_ms, self)
      self.package.identifiers.register(self.identifier_v_sm, self)
      self.package.identifiers.register(self.const_null_ms, self)
      self.package.identifiers.register(self.const_null_sm, self)
    self.derived_from = None
    self.derivates = {self.role: self}

  def __str__(self):
    return '({}).t{}_{}'.format(self.package, self.role, self.name)

  def __getattr__(self, key):
    if key.startswith('x_') and key[2:] in self.props:
      return self.props[key[2:]]
    else:
      raise AttributeError(key)

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


