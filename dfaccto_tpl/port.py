import collections.abc as abc

from .util import DFACCTOAssert, IndexWrapper, DFACCTOError, safe_str
from .common import Typed, Connectable, Instantiable
from .element import EntityElement


class InstPort(Typed, Instantiable, EntityElement):
  def __init__(self, port, inst_entity):
    size = inst_entity.generics.lookup(port.size.name) if port.is_vector else None

    EntityElement.__init__(self, inst_entity, port.name, 'p{mode}_{name}{dir}')
    Instantiable.__init__(self, port)
    # size.raw_value may be DeferredValue and will propagate if necessary
    Typed.__init__(self, port.type, size is not None, size and size.raw_value)

    self._connection = None

    self.entity.ports.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.is_vector:
        if self._connection is None:
          return '({}).p_{}:{}({})'.format(self.entity, self.name, self.type, self.size)
        else:
          return '({}).p_{}:{}({})=>{}'.format(self.entity, self.name, self.type, self.size, self._connection)
      else:
        if self._connection is None:
          return '({}).p_{}:{}'.format(self.entity, self.name, self.type)
        else:
          return '({}).p_{}:{}=>{}'.format(self.entity, self.name, self.type, self._connection)
    except AttributeError:
      return safe_str(self)

  def connect(self, to):
    DFACCTOAssert(self._connection is None or self._connection == to,
      'Can not reconnect port {} to {}'.format(self, to))

    if isinstance(to, Connectable):
      self.adapt(to)
      to.connect_port(self)
    elif isinstance(to, abc.Sequence):
      DFACCTOAssert(all(isinstance(part, Connectable) for part in to),
        'List connection to port {} must only contain connectable elements'.format(self))
      vec = len(to)
      for idx, part in enumerate(to):
        self.adapt(part, part_of=vec)
        part.connect_port(self, idx)
    else:
      raise DFACCTOError(
        'Connection to port {} must be a connectable element or list of such'.format(self))

    self._connection = to

  @property
  def is_port(self):
    return True

  @property
  def connection(self):
    if isinstance(self._connection, Connectable):
      return self._connection
    return None

  @property
  def connections(self):
    if isinstance(self._connection, abc.Sequence):
      return IndexWrapper(self._connection)
    return None

  @property
  def is_connected(self):
    return self._connection is not None


class Port(EntityElement, Typed, Connectable, Instantiable):
  def __init__(self, entity, name, type, size_generic):
    if size_generic is not None:
      size_generic.vector_equals(False)

    EntityElement.__init__(self, entity, name, 'p{mode}_{name}{dir}')
    Typed.__init__(self, type, size_generic is not None, size_generic)
    Connectable.__init__(self)
    Instantiable.__init__(self)

    self.entity.ports.register(self.name, self)
    self.entity.connectables.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.is_vector:
        return '({}).p_{}:{}({})'.format(self.entity, self.name, self.type, self.size)
      else:
        return '({}).p_{}:{}'.format(self.entity, self.name, self.type)
    except:
      return safe_str(self)

  def instantiate(self, inst_entity):
    return InstPort(self, inst_entity)

  @property
  def is_port(self):
    return True


