from .constant import Constant
from .element import Element, PackageElement
from .type import Type
from .util import Registry, safe_str, IndexWrapper



class Package(Element):

  def __init__(self, context, name):
    Element.__init__(self, context, name, '{name}')

    self._types = Registry()
    self._constants = Registry()
    self._declarations = Registry()
    self._identifiers = Registry()

    self.context.packages.register(self.name, self)
    self.context.identifiers.register(self.identifier, self)

  def __str__(self):
    try:
      return self.name
    except:
      return safe_str(self)

  @property
  def has_role(self):
    return False

  @property
  def types(self):
    return self._types

  @property
  def constants(self):
    return self._constants

  @property
  def declarations(self):
    return self._declarations

  @property
  def identifiers(self):
    return self._identifiers

  @property
  def used_packages(self):
    packages = set()
    for decl in self._declarations.contents():
      for prop in decl.props:
        if isinstance(prop, PackageElement):
          packages.add(prop.package)
      if isinstance(decl, Constant):
        packages.add(decl.type.package)
        if isinstance(decl.size, PackageElement):
          packages.add(decl.size.package)
        if isinstance(decl.assignment, PackageElement):
          packages.add(decl.assignment.package)
        if decl.assignments:
          for part in decl.assignments:
            if isinstance(part, PackageElement):
              packages.add(part.package)
    packages.remove(self)
    return IndexWrapper(packages)

  def add_type(self, name, is_complex):
    return Type(self, name, is_complex)

  def add_constant(self, name, type, size, value):
    return Constant(self, name, type, size, value)

  def get_type(self, name, pkg_name=None):
    if pkg_name is None and self.types.has(name):
      return self.types.lookup(name)
    else:
      return self.context.get_type(name, pkg_name)

  def get_constant(self, name, pkg_name=None):
    if pkg_name is None and self.constants.has(name):
      return self.constants.lookup(name)
    else:
      return self.context.get_constant(name, pkg_name)


