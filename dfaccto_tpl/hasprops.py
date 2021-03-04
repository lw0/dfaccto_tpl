


class HasProps:
  def __init__(self):
    self._props = dict()

  def __getattr__(self, key):
    if key.startswith('x_') and key[2:] in self._props:
      return self._props[key[2:]]
    elif key.startswith('is_a_'):
      name = key[5:].lower()
      return any(name == cls.__name__.lower() for cls in type(self).mro())
    else:
      raise AttributeError(key)

  def set_prop(self, key, value):
    self._props[key] = value

  # -> see Frontend.global_statement()
  # def update_prop(self, key, value):
  #   if key in self._props:
  #     old = self._props[key]
  #     try:
  #       old.update(value)
  #       return
  #     except:
  #       try:
  #         old.extend(value)
  #         return
  #       except:
  #         pass
  #   self._props[key] = value

  def clear_props(self):
    self._props.clear()

  @property
  def props(self):
    return self._props


