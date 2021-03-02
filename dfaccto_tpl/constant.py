from .common import ValueContainer, Connectable, Assignable
from .element import PackageElement
from .util import DFACCTOAssert, safe_str
from .role import Role


class Constant(PackageElement, ValueContainer, Connectable, Assignable):
  def __init__(self, package, name, type, size_constant, value=None, *, props):
    if size_constant is not None:
      size_constant.vector_equals(False)

    if type.is_complex:
      if not type.is_directed:
        type = type.derive(Role.View)
      elif not type.is_view:
        raise DFACCTOError('Complex constants must have view role')
    else:
      if not type.is_directed:
        type = type.derive(Role.Input)
      elif not type.is_input:
        raise DFACCTOError('Simple constants must have input role')

    PackageElement.__init__(self, package, name, 'c_{name}{dir}', props)
    ValueContainer.__init__(self, type, size_constant is not None, size_constant and size_constant.raw_value, value)
    Connectable.__init__(self)
    self._size_constant = size_constant

    self.package.constants.register(self.name, self)
    decl_name = self.package.declarations.unique_name(self.name) # Avoid collisions with type names
    self.package.declarations.register(decl_name, self)
    if self.is_complex:
      self.package.identifiers.register(self.identifier_ms, self)
      self.package.identifiers.register(self.identifier_sm, self)
    else:
      self.package.identifiers.register(self.identifier, self)

  def __str__(self):
    try:
      if self.is_vector:
        return '({}).c_{}:{}({}):={}'.format(self.package, self.name, self.type, self.size_constant, self.value)
      else:
        return '({}).c_{}:{}:={}'.format(self.package, self.name, self.type, self.value)
    except:
      return safe_str(self)

  @property
  def is_constant(self):
    return True

  @property
  def size_constant(self):
    return self._size_constant


