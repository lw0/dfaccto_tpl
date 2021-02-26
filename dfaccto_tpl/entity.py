from .util import Registry, IndexWrapper, safe_str
from .signal import Signal
from .port import Port
from .generic import Generic
from .common import Instantiable, HasProps
from .element import Element

class EntityCommon(HasProps):
  def __init__(self, props):
    HasProps.__init__(self, props)

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
  def has_generics(self):
    return len(self._generics) > 0


  @property
  def ports(self):
    return self._ports

  @property
  def has_ports(self):
    return len(self._ports) > 0


  @property
  def instances(self):
    return self._instances

  @property
  def has_instances(self):
    return len(self._instances) > 0


  @property
  def signals(self):
    return self._signals

  @property
  def has_signals(self):
    return len(self._signals) > 0


  @property
  def connectables(self):
    return self._connectables

  @property
  def used_packages(self):
    packages = set()
    for conn in self._connectables.contents():
      packages.add(conn.type.package)
    return IndexWrapper(packages)


  @property
  def identifiers(self):
    return self._identifiers


class InstEntity(EntityCommon, Instantiable, Element):
  def __init__(self, entity, parent, name):
    Element.__init__(self, entity.context, name, 'i_{name}')
    Instantiable.__init__(self, entity)
    EntityCommon.__init__(self, entity.props)
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
    self.generics.lookup(generic_name).assign(value)

  def connect(self, port_name, to):
    self.ports.lookup(port_name).connect(to)


class Entity(EntityCommon, Instantiable, Element):
  def __init__(self, context, name, **props):
    Element.__init__(self, context, name, '{name}')
    Instantiable.__init__(self)
    EntityCommon.__init__(self, props)

    self.context.entities.register(self.name, self)
    self.context.identifiers.register(self.identifier, self)


  def __str__(self):
    try:
      return self.name
    except:
      return safe_str(self)

  def generic(self, name, type, size_generic_name):
    return Generic(self, name, type, size_generic_name)

  def port(self, name, type, size_generic_name=None):
    return Port(self, name, type, size_generic_name)

  def instantiate(self, parent, name):
    return InstEntity(self, parent, name)

  def get_connectable(self, name):
    if self.connectables.has(name):
      return self.connectables.lookup(name)
    return Signal(self, name)



