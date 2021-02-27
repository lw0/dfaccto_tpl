from .util import safe_str
from .common import Connectable, Typed
from .element import EntityElement


class Signal(EntityElement, Typed, Connectable):
  def __init__(self, entity, name, type=None, size=None):
    EntityElement.__init__(self, entity, name, 's_{name}{dir}')
    Typed.__init__(self, type, size, on_type_set=self._register_identifiers)
    Connectable.__init__(self)

    self.entity.signals.register(self.name, self)
    self.entity.connectables.register(self.name, self)

  def _register_identifiers(self):
    if self.is_simple:
      self.entity.identifiers.register(self.identifier, self)
    elif self.is_complex:
      self.entity.identifiers.register(self.identifier_ms, self)
      self.entity.identifiers.register(self.identifier_sm, self)

  def __str__(self):
    try:
      if self.knows_type:
        type_str = ':{}'.format(self.type)
      else:
        type_str = '?'
      if self.knows_cardinality:
        if self.is_vector:
          size_str = '({})'.format(self.size if self.knows_size else '')
        else:
          size_str = ''
      else:
        size_str = '?'
      return '({}).s_{}{}{}'.format(self.entity, self.name, type_str, size_str)
    except:
      return safe_str(self)

