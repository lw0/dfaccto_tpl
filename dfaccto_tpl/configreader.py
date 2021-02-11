from pathlib import Path
import sys
import traceback

from .util import DFACCTOError, Seq
from .role import Role
from .context import Context
from .frontend import Frontend


class ConfigReader:
  def __init__(self, context=None):
    self._context = context or Context()
    self._frontend = Frontend(self._context)
    self._globals = {
      'Inc': self.read,
      'Simple': Role.Simple,
      'Complex': Role.Complex,
      'Seq': Seq,
      'Gbl': self._frontend.Gbl,
      'Pkg': self._frontend.Pkg,
      'Ent': self._frontend.Ent }
    self._executed = set()
    self._base_path = list()

  @property
  def context(self):
    return self._context

  def read(self, path):
    if self._base_path:
      path = self._base_path[-1] / path
    path = Path(path).resolve()

    if path in self._executed:
      return
    self._executed.add(path)

    self._base_path.append(path.parent)
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
      self._base_path.pop()
