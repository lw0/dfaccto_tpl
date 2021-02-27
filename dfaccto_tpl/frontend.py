import collections.abc as abc
import re

from .util import DFACCTOAssert, DFACCTOError
from .role import Role
from .type import Type
from .entity import Entity
from .signal import Signal
from .package import Package


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
      return (m.group(2), Role.parse(m.group(1))) # name, role
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

    # if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], str) and isinstance(value[1], str):
    #   return (value[0], value[1]) # type_name, size_name
    # elif isinstance(value, str):
    #   return (value, None)
    # else:
    #   return None

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
      return Role.Simple
    else: # complex
      return Role.Complex

  @classmethod
  def read_props(cls, directives):
    props = dict()
    for key,val in directives.items():
      if (res := Decoder.prop_key(key)) is not None:
        name = res
        props[name] = val
      else:
        raise DFACCTOError('Invalid directive "{}"'.format(key))
    return props

  @classmethod
  def read_entity(cls, directives):
    generics = list()
    ports = list()
    props = dict()
    for key,val in directives.items():
      if (res := cls.generic_key(key)) is not None:
        name = res
        type_name, pkg_name, size_name = cls.type_value(val)
        generics.append((name, type_name, pkg_name, size_name))
      elif (res := cls.port_role_key(key)) is not None:
        name, role = res
        DFACCTOAssert(role.is_port, 'Invalid port role "{}"'.format(role.name))
        type_name, pkg_name, size_name = cls.type_value(val)
        ports.append((name, role, type_name, pkg_name, size_name))
      elif (res := cls.prop_key(key)) is not None:
        name = res
        props[name] = val
      else:
        raise DFACCTOError('Invalid directive "{}"'.format(key))
    return (generics, ports, props)

  @classmethod
  def read_inst(cls, directives):
    generics = list()
    ports = list()
    props = dict()
    for key,val in directives.items():
      if (res := cls.generic_key(key)) is not None:
        name = res
        generics.append((name, val))
      elif (res := cls.port_key(key)) is not None:
        name = res
        ports.append((name, val))
      elif (res := cls.prop_key(key)) is not None:
        name = res
        props[name] = val
      else:
        raise DFACCTOError('Invalid directive "{}"'.format(key))
    return (generics, ports, props)



class Frontend:
  def __init__(self, context, *, entity=None, package=None):
    self._context = context
    self._entity = entity
    self._package = package


  def Gbl(self, **directives):
    props = Decoder.read_props(directives)
    self._context.props.update(props)
    # TODO-lw deep update, so that multiple Gbl(x_templates={...}) extend templates dir!


  def Pkg(self, name, **directives):
    name = Decoder.name_value(name)
    props = Decoder.read_props(directives)

    package = Package(self._context, name, props)
    return Frontend(self._context, package=package)


  def Typ(self, name, simple=False, complex=False, **directives):
    DFACCTOAssert(self._package is not None, 'Type declaration must appear in a package context')
    name = Decoder.name_value(name)
    role = Decoder.type_role_value(simple, complex)
    props = Decoder.read_props(directives)

    self._package.add_type(name, role, props)


  def Con(self, name, type, value=None, **directives):
    DFACCTOAssert(self._package is not None, 'Constant declaration must appear in a package context')
    name = Decoder.name_value(name)
    type_name, pkg_name, size_name = Decoder.type_value(type)
    props = Decoder.read_props(directives)

    type = self._package.get_type(type_name, pkg_name)
    self._package.add_constant(name, type, size_name, value, props)


  def Ent(self, name, **directives):
    name = Decoder.name_value(name)
    generics, ports, props = Decoder.read_entity(directives)

    entity = Entity(self._context, name, **props)

    for name, type_name, pkg_name, size_name in generics:
      type = self._context.get_type(type_name, pkg_name)
      # size = size_name and entity.get_generic(size_name)
      entity.add_generic(name, type, size_name)

    for name, role, type_name, pkg_name, size_name in ports:
      type = self._context.get_type(type_name, pkg_name).derive(role)
      # size = size_name and entity.get_generic(size_name)
      entity.add_port(name, type, size_name)

    return Frontend(self._context, entity=entity)

  def To(self, name):
    DFACCTOAssert(self._entity is not None, 'Connectable reference must appear in an entity context')
    name = Decoder.name_value(name)
    return self._entity.get_connectable(name)

  def ToVec(self, *names):
    DFACCTOAssert(self._entity is not None, 'Connectable reference must appear in an entity context')
    return tuple(self.To(name) for name in names)

  def Val(self, ref): # assign
    name, pkg_name = Decoder.ref_value(ref)
    if self._entity is not None:
      assignable = self._entity.get_assignable(name, pkg_name)
    elif self._package is not None:
      assignable = self._package.get_constant(name, pkg_name)
    else:
      assignable = self._context.get_constant(name, pkg_name)
    return assignable

  def ValVec(self, *refs):
    return tuple(self.Val(ref) for ref in refs)

  def Ins(self, entity_name, name=None, index=None, **directives):
    DFACCTOAssert(self._entity is not None, 'Instance declaration must appear in an entity context')
    entity_name = Decoder.name_value(entity_name)
    if name is None:
      name = entity_name[0].lower() + entity_name[1:]
    if index is not None:
      name = '{}{:d}'.format(name, index)
    inst_name = self._entity.instances.unique_name(name)
    generics, ports, props = Decoder.read_inst(directives)

    entity = self._context.get_entity(entity_name)
    instance = entity.instantiate(self._entity, inst_name, props)
    for name,value in generics:
      instance.assign(name, value)
    for name,to in ports:
      instance.connect(name, to)

