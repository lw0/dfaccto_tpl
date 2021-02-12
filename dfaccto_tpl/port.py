import collections.abc as abc

from .util import DFACCTOAssert, IndexWrapper
from .common import Typed, Sized, Connectable, Instantiable, EntityElement


class InstPort(Typed, Sized, Instantiable, EntityElement):
  def __init__(self, port, inst_entity):
    inst_size_generic = port.size_generic and inst_entity.generics.lookup(port.size_generic.name)
    EntityElement.__init__(self, inst_entity, port.name, 'p{mode}_{name}{dir}')
    Instantiable.__init__(self, port)
    Sized.__init__(self, inst_size_generic or False) # inst_size_generic is ValueContainer and will propagate
    Typed.__init__(self, port.type, on_type_set=self._register_identifiers)

    self._size_generic = inst_size_generic
    self._connection = None

    self.entity.ports.register(self.name, self)

  def _register_identifiers(self):
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    if self.is_vector:
      if self._connection is None:
        return '({}).p_{}({}):{}'.format(self.entity, self.name, self.size, self.type)
      else:
        return '({}).p_{}({}):{}=>{}'.format(self.entity, self.name, self.size, self.type, self._connection)
    else:
      if self._connection is None:
        return '({}).p_{}:{}'.format(self.entity, self.name, self.type)
      else:
        return '({}).p_{}:{}=>{}'.format(self.entity, self.name, self.type, self._connection)

  def connect(self, to):
    DFACCTOAssert(self._connection is None or self._connection == to,
      'Can not reconnect port {} to {}'.format(self, to))

    if isinstance(to, Connectable):
      to.connect_port(self)
    elif isinstance(to, abc.Sequence):
      DFACCTOAssert(all(isinstance(part, Connectable) for part in to),
        "Vector port {} connection list expects ports or signals".format(self))
      for idx, connectable in enumerate(to):
        connectable.connect_port(self, idx)
      self._size_generic.assign(len(to))
    else:
      DFACCTOAssert(False,
        "Vector port {} connection expects a port, signal or list of those".format(self))

    self._connection = to

  @property
  def size_generic(self):
    return self._size_generic

  @property
  def connection(self):
    if isinstance(self._connection, Connectable):
      return self._connection
    return None

  @property
  def connections(self):
    if isinstance(self._connection, abc.Sequence):
      return IndexWrapper(self._connection, 'connection')
    return None

  @property
  def is_connected(self):
    return self._connection is not None


class Port(Connectable, Instantiable, EntityElement):
  def __init__(self, entity, name, type, size_generic_name=None):
    size_generic = None
    size = False
    if size_generic_name is not None:
      size_generic = entity.generics.lookup(size_generic_name)
      size = size_generic.identifier
    # Generic identifier or False are not ValueContainers, size will be determined here

    EntityElement.__init__(self, entity, name, 'p{mode}_{name}{dir}')
    Instantiable.__init__(self)
    Connectable.__init__(self, type, size, on_type_set=self._register_identifiers)

    self._size_generic = size_generic

    self.entity.ports.register(self.name, self)
    self.entity.connectables.register(self.name, self)

  def _register_identifiers(self):
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self): #TODO-lw add vector info
    if self.is_vector:
      return '({}).p_{}({}):{}'.format(self.entity, self.name, self.size, self.type)
    else:
      return '({}).p_{}:{}'.format(self.entity, self.name, self.type)

  def instantiate(self, inst_entity):
    return InstPort(self, inst_entity)

  @property
  def size_generic(self):
    return self._size_generic


