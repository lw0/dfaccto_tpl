from .util import ValueContainer
from .common import Instantiable, EntityElement


class InstGeneric(Instantiable, EntityElement, ValueContainer):
  def __init__(self, generic, inst_entity):
    ValueContainer.__init__(self)
    EntityElement.__init__(self, inst_entity, generic.name, 'g_{name}')
    Instantiable.__init__(self, generic)

    self.entity.generics.register(self.name, self)
    self.entity.identifiers.register(self.identifier, self)

  def __str__(self):
    if self.value is None:
      return '({}).g_{}'.format(self.entity, self.name)
    else:
      return '({}).g_{}={}'.format(self.entity, self.name, self.value)


class Generic(Instantiable, EntityElement):
  def __init__(self, entity, name):
    EntityElement.__init__(self, entity, name, 'g_{name}')
    Instantiable.__init__(self)

    self.entity.generics.register(self.name, self)
    self.entity.identifiers.register(self.identifier, self)

  def __str__(self):
      return '({}).g_{}'.format(self.entity, self.name)

  def instantiate(self, inst_entity):
    return InstGeneric(self, inst_entity)



