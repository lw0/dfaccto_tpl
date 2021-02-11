from copy import copy
from enum import Enum

from .base import DFACCTOError


class Role(Enum):
  Input      = 0x1  # Port   - in
  Output     = 0x2  # Port   - out
  Simple     = 0x3  # Signal - Input or Output
  Slave      = 0x10 # Port   - ms: in  | sm: out
  Master     = 0x20 # Port   - ms: out | sm: in
  View       = 0x40 # Port   - ms: in  | sm: in
  Pass       = 0x80 # Port   - ms: out | sm: out
  Complex    = 0xF0 # Signal - Slave, Master, View or Pass

  @staticmethod
  def parse(string):
    if string == 'i':
      return Role.Input
    elif string == 'o':
      return Role.Output
    elif string == 'S':
      return Role.Simple
    elif string == 's':
      return Role.Slave
    elif string == 'm':
      return Role.Master
    elif string == 'v':
      return Role.View
    elif string == 'p':
      return Role.Pass
    elif string == 'C':
      return Role.Complex
    raise DFACCTOError('"{}" is not a role identifier'.format(string))

  def __str__(self):
    if self.value == 0x1:
      return 'i'
    elif self.value == 0x2:
      return 'o'
    elif self.value == 0x3:
      return 'S'
    elif self.value == 0x10:
      return 's'
    elif self.value == 0x20:
      return 'm'
    elif self.value == 0x40:
      return 'v'
    elif self.value == 0x80:
      return 'p'
    elif self.value == 0xF0:
      return 'C'
    return '!'

  @property
  def is_signal(self):
    return self.value in (0x3, 0xF0)

  @property
  def is_port(self):
    return self.value in (0x1, 0x2, 0x10, 0x20, 0x40, 0x80)

  @property
  def is_input(self):
    return self.value == 0x1

  @property
  def is_output(self):
    return self.value == 0x2

  @property
  def is_simple(self):
    return self.value in (0x1, 0x2, 0x3)

  @property
  def is_slave(self):
    return self.value == 0x10

  @property
  def is_master(self):
    return self.value == 0x20

  @property
  def is_view(self):
    return self.value == 0x40

  @property
  def is_pass(self):
    return self.value == 0x80

  @property
  def is_complex(self):
    return self.value in (0x10, 0x20, 0x40, 0x80, 0xF0)

  def is_compatible(self, other):
    if self.value == 0x1:
      return other.value in (0x1, 0x3)
    elif self.value == 0x2:
      return other.value in (0x2, 0x3)
    elif self.value == 0x3:
      return other.value in (0x1, 0x2, 0x3)
    elif self.value == 0x10:
      return other.value in (0x10, 0xF0)
    elif self.value == 0x20:
      return other.value in (0x20, 0xF0)
    elif self.value == 0x40:
      return other.value in (0x40, 0xF0)
    elif self.value == 0x80:
      return other.value in (0x80, 0xF0)
    elif self.value == 0xF0:
      return other.value in (0x10, 0x20, 0x40, 0x80, 0xF0)
    return False

  # @property
  # def inverted(self):
  #   if self.value == 0x1:
  #     return Role.Output
  #   elif self.value == 0x2:
  #     return Role.Input
  #   elif self.value == 0x3:
  #     return Role.Simple # not invertible
  #   elif self.value == 0x10:
  #     return Role.Master
  #   elif self.value == 0x20:
  #     return Role.Slave
  #   elif self.value == 0x40:
  #     return Role.Pass
  #   elif self.value == 0x80:
  #     return Role.View
  #   elif self.value == 0x80:
  #     return Role.Complex # not invertible

  @property
  def mode(self):
    if self.is_input:
      return 'in'
    elif self.is_output:
      return 'out'
    else:
      return None

  @property
  def mode_ms(self):
    if self.is_slave or self.is_view:
      return 'in'
    elif self.is_master or self.is_pass:
      return 'out'
    else:
      return None

  @property
  def mode_sm(self):
    if self.is_master or self.is_view:
      return 'in'
    elif self.is_slave or self.is_pass:
      return 'out'
    else:
      return None



