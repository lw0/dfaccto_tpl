from .util import Registry, IndexWrapper, safe_str
from .signal import Signal
from .port import Port
from .generic import Generic
from .common import Instantiable
from .element import Element, PackageElement



class Instance(Instantiable, Element):
  def __init__(self, entity, parent, name, props):
    new_props = entity.props.copy()
    new_props.update(props)

    Element.__init__(self, entity.context, name, 'i_{name}', new_props)
    Instantiable.__init__(self, entity)
    # EntityCommon.__init__(self)
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
  def parent(self):
    return self._parent

  @property
  def has_role(self):
    return False

  @property
  def generics(self):
    return self._generics

  @property
  def ports(self):
    return self._ports

  @property
  def identifiers(self):
    return self._identifiers

  def assign(self, generic_name, value):
    self.generics.lookup(generic_name).value_equals(value)

  def connect(self, port_name, to):
    self.ports.lookup(port_name).connect(to)


class Entity(Instantiable, Element):
  def __init__(self, context, name, props):
    Element.__init__(self, context, name, '{name}', props)
    Instantiable.__init__(self)
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
      # TODO-lw: require inst.props?
      for generic in inst.generics.contents():
        packages.add(generic.type.package)
        if isinstance(generic.size, PackageElement):
          packages.add(generic.size.package)
        if isinstance(generic.value, PackageElement):
          packages.add(generic.value.package)
        if generic.values:
          for part in generic.values:
            if isinstance(part, PackageElement):
              packages.add(part.package)
      for port in inst.ports.contents():
        packages.add(port.type.package)
        if isinstance(port.size, PackageElement):
          packages.add(port.size.package)
        if isinstance(port.connection, PackageElement):
          packages.add(port.connection.package)
        if port.connections:
          for part in port.connections:
            if isinstance(part, PackageElement):
              packages.add(part.package)
    return IndexWrapper(packages)

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

  def add_generic(self, name, type, size_generic):
    return Generic(self, name, type, size_generic)

  def add_port(self, name, role, type, size_generic):
    return Port(self, name, role, type, size_generic)

  def instantiate(self, parent, name, props):
    return Instance(self, parent, name, props)


