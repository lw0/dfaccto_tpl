from collections import defaultdict
import collections.abc as abc

from .util import DFACCTOError, DFACCTOAssert, IndexedObj, ValueStore



class Instantiable:
  def __init__(self, base=None):
    self._base = base

  @property
  def base(self):
    return self._base

  @property
  def is_instance(self):
    return self._base is not None


class HasProps:
  def __init__(self, props=None):
    self._props = props or dict()

  @property
  def props(self):
    return self._props

  def __getattr__(self, key):
    if key.startswith('x_') and key[2:] in self._props:
      return self._props[key[2:]]
    else:
      raise AttributeError(key)


class Typed:
  def __init__(self, type=None, size=None, *, on_type_set=None):
    # size may be None (unknown if vector), False (scalar), ValueContainer (vector), others wrapped in ValueContainer
    self._type = type
    self._on_type_set = on_type_set
    self._type = None
    self._set_type(type)
    self._size = None
    self._set_size(size)

  def adapt(self, other, part_of=None):
    # concerns: check type and multiplicity compatibility
    if isinstance(other, Typed):
      if self._type is None:
        # only signals may have unset types, so use a signal type here
        self._set_type(other._type.base)
      elif other._type is None:
        # only signals may have unset types, so use a signal type here
        other._set_type(self._type.base)
      elif not self._type.base.is_compatible(other._type):
        raise DFACCTOError("Type of {} is incompatible with {}".format(self, other))

      if part_of is None:
        if self.knows_cardinality and other.knows_cardinality:
          if self.is_scalar and other.is_scalar:
            pass #nothing to do, as both _size fields are already set
          elif self.is_vector and other.is_vector:
            if self.knows_size and other.knows_size:
              DFACCTOAssert(self.size == other.size,
                'Can not adapt vector {} to vector {} of different size'.format(self, other))
            elif other.knows_size:
              other._set_size(self._size)
            else: # only other knows size or both do not know
              self._set_size(other._size)
          elif self.is_vector:
            raise DFACCTOError(
              'Can not adapt vector {} to scalar {}'.format(self, other))
          else: # self.is_scalar
            raise DFACCTOError(
              'Can not adapt scalar {} to vector {}'.format(self, other))
        elif self.knows_cardinality:
          other._set_size(self._size)
        elif other.knows_cardinality:
          self._set_size(other._size)
        # impossible that neither knows cardinality,
        # as only signals can be in this state
        # and they can not be connected together
      else:
        if self.knows_cardinality:
          DFACCTOAssert(self.is_vector,
            'Can not adapt scalar {} to partial'.format(self))
          if self.knows_size:
            DFACCTOAssert(self.size == part_of,
              'Can not adapt vector {} to partial of {} elements'.format(self, part_of))
          else:
            self._set_size(part_of)
        else:
          self._set_size(part_of)
        if other.knows_cardinality:
          DFACCTOAssert(other.is_scalar,
            'Can not adapt vector {} as partial, which must be scalar.'.format(other))
        else:
          other._set_size(False)
    else:
      # Only ValueContainers may adapt to plain values and ValueContainers have explicit types
      # thus self.has_type should be True here
      DFACCTOAssert(self.knows_type,
        'Untyped {} can not adapt to plain value "{}"'.format(self, other))

      # plain values are considered untyped scalars
      #  unless part_of specifies an untyped vector
      # do not touch _type
      if part_of is None:
        other_is_sequence = isinstance(other, abc.Sequence) and not isinstance(other, str)
        if self.knows_cardinality:
          if self.is_scalar and not other_is_sequence:
            pass # _size already correctly set to False
          elif self.is_vector and other_is_sequence:
            if self.knows_size:
              DFACCTOAssert(self.size == len(other),
                'Can not adapt vector {} to list "{}" of different length {}'.format(self, other, len(other)))
            else:
              self._set_size(len(other))
          elif self.is_vector:
            raise DFACCTOError(
              'Can not adapt vector {} to non-list "{}"'.format(self, other))
          else: # self.is_vector
            raise DFACCTOError(
              'Can not adapt scalar {} to list "{}"'.format(self, other))
        else:
          self._set_size(other_is_sequence and len(other))
      else:
        if self.knows_cardinality:
          DFACCTOAssert(self.is_vector,
            'Can not adapt scalar {} to partial'.format(self))
          if self.knows_size:
            DFACCTOAssert(self.size == part_of,
              'Can not adapt vector {} to partial of {} elements'.format(self, part_of))
          else:
            self._set_size(part_of)
        else:
          self._set_size(part_of)

  def _set_type(self, type):
    self._type = type
    if self._type is not None and self._on_type_set is not None:
      self._on_type_set()

  def _set_size(self, size):
    if self._size is None:
      if size is None:
        pass # unknown size has no effect
      elif size is False:
        self._size = False
      elif isinstance(size, ValueContainer):
        DFACCTOAssert(size.is_scalar,
          'Can not use vector {} as size for vector {}'.format(size, self))
        self._size = size
      else:
        # TODO-lw: _size must have a simple type, but type=None here
        #  also allows complex types!
        self._size = ValueContainer(type=None, size=False, value=size)
    elif isinstance(self._size, ValueContainer):
      self._size.assign(size)
    else: # self._size is False
      DFACCTOAssert(size is None or size is False,
        'Can not set size of scalar {} to {}'.format(self, size))


  @property
  def has_role(self):
    return True

  @property
  def knows_role(self):
    return self._type is not None

  @property
  def role(self):
    return self._type and self._type.role


  @property
  def knows_type(self):
    return self._type is not None

  @property
  def type(self):
    return self._type

  @property
  def is_signal(self):
    return self._type is not None and self._type.is_signal

  @property
  def is_port(self):
    return self._type is not None and self._type.is_port

  @property
  def is_input(self):
    return self._type is not None and self._type.is_input

  @property
  def is_output(self):
    return self._type is not None and self._type.is_output

  @property
  def is_simple(self):
    return self._type is not None and self._type.is_simple

  @property
  def is_slave(self):
    return self._type is not None and self._type.is_slave

  @property
  def is_master(self):
    return self._type is not None and self._type.is_master

  @property
  def is_view(self):
    return self._type is not None and self._type.is_view

  @property
  def is_pass(self):
    return self._type is not None and self._type.is_pass

  @property
  def is_complex(self):
    return self._type is not None and self._type.is_complex

  @property
  def mode(self):
    return self._type and self._type.mode

  @property
  def mode_ms(self):
    return self._type and self._type.mode_ms

  @property
  def mode_sm(self):
    return self._type and self._type.mode_sm

  @property
  def cmode(self):
    return self._type and self._type.cmode

  @property
  def cmode_ms(self):
    return self._type and self._type.cmode_ms

  @property
  def cmode_sm(self):
    return self._type and self._type.cmode_sm


  @property
  def knows_cardinality(self):
    return self._size is not None

  @property
  def is_scalar(self):
    return self._size is False

  @property
  def is_vector(self):
    return isinstance(self._size, ValueContainer)

  @property
  def knows_size(self):
    return isinstance(self._size, ValueContainer) and self._size.value is not None

  @property
  def size(self):
    return self._size.value if isinstance(self._size, ValueContainer) else None


class ValueContainer(Typed, ValueStore):
  def __init__(self, type, size, value=None):
    self._idx = self._create()
    Typed.__init__(self, type, size)
    if value is not None:
      self.assign(value)

  @property
  def value(self):
    return self._get_value(self._idx) if self.is_simple else None

  @property
  def value_ms(self):
    val = self._get_value(self._idx)
    return val and val[0] if self.is_complex else None

  @property
  def value_sm(self):
    val = self._get_value(self._idx)
    return val and val[1] if self.is_complex else None

  @property
  def has_value(self):
    return self._get_value(self._idx) is not None

  def assign(self, other):
    self.adapt(other)
    if isinstance(other, ValueContainer):
      self._assign(self._idx, other._idx)
    else:
      if self.is_complex:
        DFACCTOAssert(isinstance(other, abc.Mapping) and 'ms' in other and 'sm' in other,
          'Complex {} must be assigned a mapping with "ms" and "sm" entries'.format(self))
        self._set_value(self._idx, (other['ms'], other['sm']))
      else: #self.is_simple
        self._set_value(self._idx, other)


class Connectable:
  def __init__(self):
    self._connections = defaultdict(list)

  def connect_port(self, port_inst, idx=None):
    if self.has_role:
      DFACCTOAssert(self.role.is_compatible(port_inst.role),
        'Can not connect {} {} to {} {}'.format(self.role.name, self, port_inst.role.name, port_inst))
    DFACCTOAssert(port_inst.is_input or port_inst.is_view or len(self._connections[port_inst.role]) == 0,
      'Connectable {} can not be connected to multiple ports of role {}'.format(self, port_inst.role.name))
    self._connections[port_inst.role].append(IndexedObj(port_inst, idx, None))

  # TODO-lw flatten and IndexWrapper?
  # @property
  # def connections(self):
  #   return self._connections

