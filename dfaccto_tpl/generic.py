import collections.abc as abc

from .util import DFACCTOAssert, safe_str
from .common import Instantiable, Typed, ValueContainer, Assignable
from .element import EntityElement
from .role import Role


class InstGeneric(ValueContainer, Instantiable, EntityElement):
  def __init__(self, generic, inst_entity):
    size = inst_entity.generics.lookup(generic.size.name) if generic.is_vector else None

    # size_generic_inst.raw_value may be DeferredValue and will propagate if necessary
    ValueContainer.__init__(self, generic.type, size is not None, size and size.raw_value)
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
  def is_generic(self):
    return True


class Generic(EntityElement, Typed, Instantiable, Assignable):
  def __init__(self, entity, name, type, size_generic):
    if size_generic is not None:
      size_generic.vector_equals(False)

    if type.is_complex:
      if not type.is_directed:
        type = type.derive(Role.View)
      elif not type.is_view:
        raise DFACCTOError('Complex generics must have view role')
    else:
      if not type.is_directed:
        type = type.derive(Role.Input)
      elif not type.is_input:
        raise DFACCTOError('Simple generics must have input role')

    EntityElement.__init__(self, entity, name, 'g_{name}{dir}')
    # Generic or False are not ValueContainers, size will be determined here
    Typed.__init__(self, type, size_generic is not None, size_generic)
    Assignable.__init__(self)
    Instantiable.__init__(self)

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
  def is_generic(self):
    return True


