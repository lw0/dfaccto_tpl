from .util import Registry, IndexWrapper, safe_str
from .signal import Signal
from .port import Port
from .generic import Generic
from .common import Instantiable
from .element import Element


class EntityCommon:
  def __init__(self):
    self._ports = Registry()
    self._generics = Registry()
    self._instances = Registry()
    self._signals = Registry()
    self._connectables = Registry()
    self._identifiers = Registry()

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
    # TODO-lw also consider constants used as values!
    packages = set()
    for conn in self._connectables.contents():
      packages.add(conn.type.package)
    return IndexWrapper(packages)


class Instance(EntityCommon, Instantiable, Element):
  def __init__(self, entity, parent, name, props):
    new_props = entity.props.copy()
    new_props.update(props)

    Element.__init__(self, entity.context, name, 'i_{name}', new_props)
    Instantiable.__init__(self, entity)
    EntityCommon.__init__(self)
    self._parent = parent

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

  def assign(self, generic_name, value):
    self.generics.lookup(generic_name).value_equals(value)

  def connect(self, port_name, to):
    self.ports.lookup(port_name).connect(to)


class Entity(EntityCommon, Instantiable, Element):
  def __init__(self, context, name, props):
    Element.__init__(self, context, name, '{name}', props)
    Instantiable.__init__(self)
    EntityCommon.__init__(self)

    self.context.entities.register(self.name, self)
    self.context.identifiers.register(self.identifier, self)

  def __str__(self):
    try:
      return self.name
    except:
      return safe_str(self)

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

  def add_port(self, name, type, size_generic):
    return Port(self, name, type, size_generic)

  def instantiate(self, parent, name, props):
    return Instance(self, parent, name, props)


