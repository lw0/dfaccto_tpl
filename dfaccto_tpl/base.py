from collections import OrderedDict



class DFACCTOError(Exception):
  def __init__(self, msg):
    self.msg = msg


def DFACCTOAssert(condition, msg):
  if not condition:
    raise DFACCTOError(msg)


def Seq(*items, f):
  result = []
  for idx in f:
    result.extend(item.format(idx) for item in items)
  return result


class IndexedObj():
  def __init__(self, obj, idx, len):
    self._obj = obj
    self._idx = idx
    self._len = len

  def __getattr__(self, key):
    try:
      return self._obj[key]
    except TypeError:
      pass
    except KeyError:
      pass
    return getattr(self._obj, key)

  #TODO-lw @property
  def _last(self):
    return self._idx == (self._len - 1)

  def _first(self):
    return self._idx == 0


class IndexWrapper():
  def __init__(self, lst):
    self._iter = iter(lst)
    self._lst = lst
    self._idx = 0

  def __iter__(self):
    return self

  def __next__(self):
    item = IndexedObj(next(self._iter), self._idx, len(self._lst))
    self._idx += 1
    return item

  def _len(self):
    return len(self._lst)


class Registry():
  def __init__(self):
    self.map = OrderedDict()
    self.idx_cache = {}

  def clear(self):
    self.map.clear()
    self.idx_cache.clear()

  def __iter__(self):
    return IndexWrapper(self.map.values())

  def __len__(self):
    return len(self.map)

  def register(self, name, obj):
    DFACCTOAssert(name not in self.map, 'Name collision: "{}" is already defined'.format(name))
    self.map[name] = obj

  def lookup(self, name):
    DFACCTOAssert(name in self.map, 'Unresolved reference: "{}" is not defined'.format(name))
    return self.map[name]

  def has(self, name):
    return name in self.map

  def keys(self):
    return self.map.keys()

  def contents(self):
    return self.map.values()

  def uniqueName(self, prefix):
    idx = self.idx_cache.get(prefix, 0)
    candidate = prefix
    while candidate in self.map:
      candidate = '{}_{:d}'.format(prefix, idx)
      idx += 1
      self.idx_cache[prefix] = idx
    return candidate

  def dump(self):
    for key, value in self.map.items():
      print('{!s}: {!s}'.format(key, value))


class UnionFind:
  def __init__(self):
    self._root = list()
    self._groups = dict()

  def new(self):
    idx = len(self._root)
    self._root.append(idx)
    self._groups[idx] = set((idx,))
    return idx

  def find(self, idx):
    return self._root[idx]

  def union(self, idx_a, idx_b):
    root_a = self.find(idx_a)
    root_b = self.find(idx_b)
    if root_a == root_b:
      return root_a

    for idx in self._groups[root_b]:
      self._root[idx] = root_a
      self._groups[root_a].add(idx)
    del self._groups[root_b]
    return root_a

  def dump(self):
    print('UnionFind @{:d}'.format(self._idx))
    for idx, root in self._root.items():
      print(' {:d} -> {:d}'.format(idx, root))
    for root, idx_set in self._groups.items():
      print(' {:d}: {!s}'.format(root, idx_set))


class ValueContainer:

  _registry = UnionFind()
  _values = dict()

  @classmethod
  def _create(cls, val):
    idx = cls._registry.new()
    if val is not None:
      root = cls._registry.find(idx)
      cls._values[root] = val
    return idx

  @classmethod
  def _value(cls, idx):
    root = cls._registry.find(idx)
    return cls._values.get(root)

  @classmethod
  def _set_value(cls, idx, val):
    root = cls._registry.find(idx)
    if root not in cls._values:
      if val is not None:
        cls._values[root] = val
    else:
      if cls._values[root] != val:
        raise ValueError("Value is already set and may not be changed")

  @classmethod
  def _assign(cls, idx_a, idx_b):
    val_a = cls._value(idx_a)
    val_b = cls._value(idx_b)
    if val_b is None or val_a == val_b:
      cls._registry.union(idx_a, idx_b)
    elif val_a is None:
      cls._registry.union(idx_b, idx_a)
    else:
      raise ValueError("Can not assign containers with different values")

  def __init__(self, value=None):
    self._idx = self._create(value)

  @property
  def value(self):
    return self._value(self._idx)

  @property
  def has_value(self):
    return self._value(self._idx) is not None

  def assign(self, other):
    if isinstance(other, ValueContainer):
      self._assign(self._idx, other._idx)
    else:
      self._set_value(self._idx, other)

