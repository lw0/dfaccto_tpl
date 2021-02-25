from .util import ValueContainer
from .common import Instantiable, EntityElement, Sized, Typed


class InstGeneric(Typed, Sized, Instantiable, EntityElement, ValueContainer):
  def __init__(self, generic, inst_entity):
    self._size_generic = generic.size_generic and inst_entity.generics.lookup(port.size_generic.name)

    Typed.__init__(self, generic.type)
    Sized.__init__(self, self._size_generic or False) # InstGeneric is ValueContainer and will propagate
    Instantiable.__init__(self, generic)
    EntityElement.__init__(self, inst_entity, generic.name, 'g_{name}{dir}')
    ValueContainer.__init__(self)

    self.entity.generics.register(self.name, self)
    self.entity.identifiers.register(self.identifier, self)

  def __str__(self):
    if self.value is None:
      return '({}).g_{}'.format(self.entity, self.name)
    else:
      return '({}).g_{}={}'.format(self.entity, self.name, self.value)

  @property
  def size_generic(self):
    return self._size_generic


class Generic(Typed, Sized, Instantiable, EntityElement):
  def __init__(self, entity, name, type, size_generic_name=None):
    self._size_generic = size_generic_name and entity.generics.lookup(size_generic_name)
    # Generic or False are not ValueContainers, size will be determined here

    Typed.__init__(self, type)
    Sized.__init__(self, self._size_generic or False)
    Instantiable.__init__(self)
    EntityElement.__init__(self, entity, name, 'g_{name}{dir}')

    self.entity.generics.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    if self.is_vector:
      return '({}).g_{}({}):{}'.format(self.entity, self.name, self.size, self.type)
    else:
      return '({}).g_{}:{}'.format(self.entity, self.name, self.type)

  def instantiate(self, inst_entity):
    return InstGeneric(self, inst_entity)

  @property
  def size_generic(self):
    return self._size_generic



