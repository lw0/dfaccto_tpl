import collections.abc as abc
import re

from .base import DFACCTOAssert
from .role import Role
from .type import Type
from .entity import Entity
from .signal import Signal
from .package import Package


class Frontend:

  # '<type_name>'
  # '<pkg_name>.<type_name>'
  TypePattern = re.compile('(?:(\w+)\.)?(\w+)')

  # g_<name>=None
  # g_<name>=<value>
  GenericPattern = re.compile('g_(\w+)')

  # p<role>_<name>='<type>'
  # p<role>_<name>=('<type>', '<size_generic_name>')
  PortRolePattern = re.compile('p(\w)_(\w+)')

  # p_<name>='<signal_name>'
  # p_<name>=['<signal_name>', ... ]
  PortConnectPattern = re.compile('p_(\w+)')

  # x_<name>=<value>
  # xt_<name>='<type_name>'
  PropertyPattern = re.compile('x(t?)_(\w+)')


  def __init__(self, context, *, entity=None, package=None):
    self._context = context
    self._entity = entity
    self._package = package



  def _resolve_generic(self, key, value):
    m = type(self).GenericPattern.match(key)
    if m:
      name = m.group(1)
      return (name, value)
    return None

  def _resolve_type(self, value):
    m = type(self).TypePattern.match(value)
    DFACCTOAssert(m,
      'Invalid type specification "{}"'.format(value))
    pkg_name = m.group(1)
    type_name = m.group(2)
    return self._context.get_type(type_name, pkg_name)

  def _resolve_port_definition(self, key, value):
    m = type(self).PortRolePattern.match(key)
    if m:
      role = Role.parse(m.group(1))
      name = m.group(2)
      DFACCTOAssert(role.is_port,
        'Can not define port {} with non-port role {}'.format(name, role))
      if isinstance(value, str):
        port_type = self._resolve_type(value)
        size_generic_name = None
      else:
        port_type = self._resolve_type(value[0])
        size_generic_name = value[1]
      return (name, port_type.derive(role), size_generic_name)
    return None


  def _resolve_port_connect(self, key, value, index=None):
    m = type(self).PortConnectPattern.match(key)
    if m:
      port_name = m.group(1)
      if isinstance(value, str):
        to = self._entity.get_connectable(value.format(index))
      elif isinstance(value, abc.Sequence):
        DFACCTOAssert(all(isinstance(sig_name, str) for sig_name in value),
          "Vector Port Assignment requires signal names throughout")
        to = [self._entity.get_connectable(sig_name.format(index)) for sig_name in value]
      return (port_name, to)
    return None


  def _resolve_property(self, key, value):
    m = type(self).PropertyPattern.match(key)
    if m:
      name = m.group(2)
      if m.group(1) == 't': # expand type name
        value = self._resolve_type(value)
      elif m.group(1) == 'p': # expand partial name
        value = lambda: '{{{{>{}}}}}'.format(value)
      return (name, value)
    return None

  def Gbl(self, **directives):
    props = {}
    for key,value in directives.items():
      res = self._resolve_property(key, value)
      if res is not None:
        props[res[0]] = res[1]
      #TODO-lw ?raise error for unrecognized directives?
    self._context.props.update(props) # TODO-lw deep update, so that multiple Gbl(x_templates={...}) extend templates dir!


  def Pkg(self, name, **directives):
    props = {}
    for key,value in directives.items():
      res = self._resolve_property(key, value)
      if res is not None:
        props[res[0]] = res[1]
      #TODO-lw ?raise error for unrecognized directives?
    package = Package(self._context, name, props)
    return Frontend(self._context, package=package)


  def Typ(self, name, role, **directives):
    DFACCTOAssert(self._package is not None,
      'Typ() must be used in a package context')
    props = {}
    for key,value in directives.items():
      res = self._resolve_property(key, value)
      if res is not None:
        props[res[0]] = res[1]
      #TODO-lw ?raise error for unrecognized directives?
    DFACCTOAssert(role.is_signal,
      'Can not define type {} with port role "{}"'.format(name, role))
    Type(self._package, name, role, **props)


  def Ent(self, name, **directives):
    generics = []
    ports = []
    props = {}
    for key,value in directives.items():
      res = self._resolve_generic(key, value)
      if res is not None:
        generics.append(res[0])
        continue
      res = self._resolve_port_definition(key, value)
      if res is not None:
        ports.append(res)
        continue
      res = self._resolve_property(key, value)
      if res is not None:
        props[res[0]] = res[1]
    entity = Entity(self._context, name, **props)
    for name in generics:
      entity.generic(name)
    for name,type,size_generic_name in ports:
      entity.port(name, type, size_generic_name)
    return Frontend(self._context, entity=entity)

  def _instance_name(self, name, entity_name, index=None):
    if name is None:
      name = entity_name[0].lower() + entity_name[1:]
    if index is not None:
      name = '{}{:d}'.format(name, index)
    return self._entity.instances.uniqueName(name)

  def Ins(self, entity_name, **directives):
    DFACCTOAssert(self._entity is not None,
      'Ins() must be used in an entity context')
    index = directives.get('index', None)
    name = directives.get('name', None)
    generics = []
    ports = []
    for key,value in directives.items():
      res = self._resolve_generic(key, value)
      if res is not None:
        generics.append(res)
        continue
      res = self._resolve_port_connect(key, value, index)
      if res is not None:
        ports.append(res)
        continue
    entity = self._context.entities.lookup(entity_name)
    inst_name = self._instance_name(name, entity_name, index)
    instance = entity.instantiate(self._entity, inst_name)
    for name,value in generics:
      instance.assign(name, value)
    for name,to in ports:
      instance.connect(name, to)

  def Sig(self, name, type_name=None): # TODO-lw consider removal
    DFACCTOAssert(self._entity is not None,
      'Sig() must be used in an entity context')
    type = type_name and self._resolve_type(type_name)
    Signal(self._entity, name, type)
