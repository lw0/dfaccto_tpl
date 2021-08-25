from .assignable import Assignable
from .assignment import Assignment
from .element import EntityElement
from .role import Role
from .typed import TypedWithDefault
from .util import DFACCTOError, safe_str, IndexWrapper



class Port(EntityElement, TypedWithDefault, Assignable):
  def __init__(self, entity, name, role, type, size_generic, default):
    if size_generic is not None:
      # Generics used for size must be simple scalars
      size_generic.role_equals(Role.Simple)
      size_generic.vector_equals(False)

    EntityElement.__init__(self, entity, name, 'p{mode}_{name}{dir}', inst_type=InstPort)
    TypedWithDefault.__init__(self, role, type, size_generic is not None, size_generic, default)
    Assignable.__init__(self)

    self.entity.ports.register(self.name, self)
    self.entity.connectables.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.has_default:
        def_str = ':={}'.format(str(self.default))
      else:
        def_str = ''
      if self.is_vector:
        return '({}).p_{}:{}({}){}'.format(self.entity, self.name, self.type, self.size, def_str)
      else:
        return '({}).p_{}:{}{}'.format(self.entity, self.name, self.type, def_str)
    except:
      return safe_str(self)

  def usage_deps(self, deps, visited):
    EntityElement.usage_deps(self, deps, visited)
    TypedWithDefault.usage_deps(self, deps, visited)


class InstPort(EntityElement, Assignment):
  def __init__(self, port, inst_entity):
    size = inst_entity.generics.lookup(port.size.name) if port.is_vector else None

    EntityElement.__init__(self, inst_entity, port.name, 'p{mode}_{name}{dir}', base=port)
    # size.raw_value may be DeferredValue and will propagate if necessary
    Assignment.__init__(self, Assignable, port.role, port.type, size is not None, size and size.raw_value)

    self.entity.ports.register(self.name, self)
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.is_vector:
        if self.is_assigned is None:
          return '({}).p_{}:{}({})'.format(self.entity, self.name, self.type, self.size)
        else:
          return '({}).p_{}:{}({})=>{}'.format(self.entity, self.name, self.type, self.size, self.raw_value)
      else:
        if self.is_assigned is None:
          return '({}).p_{}:{}'.format(self.entity, self.name, self.type)
        else:
          return '({}).p_{}:{}=>{}'.format(self.entity, self.name, self.type, self.raw_value)
    except AttributeError:
      return safe_str(self)

  def usage_deps(self, deps, visited):
    EntityElement.usage_deps(self, deps, visited)
    Assignment.usage_deps(self, deps, visited)

