from .common import Connectable, EntityElement


class Signal(Connectable, EntityElement):

  def __init__(self, entity, name, type=None, size=None):
    EntityElement.__init__(self, entity, name, 's_{name}{dir}')
    Connectable.__init__(self, type, size, on_type_set=self._register_identifiers)

    self.entity.signals.register(self.name, self)
    self.entity.connectables.register(self.name, self)

  def _register_identifiers(self):
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    if self.is_vector:
      if self.type is None:
        return '({}).s_{}({})?'.format(self.entity, self.name, self.size)
      else:
        return '({}).s_{}({}):{}'.format(self.entity, self.name, self.size, self.type)
    else:
      if self.type is None:
        return '({}).s_{}?'.format(self.entity, self.name)
      else:
        return '({}).s_{}:{}'.format(self.entity, self.name, self.type)

