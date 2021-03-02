from collections import defaultdict
import collections.abc as abc

from .util import DFACCTOError, DFACCTOAssert, IndexedObj, ValueStore, IndexWrapper, DeferredValue
from .role import Role
from .element import PackageElement, EntityElement



class Instantiable:
  def __init__(self, base=None):
    self._base = base

  @property
  def base(self):
    return self._base

  @property
  def is_instance(self):
    return self._base is not None


class Connectable:
  def __init__(self, is_literal=False):
    self._connections = defaultdict(list)
    self._is_literal = is_literal

  @property
  def is_literal(self):
    return self._is_literal

  def connect_port(self, port_inst, idx=None):
    DFACCTOAssert(port_inst.is_input or port_inst.is_view or len(self._connections[port_inst.role]) == 0,
      'Connectable {} can not be connected to multiple ports of role {}'.format(self, port_inst.role.name))
    self._connections[port_inst.role].append(IndexedObj(port_inst, idx, None))


class Assignable(Connectable):
  def __init__(self, is_literal=False):
    Connectable.__init__(self, is_literal)


class Typed:
  def __init__(self, role, type=None, vector=None, size=None, on_type_set=None):
    self._on_type_set = on_type_set
    self._role = role
    self._type = DeferredValue(self._resolve_type)
    self._vector = DeferredValue(self._resolve_vector)
    self._size = DeferredValue(self._resolve_size)
    self.type_equals(type)
    self.vector_equals(vector)
    self.size_equals(size)

  def adapt(self, other, part_of=None):
    if isinstance(other, Typed):
      self.type_equals(other._type)
      if part_of is None:
        self.vector_equals(other._vector)
        self.size_equals(other._size)
      else:
        self.vector_equals(True)
        self.size_equals(LiteralValue(part_of))
        other.vector_equals(False)
    else:
      if part_of is None:
        self.vector_equals(False)
      else:
        self.vector_equals(True)
        self.size_equals(LiteralValue(part_of))

  def role_equals(self, role):
    new_role = self._role.refine(role)
    if new_role is None:
      raise DFACCTOError('Role "{}" of {} can not be refined with incompatible role "{}"'.format(self.role, self, role))
    self._role = new_role

  def type_equals(self, type):
    if type is None:
      return
    if isinstance(self._type, DeferredValue):
      self._type.assign(type)
    elif isinstance(type, DeferredValue):
      type.assign(self._type)
    elif self._type != type:
      raise DFACCTOError("Type of {} is already set and can not be changed to {}".format(self, type))

  def _resolve_type(self, type):
    self.role_equals(type.role)
    self._type = type
    if self._on_type_set is not None:
      self._on_type_set()

  def vector_equals(self, vector):
    if vector is None:
      return
    if isinstance(self._vector, DeferredValue):
      self._vector.assign(vector)
    elif isinstance(vector, DeferredValue):
      vector.assign(self._vector)
    elif self._vector != vector:
      self_str = 'Vector' if self._vector else 'Scalar'
      other_str = 'vector' if vector else 'scalar'
      raise DFACCTOError("{} is already a {} and can not be changed to a {}".format(self, self_str, other_str))

  def _resolve_vector(self, vector):
    self._vector = vector

  def size_equals(self, size):
    if size is None:
      return
    if isinstance(self._size, DeferredValue):
      self._size.assign(size)
    elif isinstance(size, DeferredValue):
      size.assign(self._size)
    elif self._size != size:
      raise DFACCTOError("Size of {} is already set and can not be changed to {}".format(self, size))

  def _resolve_size(self, size):
    self._size = size


  @property
  def has_role(self):
    return True

  @property
  def role(self):
    return self._role

  @property
  def knows_specific(self):
    return self._role.knows_specific
  @property
  def is_input(self):
    return self._role.is_input
  @property
  def is_output(self):
    return self._role.is_output
  @property
  def is_unidir(self):
    return self._role.is_unidir
  @property
  def is_slave(self):
    return self._role.is_slave
  @property
  def is_master(self):
    return self._role.is_master
  @property
  def is_view(self):
    return self._role.is_view
  @property
  def is_pass(self):
    return self._role.is_pass
  @property
  def is_bidir(self):
    return self._role.is_bidir

  @property
  def knows_complex(self):
    return self._role.knows_complex
  @property
  def is_simple(self):
    return self._role.is_simple
  @property
  def is_complex(self):
    return self._role.is_complex

  @property
  def knows_entity(self):
    return self._role.knows_entity
  @property
  def is_port(self):
    return self._role.is_port
  @property
  def is_const(self):
    return self._role.is_const
  @property
  def is_signal(self):
    return self._role.is_signal

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


  @property
  def knows_type(self):
    return not isinstance(self._type, DeferredValue)

  @property
  def type(self):
    return self._type


  @property
  def knows_vector(self):
    return not isinstance(self._vector, DeferredValue)

  @property
  def is_scalar(self):
    return self._vector is False

  @property
  def is_vector(self):
    return self._vector is True


  @property
  def knows_size(self):
    return not isinstance(self._size, DeferredValue)

  @property
  def size(self):
    return self._size


class LiteralValue(Typed, Assignable):
  def __init__(self, value):
    Typed.__init__(self, Role.Const)
    Assignable.__init__(self, is_literal=True)
    self._value = value

  def __str__(self):
    return str(self._value)

  def __eq__(self, other):
    if isinstance(other, LiteralValue):
      return self._value == other._value
    return False

  @property
  def value(self):
    return self._value


class ValueContainer(Typed):
  def __init__(self, role, type, vector, size, value=None):
    Typed.__init__(self, role, type, vector, size)
    self._value = DeferredValue(self._resolve_value)
    self.value_equals(value)

  @property
  def knows_value(self):
    return not isinstance(self._value, DeferredValue)

  @property
  def raw_value(self):
    return self._value

  @property
  def value(self):
    if not isinstance(self._value, (DeferredValue, abc.Sequence)):
      return self._value
    return None

  @property
  def values(self):
    if isinstance(self._value, abc.Sequence):
      return IndexWrapper(self._value)
    return None

  def value_equals(self, value):
    if value is None:
      return
    if isinstance(self._value, DeferredValue):
      self._value.assign(value)
    elif isinstance(value, DeferredValue):
      value.assign(self._value)
    elif self._value != value:
      raise DFACCTOError('Value of {} is already set and can not be changed to {}'.format(self, value))

  def _resolve_value(self, value):
    if isinstance(value, Assignable):
      self.adapt(value)
    elif isinstance(value, abc.Sequence):
      DFACCTOAssert(all(isinstance(part, Assignable) for part in value),
        'List assignment to {} must only contain assignable elements'.format(self))
      vec = len(value)
      for idx,part in enumerate(value):
        self.adapt(part, part_of=vec)
    else:
      raise DFACCTOError(
        'Assignment to {} must be an assignable element or list of such'.format(self))
    self._value = value


