from itertools import chain

from .element import Element, PackageElement
from .generic import Generic
from .port import Port
from .signal import Signal
from .util import Registry, IndexWrapper, safe_str



class Entity(Element):
  def __init__(self, context, name):
    Element.__init__(self, context, name, '{name}')
    self._ports = Registry()
    self._generics = Registry()
    self._instances = Registry()
    self._signals = Registry()
    self._connectables = Registry()
    self._identifiers = Registry()

    self.context.entities.register(self.name, self)
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
  def is_instance(self):
    return False

  @property
  def base(self):
    return None

  @property
  def generics(self):
    return self._generics

  @property
  def ports(self):
    return self._ports

  @property
  def instances(self):
    return self._instances

  @property
  def signals(self):
    return self._signals

  @property
  def connectables(self):
    return self._connectables

  @property
  def identifiers(self):
    return self._identifiers

  @property
  def used_packages(self):
    packages = set()
    for conn in self._connectables.contents():
      packages.add(conn.type.package)
    for prop in self.props.values():
      if isinstance(prop, PackageElement):
        packages.add(prop.package)
    for inst in self._instances.contents():
      for prop in inst.props.values():
        if isinstance(prop, PackageElement):
          packages.add(prop.package)
      for assignment in chain(inst.generics.contents(), inst.ports.contents()):
        packages.add(assignment.type.package)
        if isinstance(assignment.size, PackageElement):
          packages.add(assignment.size.package)
        if isinstance(assignment.assignment, PackageElement):
          packages.add(assignment.assignment.package)
        if assignment.assignments:
          for part in assignment.assignments:
            if isinstance(part, PackageElement):
              packages.add(part.package)
    return IndexWrapper(packages)

  def add_generic(self, name, type, size_generic):
    return Generic(self, name, type, size_generic)

  def add_port(self, name, role, type, size_generic):
    return Port(self, name, role, type, size_generic)

  def instantiate(self, parent, name):
    return Instance(self, parent, name)

  def get_generic(self, name):
    if self.generics.has(name):
      return self.generics.lookup(name)
    else:
      raise DFACCTOError(
        'Entity {} does not have a generic "{}"'.format(self, name))

  def get_assignable(self, name, pkg_name=None):
    if pkg_name is None and self.generics.has(name):
      return self.generics.lookup(name)
    else:
      return self.context.get_constant(name, pkg_name)

  def get_connectable(self, name):
    if self.connectables.has(name):
      return self.connectables.lookup(name)
    return Signal(self, name)


class Instance(Element):
  def __init__(self, entity, parent, name):
    Element.__init__(self, entity.context, name, 'i_{name}')
    self._base = entity
    self._parent = parent
    self._ports = Registry()
    self._generics = Registry()
    self._identifiers = Registry()

    for generic in entity.generics.contents():
      generic.instantiate(self)
    for port in entity.ports.contents():
      port.instantiate(self)

    self._parent.instances.register(self.name, self)
    self._parent.identifiers.register(self.identifier, self)

  def __str__(self):
    try:
      return '({}).i_{}:{}'.format(self.parent, self.name, self.base)
    except:
      return safe_str(self)

  @property
  def has_role(self):
    return False

  @property
  def is_instance(self):
    return True

  @property
  def base(self):
    return self._base

  @property
  def parent(self):
    return self._parent

  @property
  def generics(self):
    return self._generics

  @property
  def ports(self):
    return self._ports

  @property
  def identifiers(self):
    return self._identifiers

  def assign_generic(self, name, value):
    self.generics.lookup(name).assign(value)

  def assign_port(self, name, to):
    self.ports.lookup(name).assign(to)


