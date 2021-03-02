from .util import Registry, safe_str, IndexWrapper
from .element import Element, PackageElement
from .type import Type
from .constant import Constant


class Package(Element):

  def __init__(self, context, name, props):
    Element.__init__(self, context, name, '{name}', props)

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
        if isinstance(decl.value, PackageElement):
          packages.add(decl.value.package)
        if decl.values:
          for part in decl.values:
            if isinstance(part, PackageElement):
              packages.add(part.package)
    packages.remove(self)
    return IndexWrapper(packages)

  def get_type(self, type_name, pkg_name=None):
    if pkg_name is None and self.types.has(type_name):
      return self.types.lookup(type_name)
    else:
      return self.context.get_type(type_name, pkg_name)

  def get_constant(self, const_name, pkg_name=None):
    if pkg_name is None and self.constants.has(const_name):
      return self.constants.lookup(const_name)
    else:
      return self.context.get_constant(const_name, pkg_name)

  def add_type(self, name, is_complex, props):
    return Type(self, name, is_complex, props)

  def add_constant(self, name, type, size, value, props):
    return Constant(self, name, type, size, value, props=props)


