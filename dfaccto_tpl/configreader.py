from collections import namedtuple
from pathlib import Path
import sys
import traceback

from .context import Context
from .frontend import Frontend
from .util import DFACCTOError, ModuleRef, resolve_path


ExecEntry = namedtuple('ExecEntry', ['base', 'module'])


class ConfigReader:
  def __init__(self, args, context=None):
    self._args = args
    self._context = context or Context()
    self._frontend = Frontend(self._context)
    self._globals = {'Inc': self.read,
                     'File': self.module_ref,
                     'Part': self.partial_ref}
    self._globals.update(self._frontend.namespace)
    self._executed = set()
    self._stack = [ExecEntry(Path('.').resolve(), None)]

  @property
  def context(self):
    return self._context

  def module_ref(self, name, mod=None):
    module = self._stack[-1].module if mod is None else mod
    return ModuleRef(module, name)

  def partial_ref(self, name, mod=None):
    module = self._stack[-1].module if mod is None else mod
    return '{{{{>{}:{}}}}}'.format(module if module is not None else '', name)

  def _resolve_cfg(self, name, abs=False):
    if abs is False:
      module = self._stack[-1].module
      path = self._stack[-1].base / name
      if not path.exists():
        raise DFACCTOError('Can not resolve relative script name "{}"'.format(name))
    else:
      module = self._stack[-1].module if abs is True else abs
      path = resolve_path(self._args.cfgdirs(module), name)
      if path is None:
        raise DFACCTOError('Can not resolve absolute script name "{}" in module {}'.format(name, module))
    return (path.resolve(), module)

  def read(self, name, abs=False):
    path, module = self._resolve_cfg(name, abs)

    if path in self._executed:
      return
    self._executed.add(path)
    self._stack.append(ExecEntry(path.parent, module))

    try:
      code = None
      try:
        code = compile(path.read_text(), path, 'exec')
      except Exception as e:
        raise DFACCTOError('Error compiling "{}":\n  {}'.format(path, e))
      try:
        exec(code, self._globals)
      except DFACCTOError:
        e_type,e_msg,e_tb = sys.exc_info()
        e_trace = traceback.extract_tb(e_tb)
        e_frame = e_trace[1] # select frame within user code
        msg = '{}\n  at [{} : {}]\n  "{}"'.format(e_msg, e_frame.filename, e_frame.lineno, e_frame.line)
        raise DFACCTOError(msg)
    finally:
      self._stack.pop()

