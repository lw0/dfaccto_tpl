import collections.abc as abc

from .util import DFACCTOAssert, safe_str
from .common import Instantiable, Typed, ValueContainer, Connectable
from .element import EntityElement
from .role import Role

class InstGeneric(ValueContainer, Instantiable, EntityElement):
  def __init__(self, generic, inst_entity):
    self._size_generic = generic.size_generic and inst_entity.generics.lookup(generic.size_generic.name)

    # InstGeneric is ValueContainer and will propagate
    ValueContainer.__init__(self, generic.type, self._size_generic or False)
    Instantiable.__init__(self, generic)
    EntityElement.__init__(self, inst_entity, generic.name, 'g_{name}{dir}')

    self.entity.generics.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.is_vector:
        if self.has_value:
          return '({}).g_{}:{}({})={}'.format(self.entity, self.name, self.type, self.size, self.value)
        else:
          return '({}).g_{}:{}({})'.format(self.entity, self.name, self.type, self.size)
      else:
        if self.has_value:
          return '({}).g_{}:{}={}'.format(self.entity, self.name, self.type, self.value)
        else:
          return '({}).g_{}:{}'.format(self.entity, self.name, self.type)
    except:
      return safe_str(self)

  @property
  def size_generic(self):
    return self._size_generic

  # adapt() by ValueContainer


class Generic(EntityElement, Typed, Connectable, Instantiable):
  def __init__(self, entity, name, type, size_generic_name=None):
    self._size_generic = size_generic_name and entity.generics.lookup(size_generic_name)
    # Generic or False are not ValueContainers, size will be determined here

    if type.is_complex:
      if type.is_signal:
        type = type.derive(Role.View)
      elif not type.is_view:
        raise DFACCTOError('Complex generics must have view role')
    else:
      if type.is_signal:
        type = type.derive(Role.Input)
      elif not type.is_input:
        raise DFACCTOError('Simple generics must have input role')

    EntityElement.__init__(self, entity, name, 'g_{name}{dir}')
    Typed.__init__(self, type, self._size_generic or False)
    Connectable.__init__(self)
    Instantiable.__init__(self)

    DFACCTOAssert(self._size_generic is None or self._size_generic.is_scalar,
      'Size generic {} for vector generic {} can not itself be a vector'.format(self._size_generic, self))

    self.entity.generics.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.is_vector:
        return '({}).g_{}:{}({})'.format(self.entity, self.name, self.type, self.size)
      else:
        return '({}).g_{}:{}'.format(self.entity, self.name, self.type)
    except:
      return safe_str(self)

  def instantiate(self, inst_entity):
    return InstGeneric(self, inst_entity)

  @property
  def size_generic(self):
    return self._size_generic



