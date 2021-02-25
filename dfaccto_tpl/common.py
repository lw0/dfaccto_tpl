from collections import defaultdict

from .util import DFACCTOError, DFACCTOAssert, ValueContainer, IndexedObj


class Element:
  def __init__(self, context, name, identifier_pattern, has_vector=False):
    self._context = context
    self._name = name
    self._identifier_pattern = identifier_pattern
    self._identifier = None
    self._identifier_ms = None
    self._identifier_sm = None
    self._identifier_v = None
    self._identifier_v_ms = None
    self._identifier_v_sm = None
    self._has_vector = has_vector

  @property
  def context(self):
    return self._context

  @property
  def name(self):
    return self._name

  @property
  def identifier(self):
    if self._identifier is None:
      if self.has_role:
        if self.is_definite and self.role.is_simple:
          self._identifier = self._identifier_pattern.format(name=self._name,
                                                             mode=self.cmode,
                                                             vec='', dir='')
      else:
        self._identifier = self._identifier_pattern.format(name=self._name,
                                                           mode='',
                                                           vec='', dir='')
    return self._identifier

  @property
  def identifier_ms(self):
    if self._identifier_ms is None:
      if self.has_role and self.is_definite and self.role.is_complex:
        self._identifier_ms = self._identifier_pattern.format(name=self._name,
                                                              mode=self.cmode_ms,
                                                              vec='', dir='_ms')
    return self._identifier_ms

  @property
  def identifier_sm(self):
    if self._identifier_sm is None:
      if self.has_role and self.is_definite and self.role.is_complex:
        self._identifier_sm = self._identifier_pattern.format(name=self._name,
                                                              mode=self.cmode_sm,
                                                              vec='', dir='_sm')
    return self._identifier_sm

  @property
  def identifier_v(self):
    if self._has_vector and self._identifier_v is None:
      if self.has_role:
        if self.is_definite and self.role.is_simple:
          self._identifier_v = self._identifier_pattern.format(name=self._name,
                                                               mode=self.cmode,
                                                               vec='_v', dir='')
      else:
        self._identifier_v = self._identifier_pattern.format(name=self._name,
                                                             mode='',
                                                             vec='_v', dir='')
    return self._identifier_v

  @property
  def identifier_v_ms(self):
    if self._has_vector and self._identifier_v_ms is None:
      if self.has_role and self.is_definite and self.role.is_complex:
        self._identifier_v_ms = self._identifier_pattern.format(name=self._name,
                                                                mode=self.cmode_ms,
                                                                vec='_v', dir='_ms')
    return self._identifier_v_ms

  @property
  def identifier_v_sm(self):
    if self._has_vector and self._identifier_v_sm is None:
      if self.has_role and self.is_definite and self.role.is_complex:
        self._identifier_v_sm = self._identifier_pattern.format(name=self._name,
                                                                mode=self.cmode_sm,
                                                                vec='_v', dir='_sm')
    return self._identifier_v_sm


class EntityElement(Element):
  def __init__(self, entity, name, identifier_pattern, has_vector=False):
    Element.__init__(self, entity.context, name, identifier_pattern, has_vector)
    self._entity = entity

  @property
  def entity(self):
    return self._entity

  @property
  def qualified(self):
    return self.identifier

  @property
  def qualified_ms(self):
    return self.identifier_ms

  @property
  def qualified_sm(self):
    return self.identifier_sm

  @property
  def qualified_v(self):
    return self.identifier_v

  @property
  def qualified_v_ms(self):
    return self.identifier_v_ms

  @property
  def qualified_v_sm(self):
    return self.identifier_v_sm


class PackageElement(Element):
  def __init__(self, package, name, identifier_pattern, has_vector=False):
    Element.__init__(self, package.context, name, identifier_pattern, has_vector)
    self._package = package
    self._qualified = None
    self._qualified_ms = None
    self._qualified_sm = None
    self._qualified_v = None
    self._qualified_v_ms = None
    self._qualified_v_sm = None

  @property
  def package(self):
    return self._package

  @property
  def qualified(self):
    if self._qualified is None:
      ident = self.identifier
      if ident is not None:
        self._qualified = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified

  @property
  def qualified_ms(self):
    if self._qualified_ms is None:
      ident = self.identifier_ms
      if ident is not None:
        self._qualified_ms = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_ms

  @property
  def qualified_sm(self):
    if self._qualified_sm is None:
      ident = self.identifier_sm
      if ident is not None:
        self._qualified_sm = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_sm

  @property
  def qualified_v(self):
    if self._qualified_v is None:
      ident = self.identifier_v
      if ident is not None:
        self._qualified_v = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_v

  @property
  def qualified_v_ms(self):
    if self._qualified_v_ms is None:
      ident = self.identifier_v_ms
      if ident is not None:
        self._qualified_v_ms = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_v_ms

  @property
  def qualified_v_sm(self):
    if self._qualified_v_sm is None:
      ident = self.identifier_v_sm
      if ident is not None:
        self._qualified_v_sm = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_v_sm


class Instantiable:
  def __init__(self, base=None):
    self._base = base

  @property
  def base(self):
    return self._base

  @property
  def is_instance(self):
    return self._base is not None


class HasProps:
  def __init__(self, props=None):
    self._props = props or dict()

  @property
  def props(self):
    return self._props

  def __getattr__(self, key):
    if key.startswith('x_') and key[2:] in self._props:
      return self._props[key[2:]]
    else:
      raise AttributeError(key)


class Typed:
  def __init__(self, type=None, *, on_type_set=None):
    self._type = None
    self._on_type_set = on_type_set
    self._set_type(type)

  def _set_type(self, type):
    if self._type is None:
      self._type = type
      if self._type is not None and self._on_type_set is not None:
        self._on_type_set()
    elif not self._type.is_compatible(type):
      raise DFACCTOError("Type of {} is already set and may not be changed".format(self))

  @property
  def is_definite(self):
    return self._type is not None

  @property
  def has_role(self):
    return True

  # @property
  # def has_type(self):
  #   return self._type is not None

  @property
  def type(self):
    return self._type

  @property
  def role(self):
    return self._type and self._type.role

  @property
  def is_signal(self):
    return self._type is not None and self._type.is_signal

  @property
  def is_port(self):
    return self._type is not None and self._type.is_port

  @property
  def is_input(self):
    return self._type is not None and self._type.is_input

  @property
  def is_output(self):
    return self._type is not None and self._type.is_output

  @property
  def is_simple(self):
    return self._type is not None and self._type.is_simple

  @property
  def is_slave(self):
    return self._type is not None and self._type.is_slave

  @property
  def is_master(self):
    return self._type is not None and self._type.is_master

  @property
  def is_view(self):
    return self._type is not None and self._type.is_view

  @property
  def is_pass(self):
    return self._type is not None and self._type.is_pass

  @property
  def is_complex(self):
    return self._type is not None and self._type.is_complex

  @property
  def mode(self):
    return self._type and self._type.mode

  @property
  def mode_ms(self):
    return self._type and self._type.mode_ms

  @property
  def mode_sm(self):
    return self._type and self._type.mode_sm

  @property
  def cmode(self):
    return self._type and self._type.cmode

  @property
  def cmode_ms(self):
    return self._type and self._type.cmode_ms

  @property
  def cmode_sm(self):
    return self._type and self._type.cmode_sm



class Sized:
  def __init__(self, size=None):
    self._size = ValueContainer(size)

  @property
  def size(self):
    return self._size.value

  @property
  def has_size(self):
    return self._size.value is not None

  @property
  def is_vector(self):
    return self._size.value is not None and bool(self._size.value)

  @property
  def is_scalar(self):
    return self._size.value is not None and not bool(self._size.value)

  def _set_size(self, size):
    try:
      self._size.assign(size)
    except ValueError:
      raise DFACCTOError('Size of {} is already set to {} and can not be changed to {}'.format(self, self._size, size))


class Connectable(Typed, Sized):

  def __init__(self, type=None, size=None, *, on_type_set=None):
    Typed.__init__(self, type, on_type_set=on_type_set)
    Sized.__init__(self, size)

    self._connections = defaultdict(list)

  def connect_port(self, port_inst, idx=None):
    # only signals may have unset types, so use a signal type here
    self._set_type(port_inst.type.base)
    if idx is None:
      self._set_size(port_inst.size)
    else:
      self._set_size(False)

    role = port_inst.type.role
    DFACCTOAssert(role.is_input or role.is_view or not len(self._connections[role]),
      'Signal {} can not be connected to multiple ports of role {}'.format(self, role))
    #TODO-lw make proper distinction between idx and not! perhaps dict()
    self._connections[role].append(IndexedObj(port_inst, idx, None))

  # TODO-lw flatten and IndexWrapper?
  # @property
  # def connections(self):
  #   return self._connections

