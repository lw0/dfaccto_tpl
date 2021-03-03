from collections import OrderedDict
import collections.abc as abc



class DFACCTOError(Exception):
  def __init__(self, msg):
    # breakpoint()
    self.msg = msg


def DFACCTOAssert(condition, msg):
  if not condition:
    raise DFACCTOError(msg)


def safe_str(obj):
  try:
    return '{}({})'.format(type(obj).__name__,
                           ' '.join('{}={}'.format(k,v) for k,v in vars(self).items()))
  except:
    return repr(obj)


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
    if hasattr(self._obj, key):
      return getattr(self._obj, key)
    else:
      raise AttributeError

  def __str__(self):
    return str(self._obj)

  @property
  def _last(self):
    return self._idx == (self._len - 1)

  @property
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

  @property
  def _len(self):
    return len(self._lst)


class Registry(abc.Iterable):
  def __init__(self):
    self._contents = list()
    self._names = dict()
    self._idx_cache = dict()

  def clear(self):
    self._contents.clear()
    self._names.clear()
    self._idx_cache.clear()

  def __iter__(self):
    return IndexWrapper(self._contents)

  def __len__(self):
    return len(self._contents)

  def __getitem__(self, key):
    try:
      return self._contents[key]
    except TypeError:
      idx = self._names[key]
      return self._contents[idx]

  def register(self, name, obj):
    if name in self._names:
      msg = 'Name collision: "{}" is already defined'.format(name)
      raise DFACCTOError(msg)
    self._names[name] = len(self._contents)
    self._contents.append(obj)

  def lookup(self, name):
    if name not in self._names:
      msg = 'Unresolved reference: "{}" is not defined'.format(name)
      raise DFACCTOError(msg)
    idx = self._names[name]
    return self._contents[idx]

  def has(self, name):
    return name in self._names

  def names(self):
    return self._names.keys()

  def contents(self):
    return tuple(self._contents)

  def items(self):
    for key,idx in self._names.items():
      yield key, self._contents[idx]

  def unique_name(self, prefix):
    idx = self._idx_cache.get(prefix, 0)
    candidate = prefix
    while candidate in self._names:
      candidate = '{}_{:d}'.format(prefix, idx)
      idx += 1
      self._idx_cache[prefix] = idx
    return candidate



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

  def group(self, idx):
    root = self.find(idx)
    return self._groups[root]

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


class ValueStore:

  _registry = UnionFind()
  _values = dict()

  @classmethod
  def _create(cls, val=None):
    """Create a new independent value index and initialize with val if not None"""
    idx = cls._registry.new()
    if val is not None:
      root = cls._registry.find(idx)
      cls._values[root] = val
    return idx

  @classmethod
  def _get_value(cls, idx):
    """Get value for idx if already set or None otherwise """
    root = cls._registry.find(idx)
    return cls._values.get(root)

  @classmethod
  def _set_value(cls, idx, val):
    """Set and possibly override value for idx unless val is None"""
    root = cls._registry.find(idx)
    if val is not None:
      cls._values[root] = val

  @classmethod
  def _assign(cls, idx_a, idx_b):
    """
    Join idx_a and idx_b to refer to the same value.
    If either is None the value of the other index is set for both.
    If neither is None, idx_b gets receives the value of idx_a.
    """
    val_a = cls._get_value(idx_a)
    val_b = cls._get_value(idx_b)
    if val_a is None:
      cls._registry.union(idx_b, idx_a)
    else:
      cls._registry.union(idx_a, idx_b)

class DeferredValue:
  _registry = UnionFind()
  _callbacks = dict()

  @classmethod
  def _create(cls, callback):
    idx = cls._registry.new()
    cls._callbacks[idx] = callback
    return idx

  @classmethod
  def _assign(cls, idx_a, idx_b):
    cls._registry.union(idx_a, idx_b)

  @classmethod
  def _resolve(cls, idx, value):
    #TODO-lw track if already resolved
    for i in cls._registry.group(idx):
      callback = cls._callbacks.get(i)
      if callback:
        callback(value)

  def __init__(self, on_resolve):
    self._idx = self._create(on_resolve)

  def assign(self, other):
    if isinstance(other, DeferredValue):
      self._assign(self._idx, other._idx)
    else:
      self._resolve(self._idx, other)


