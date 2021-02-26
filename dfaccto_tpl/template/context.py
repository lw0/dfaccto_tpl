from .errors import AbsentError



def _default_lookup(obj, field):
  try:
    return obj[field]
  except KeyError:
    raise AbsentError('Could not find field "{}"'.format(field))
  except TypeError:
    # TODO-lw try obj[int(field)] ?
    try:
      return getattr(obj, field)
    except AttributeError:
      raise AbsentError('Could not find field "{}"'.format(field))


class Context:

  def __init__(self, *context_items, raise_on_absent=False, lookup=None, stringify=None, escape=None, partial=None):
    self._stack = list(context_items)
    self._raise_on_absent = raise_on_absent
    self._lookup = lookup or _default_lookup
    self._stringify = stringify or str
    self._escape = escape
    self._partial = partial

  def get_partial(self, name):
    partial = None
    if self._partial is not None:
      partial = self._partial(name)
    if partial is None and self._raise_on_absent:
      raise AbsentError('Can not resolve partial "{}"'.format(name))
    return partial

  def push(self, item):
    self._stack.append(item)

  def pop(self):
    return self._stack.pop()

  def get_string(self, key, verbatim):
    val = self._get_value(key)
    if not isinstance(val, str):
      val = self._stringify(val)
    if verbatim or self._escape is None:
      return val
    else:
      return self._escape(val)

  def get_section(self, key):
    val = self._get_value(key)
    if val is None or val is False:
      # exclude integer 0 from falsey values!
      return []
    elif isinstance(val, str):
      return [val]
    else:
      try:
        iter(val)
      except TypeError:
        return [val]
      else:
        return val

  def _get_value(self, key):
    try:
      if not key.first:
        return self._top(key.skip)
      else:
        value = self._search(key.first, key.skip, key.anchored)
        for part in key.rest:
          value = self._lookup(value, part)
        return value
    except AbsentError as e:
      if self._raise_on_absent:
        e.set_key(key)
        raise e
      else:
        return None

  def _top(self, skip):
    if len(self._stack) <= skip:
      raise AbsentError('Not enough stack items to skip {}'.format(skip))
    return self._stack[-skip - 1]

  def _search(self, field, skip, anchored):
    context_items = self._stack[-1:] if anchored else reversed(self._stack)
    to_skip = skip
    for item in context_items:
      try:
        val = self._lookup(item, field)
        if to_skip > 0:
          to_skip -= 1
        else:
          return val
      except AbsentError:
        pass
    raise AbsentError('Could not find {} in context stack after skipping {}'.format(field, skip - to_skip))


