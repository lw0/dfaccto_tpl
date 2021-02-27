from .common import HasProps, ValueContainer
from .element import PackageElement
from .util import DFACCTOAssert, safe_str


class Constant(ValueContainer, PackageElement, HasProps):
  def __init__(self, package, name, type, size_constant_name=None, value=None, *, props):
    self._size_constant = size_constant_name and package.constants.lookup(size_constant_name)

    ValueContainer.__init__(self, type, self._size_constant or False, value)
    PackageElement.__init__(self, package, name, 'c_{name}{dir}')
    HasProps.__init__(self, props)

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
        return '({}).c_{}:{}({}):={}'.format(self.package, self.name, self.type, self.size, self.value)
      else:
        return '({}).c_{}:{}:={}'.format(self.package, self.name, self.type, self.value)
    except:
      return safe_str(self)

  @property
  def size_constant(self):
    return self._size_constant


