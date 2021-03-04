import re

from .entity import Entity
from .package import Package
from .role import Role
from .typed import Literal
from .util import DFACCTOError



class Decoder:

  # g_<name>=...
  GenericPattern = re.compile('g_(\w+)')
  @classmethod
  def generic_key(cls, key):
    if m:= cls.GenericPattern.fullmatch(key):
      return m.group(1) # name
    else:
      return None

  # p<role>_<name>=...
  PortRolePattern = re.compile('p(\w)_(\w+)')
  @classmethod
  def port_role_key(cls, key):
    if m := cls.PortRolePattern.fullmatch(key):
      role = Role.parse(m.group(1))
      if not role.is_port:
        raise DFACCTOError('Invalid port role "{}"'.format(role.name))
      return (m.group(2), role) # name, role
    else:
      return None

  # p_<name>=...
  PortPattern = re.compile('p_(\w+)')
  @classmethod
  def port_key(cls, key):
    if m := cls.PortPattern.fullmatch(key):
      return m.group(1) # name
    else:
      return None

  # x_<name>=...
  PropPattern = re.compile('x_(\w+)')
  @classmethod
  def prop_key(cls, key):
    if m := cls.PropPattern.fullmatch(key):
      return m.group(1) # name
    else:
      return None

  # '[<pkg_name>.]<type_name>[:<size_name>]'
  TypePattern = re.compile('(?:(\w+)\.)?(\w+)(?:\((\w+)\))?')
  @classmethod
  def type_value(cls, value):
    if not isinstance(value, str):
      raise DFACCTOError('Type declaration must be a string')
    if m := cls.TypePattern.fullmatch(value):
      return (m.group(2), m.group(1), m.group(3)) # type_name, pkg_name, size_name
    else:
      raise DFACCTOError('Invalid type declaration "{}"'.format(value))

  # '[<pkg_name>.]<name>'
  RefPattern = re.compile('(?:(\w+)\.)?(\w+)')
  @classmethod
  def ref_value(cls, value):
    if not isinstance(value, str):
      raise DFACCTOError('Reference must be a string')
    if m := cls.RefPattern.fullmatch(value):
      return (m.group(2), m.group(1)) # name, pkg_name
    else:
      raise DFACCTOError('Invalid reference "{}"'.format(value))

  # '<name>'
  NamePattern = re.compile('(\w+)')
  @classmethod
  def name_value(cls, value):
    if not isinstance(value, str):
      raise DFACCTOError('Name must be a string')
    if m := cls.NamePattern.fullmatch(value):
      return m.group(1) # name
    else:
      raise DFACCTOError('Invalid name "{}"'.format(value))

  @classmethod
  def type_role_value(cls, simple=False, complex=False):
    if simple == complex:
      raise DFACCTOError('Type role must be either simple or complex')
    elif simple:
      return False
    else: # complex
      return True

  @classmethod
  def read_props(cls, directives):
    props = list()
    for key,val in directives.items():
      if (name := Decoder.prop_key(key)) is not None:
        props.append((name, val))
      else:
        raise DFACCTOError('Invalid directive "{}"'.format(key))
    return props

  @classmethod
  def read_entity(cls, directives):
    generics = list()
    ports = list()
    props = list()
    for key,val in directives.items():
      if (name := cls.generic_key(key)) is not None:
        type_name, pkg_name, size_name = cls.type_value(val)
        generics.append((name, type_name, pkg_name, size_name))
      elif (res := cls.port_role_key(key)) is not None:
        name, role = res
        type_name, pkg_name, size_name = cls.type_value(val)
        ports.append((name, role, type_name, pkg_name, size_name))
      elif (name := cls.prop_key(key)) is not None:
        props.append((name, val))
      else:
        raise DFACCTOError('Invalid directive "{}"'.format(key))
    return (generics, ports, props)

  @classmethod
  def read_inst(cls, directives):
    generics = list()
    ports = list()
    props = list()
    for key,val in directives.items():
      if (name := cls.generic_key(key)) is not None:
        generics.append((name, val))
      elif (name := cls.port_key(key)) is not None:
        ports.append((name, val))
      elif (name := cls.prop_key(key)) is not None:
        props.append((name, val))
      else:
        raise DFACCTOError('Invalid directive "{}"'.format(key))
    return (generics, ports, props)


class ElementWrapper:
  def __init__(self, frontend, element):
    self._frontend = frontend
    self._element = element

  def __getattr__(self, key):
    return getattr(self._element, key)

  def __str__(self):
    return str(self._element)

  def __enter__(self):
    self._frontend.enter_context(self._element)

  def __exit__(self, type, value, trackback):
    self._frontend.leave_context()

  def unwrap(self):
    return self._element


class Frontend:
  def __init__(self, context):
    self._context = context
    self._package = None
    self._entity = None

  def enter_context(self, element):
    if not self.in_global_context:
      raise DFACCTOError('Can not nest contexts')
    if isinstance(element, Package):
      self._package = element
    elif isinstance(element, Entity):
      self._entity = element
    else:
      raise DFACCTOError('Can not use {} as new context'.format(element))

  def leave_context(self):
    self._package = None
    self._entity = None

  @property
  def in_global_context(self):
    return self._package is None and self._entity is None

  @property
  def in_package_context(self):
    return self._package is not None

  @property
  def in_entity_context(self):
    return self._entity is not None

  def _unpack_prop(self, value):
    value = value() if callable(value) else value
    value = value.unwrap() if isinstance(value, ElementWrapper) else value
    return value

  def literal_reference(self, ref, expand=None):
    if expand is not None and isinstance(ref, str):
      return Literal(ref.format(expand))
    else:
      return Literal(ref)

  def literal_vector_reference(self, *refs, expand=None):
    if expand is not None:
      return tuple(Literal(ref, e) for e in expand for ref in refs)
    else:
      return tuple(Literal(ref) for ref in refs)

  def assignable_reference(self, ref, expand=None):
    name, pkg_name = Decoder.ref_value(ref.format(expand) if expand is not None else ref)
    if self._entity is not None:
      assignable = self._entity.get_assignable(name, pkg_name)
    elif self._package is not None:
      assignable = self._package.get_constant(name, pkg_name)
    else:
      assignable = self._context.get_constant(name, pkg_name)
    return assignable

  def assignable_vector_reference(self, *refs, expand=None):
    if expand is not None:
      return tuple(self.assignable_reference(ref, e) for e in expand for ref in refs)
    else:
      return tuple(self.assignable_reference(ref) for ref in refs)

  def connectable_reference(self, name, expand=None):
    if not self.in_entity_context:
      raise DFACCTOError('Connectable reference must appear in an entity context')
    name = Decoder.name_value(name.format(expand) if expand is not None else name)
    return self._entity.get_connectable(name)

  def connectable_vector_reference(self, *names, expand=None):
    if not self.in_entity_context:
      raise DFACCTOError('Connectable reference must appear in an entity context')
    if expand is not None:
      return tuple(self.connectable_reference(name, e) for e in expand for name in names)
    else:
      return tuple(self.connectable_reference(name) for name in names)

  def global_statement(self, **directives):
    if not self.in_global_context:
      raise DFACCTOError('Global statement must appear in the global context')
    props = Decoder.read_props(directives)

    for name,value in props:
      self._context.set_prop(name, self._unpack_prop(value))
    # TODO-lw deep update, so that multiple Gbl(x_templates={...}) extend templates dir!

  def package_declaration(self, name, **directives):
    if not self.in_global_context:
      raise DFACCTOError('Package declaration must appear in the global context')
    name = Decoder.name_value(name)
    props = Decoder.read_props(directives)

    package = self._context.add_or_get_package(name)
    for name, value in props:
      package.set_prop(name, self._unpack_prop(value))

    return ElementWrapper(self, package)

  def type_declaration(self, name, simple=False, complex=False, **directives):
    if not self.in_package_context:
      raise DFACCTOError('Type declaration must appear in a package context')
    name = Decoder.name_value(name)
    is_complex = Decoder.type_role_value(simple, complex)
    props = Decoder.read_props(directives)

    type = self._package.add_type(name, is_complex)
    for name, value in props:
      type.set_prop(name, self._unpack_prop(value))

    return ElementWrapper(self, type)

  def constant_declaration(self, name, type, value=None, **directives):
    if not self.in_package_context:
      raise DFACCTOError('Constant declaration must appear in a package context')
    name = Decoder.name_value(name)
    type_name, pkg_name, size_name = Decoder.type_value(type)
    props = Decoder.read_props(directives)

    type = self._package.get_type(type_name, pkg_name)
    size = size_name and self._package.get_constant(size_name, self._package.name)
    constant = self._package.add_constant(name, type, size, value)
    for name, value in props:
      constant.set_prop(name, self._unpack_prop(value))

    return ElementWrapper(self, constant)

  def entity_declaration(self, name, **directives):
    if not self.in_global_context:
      raise DFACCTOError('Entity declaration must appear in the global context')
    name = Decoder.name_value(name)
    generics, ports, props = Decoder.read_entity(directives)

    entity = self._context.add_entity(name)
    for name, type_name, pkg_name, size_name in generics:
      type = self._context.get_type(type_name, pkg_name)
      size = size_name and entity.get_generic(size_name)
      entity.add_generic(name, type, size)
    for name, role, type_name, pkg_name, size_name in ports:
      type = self._context.get_type(type_name, pkg_name)
      size = size_name and entity.get_generic(size_name)
      entity.add_port(name, role, type, size)
    for name, value in props:
      entity.set_prop(name, self._unpack_prop(value))

    return ElementWrapper(self, entity)

  def instance_declaration(self, entity_name, name=None, index=None, **directives):
    if not self.in_entity_context:
      raise DFACCTOError('Instance declaration must appear in an entity context')
    entity_name = Decoder.name_value(entity_name)
    if name is None:
      name = entity_name[0].lower() + entity_name[1:]
    if index is not None:
      name = '{}{:d}'.format(name, index)
    inst_name = self._entity.instances.unique_name(name)
    generics, ports, props = Decoder.read_inst(directives)

    entity = self._context.get_entity(entity_name)
    instance = entity.instantiate(self._entity, inst_name)
    for name,value in generics:
      instance.assign_generic(name, value)
    for name,to in ports:
      instance.assign_port(name, to)
    for name, value in props:
      instance.set_prop(name, self._unpack_prop(value))

    return ElementWrapper(self, instance)

