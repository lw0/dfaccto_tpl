import re



class Key:
  """
  Represents a lookup key to get a value from a Context instance.

  It consists of a (possibly empty) path of field names to search for,
  as well as a mode parameter that modifies the search semantics.
  A negative mode values indicate anchored mode, where only the
  top of the Context stack is considered.
  A non-negative mode value results in a search through the entire
  Context stack, and indicates the number of matches that should be skipped.

  (See Context)
  """

  _Pattern = re.compile(r'(\.|\'+)|(\.|\'*)(\w+(?:\.\w+)*)')

  @classmethod
  def parse(cls, string):
    """
    Parse a string representation into a Key instance.

    The string is expected to be a dot . separated sequence of words,
    indicating a path of field names to search in the Context.
    A leading dot . indicates anchored mode;
    otherwise each leading tick ' increments skip mode.
    In anchored or skip mode, the field name path may be empty.

    Parameters:
      string : str
        Key string representation to parse.
    Returns:
      Key instance if string is valid or None otherwise
    """
    if m := cls._Pattern.fullmatch(string):
      m_onlymode = m.group(1)
      m_mode = m.group(2)
      m_path = m.group(3)
      if m_onlymode is not None:
        mode = -1 if m_onlymode == '.' else len(m_onlymode)
        return cls(mode, ())
      else:
        mode = -1 if m_mode == '.' else len(m_mode)
        path = tuple(m_path.split('.'))
        return cls(mode, path)
    else:
      return None

  def __init__(self, mode, path):
    """
    Construct a Key instance with explicit mode and path parameters.

    Parameters:
      mode : int
      path : tuple(str)
    """
    self._mode = mode
    self._path = path

  @property
  def path(self):
    """Raw path parameter"""
    return self._path

  @property
  def first(self):
    """First component of path or None if empty"""
    return self._path and self._path[0] or None

  @property
  def rest(self):
    """Following components of path or empty if absent"""
    return self._path[1:]

  @property
  def mode(self):
    """Raw mode parameter"""
    return self._mode

  @property
  def anchored(self):
    """True for anchored mode"""
    return self._mode < 0

  @property
  def skip(self):
    """Number of matches to skip"""
    return max(self._mode, 0)

  def __str__(self):
    mode_str = '.'
    if self._mode >= 0:
      mode_str = '\'' * self._mode
    path_str = '.'.join(self._path)
    return '{}{}'.format(mode_str, path_str)

  def __eq__(self, other):
    return self._mode == other._mode and self._path and other._path


