

class Element:
  def __init__(self, context, name, identifier_pattern, has_vector=False):
    self._context = context
    self._name = name
    self._identifier_pattern = identifier_pattern
    self._identifier = None
    self._identifier_ms = None
    self._identifier_sm = None
    self._identifier_v = None
    self._identifier_v_ms = None
    self._identifier_v_sm = None
    self._has_vector = has_vector

  @property
  def context(self):
    return self._context

  @property
  def name(self):
    return self._name

  @property
  def identifier(self):
    if self._identifier is None:
      if self.has_role:
        if self.knows_role and self.role.is_simple:
          self._identifier = self._identifier_pattern.format(name=self._name,
                                                             mode=self.cmode,
                                                             vec='', dir='')
      else:
        self._identifier = self._identifier_pattern.format(name=self._name,
                                                           mode='',
                                                           vec='', dir='')
    return self._identifier

  @property
  def identifier_ms(self):
    if self._identifier_ms is None:
      if self.has_role and self.knows_role and self.role.is_complex:
        self._identifier_ms = self._identifier_pattern.format(name=self._name,
                                                              mode=self.cmode_ms,
                                                              vec='', dir='_ms')
    return self._identifier_ms

  @property
  def identifier_sm(self):
    if self._identifier_sm is None:
      if self.has_role and self.knows_role and self.role.is_complex:
        self._identifier_sm = self._identifier_pattern.format(name=self._name,
                                                              mode=self.cmode_sm,
                                                              vec='', dir='_sm')
    return self._identifier_sm

  @property
  def identifier_v(self):
    if self._has_vector and self._identifier_v is None:
      if self.has_role:
        if self.knows_role and self.role.is_simple:
          self._identifier_v = self._identifier_pattern.format(name=self._name,
                                                               mode=self.cmode,
                                                               vec='_v', dir='')
      else:
        self._identifier_v = self._identifier_pattern.format(name=self._name,
                                                             mode='',
                                                             vec='_v', dir='')
    return self._identifier_v

  @property
  def identifier_v_ms(self):
    if self._has_vector and self._identifier_v_ms is None:
      if self.has_role and self.knows_role and self.role.is_complex:
        self._identifier_v_ms = self._identifier_pattern.format(name=self._name,
                                                                mode=self.cmode_ms,
                                                                vec='_v', dir='_ms')
    return self._identifier_v_ms

  @property
  def identifier_v_sm(self):
    if self._has_vector and self._identifier_v_sm is None:
      if self.has_role and self.knows_role and self.role.is_complex:
        self._identifier_v_sm = self._identifier_pattern.format(name=self._name,
                                                                mode=self.cmode_sm,
                                                                vec='_v', dir='_sm')
    return self._identifier_v_sm


class EntityElement(Element):
  def __init__(self, entity, name, identifier_pattern, has_vector=False):
    Element.__init__(self, entity.context, name, identifier_pattern, has_vector)
    self._entity = entity

  @property
  def entity(self):
    return self._entity

  @property
  def qualified(self):
    return self.identifier

  @property
  def qualified_ms(self):
    return self.identifier_ms

  @property
  def qualified_sm(self):
    return self.identifier_sm

  @property
  def qualified_v(self):
    return self.identifier_v

  @property
  def qualified_v_ms(self):
    return self.identifier_v_ms

  @property
  def qualified_v_sm(self):
    return self.identifier_v_sm


class PackageElement(Element):
  def __init__(self, package, name, identifier_pattern, has_vector=False):
    Element.__init__(self, package.context, name, identifier_pattern, has_vector)
    self._package = package
    self._qualified = None
    self._qualified_ms = None
    self._qualified_sm = None
    self._qualified_v = None
    self._qualified_v_ms = None
    self._qualified_v_sm = None

  @property
  def package(self):
    return self._package

  @property
  def qualified(self):
    if self._qualified is None:
      ident = self.identifier
      if ident is not None:
        self._qualified = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified

  @property
  def qualified_ms(self):
    if self._qualified_ms is None:
      ident = self.identifier_ms
      if ident is not None:
        self._qualified_ms = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_ms

  @property
  def qualified_sm(self):
    if self._qualified_sm is None:
      ident = self.identifier_sm
      if ident is not None:
        self._qualified_sm = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_sm

  @property
  def qualified_v(self):
    if self._qualified_v is None:
      ident = self.identifier_v
      if ident is not None:
        self._qualified_v = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_v

  @property
  def qualified_v_ms(self):
    if self._qualified_v_ms is None:
      ident = self.identifier_v_ms
      if ident is not None:
        self._qualified_v_ms = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_v_ms

  @property
  def qualified_v_sm(self):
    if self._qualified_v_sm is None:
      ident = self.identifier_v_sm
      if ident is not None:
        self._qualified_v_sm = '{}.{}'.format(self.package.identifier, ident)
    return self._qualified_v_sm


