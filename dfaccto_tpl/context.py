from .util import DFACCTOError, Registry, safe_str


class Context:

  def __init__(self):
    self._props = dict()
    self._identifiers = Registry()
    self._packages = Registry()
    self._entities = Registry()

  def clear(self):
    self._props.clear()
    self._identifiers.clear()
    self._packages.clear()
    self._entities.clear()

  def __str__(self):
    try:
      return '<global>'
    except:
      return safe_str(self)

  def __getattr__(self, key):
    if key.startswith('x_') and key[2:] in self._props:
      return self._props[key[2:]]
    else:
      raise AttributeError(key)

  # def extend_props(self, more_props):
  #   pass

  @property
  def props(self):
    return self._props

  @property
  def identifiers(self):
    return self._identifiers

  @property
  def packages(self):
    return self._packages

  @property
  def entities(self):
    return self._entities

  def get_entity(self, entity_name):
    if self._entities.has(entity_name):
      return self._entities.lookup(entity_name)
    else:
      raise DFACCTOError('Entity reference "{}" can not be found'.format(entity_name))

  def get_type(self, type_name, pkg_name=None):
    type = None
    if pkg_name is None:
      for pkg in self._packages.contents():
        if pkg.types.has(type_name):
          if type is not None:
            raise DFACCTOError('Unqualified type reference "{}" is ambiguous (Packages {}, {})'.format(type_name, pkg, type.package))
          else:
            type = pkg.types.lookup(type_name)
      if type is None:
        raise DFACCTOError('Unqualified type reference "{}" can not be found in any package'.format(type_name))
    else:
      pkg = self._packages.lookup(pkg_name)
      type = pkg.types.lookup(type_name)
    return type

  def get_constant(self, const_name, pkg_name=None):
    constant = None
    if pkg_name is None:
      for pkg in self._packages.contents():
        if pkg.constants.has(const_name):
          if constant is not None:
            raise DFACCTOError('Unqualified constant reference "{}" is ambiguous (Packages {}, {})'.format(const_name, pkg, constant.package))
          else:
            constant = pkg.constants.lookup(const_name)
      if constant is None:
        raise DFACCTOError('Unqualified constant reference "{}" can not be found in any package'.format(type_name))
    else:
      pkg = self._packages.lookup(pkg_name)
      constant = pkg.constants.lookup(type_name)
    return constant



