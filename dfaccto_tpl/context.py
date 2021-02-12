from .common import HasProps
from .util import DFACCTOError, Registry


class Context(HasProps):

  def __init__(self):
    HasProps.__init__(self)
    self._identifiers = Registry()
    self._packages = Registry('package')
    self._entities = Registry('entity')

  def clear(self):
    self._identifiers.clear()
    self._packages.clear()
    self._entities.clear()
    self.props.clear()

  def __str__(self):
    return '<global>'

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
    return self.entities.lookup(entity_name)

  def get_type(self, type_name, pkg_name=None):
    type = None
    if pkg_name is None:
      for pkg in self._packages.contents():
        if pkg.types.has(type_name):
          if type is not None:
            raise DFACCTOError('Unqualified type reference "{}" is ambiguous: {}, {}'.format(type_name, pkg, type.package))
          else:
            type = pkg.types.lookup(type_name)
      if type is None:
        raise DFACCTOError('Unqualified type reference "{}" can not be found in any package'.format(type_name))
    else:
      pkg = self._packages.lookup(pkg_name)
      type = pkg.types.lookup(type_name)
    return type



