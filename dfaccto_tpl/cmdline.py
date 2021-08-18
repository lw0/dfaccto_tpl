import argparse
from functools import partial
from pathlib import Path
import re


def path_arg(arg, dir=True, exist=False):
  path = Path(arg).expanduser().resolve()
  if dir:
    if exist:
      if not path.is_dir():
        raise argparse.ArgumentTypeError('{} must be an existing directory'.format(path))
    else:
      try:
        path.mkdir(parents=True, exist_ok=True)
      except FileExistsError:
        raise argparse.ArgumentTypeError('{} must be a directory'.format(path))
    return path
  else:
    if exist:
      if not path.is_file():
        raise argparse.ArgumentTypeError('{} must be an existing file'.format(path))
    else:
      try:
        path.parent.mkdir(parents=True, exist_ok=True)
      except FileExistsError:
        raise argparse.ArgumentTypeError('Parents of {} are not directories'.format(path))
      if path.exists and not path.is_file():
        raise argparse.ArgumentTypeError('{} must be a file'.format(path))
    return path


def str_arg(arg, regex=re.compile('.*')):
  if not regex.match(arg):
    raise argparse.ArgumentTypeError('{} is an invalid string'.format(arg))
  return arg


class Cmdline:
  KEY_CFGDIRS    = '_cfgdirs_'
  KEY_TPLDIRS    = '_tpldirs_'
  KEY_ENTRY      = '_entry_'
  KEY_OUTDIR     = '_outdir_'
  KEY_DEBUG      = '_debug_'
  MODULE_KEYS = (KEY_CFGDIRS, KEY_TPLDIRS)
  GLOBAL_KEYS = (KEY_ENTRY, KEY_OUTDIR, KEY_DEBUG)

  class SetModule(argparse.Action):
    def __call__(self, parser, namespace, value, optstr):
      namespace._current(value)

  @classmethod
  def parse(cls):
    parser = argparse.ArgumentParser(
        prog='dfaccto_tpl',
        description='Build a data model from a config script and use it to render templates')

    parser.add_argument('--debug', dest=cls.KEY_DEBUG,
        action='store_true',
        help='enter debugger after scripts are read and before templates are rendered')

    parser.add_argument('--outdir', '-o', dest=cls.KEY_OUTDIR,
        required=True, action='store',
        type=partial(path_arg, dir=True, exist=False),
        metavar='<outdir>',
        help='place generated files here (WARNING: deletes existing content!)')

    parser.add_argument('--entry', '-e', dest=cls.KEY_ENTRY,
        required=True, action='store',
        type=partial(str_arg, regex=re.compile('\S+')),
        metavar='<script>',
        help='read this script from the default module to build the data model')

    parser.add_argument('--module', '-m', action=cls.SetModule,
        type=partial(str_arg, regex=re.compile('\w+')),
        metavar='<module>',
        help='begin a new named module')

    parser.add_argument('--cfgdir', '-c', dest=cls.KEY_CFGDIRS,
        action='append',
        type=partial(path_arg, dir=True, exist=True),
        metavar='<cfgdir>',
        help='search for config scripts here (can appear more than once)')

    parser.add_argument('--tpldir', '-t', dest=cls.KEY_TPLDIRS,
        action='append',
        type=partial(path_arg, dir=True, exist=True),
        metavar='<tpldir>',
        help='search for templates and partials here (can appear more than once)')

    return parser.parse_args(namespace=cls())

  def __init__(self):
    self._modules = dict()
    self._globals = argparse.Namespace()
    self._current_key = None # default module

  def __setattr__(self, key, value):
    if key in type(self).MODULE_KEYS:
      setattr(self._current(), key, value)
    elif key in type(self).GLOBAL_KEYS:
      setattr(self._globals, key, value)
    else:
      object.__setattr__(self, key, value)

  def __getattr__(self, key):
    if key in type(self).MODULE_KEYS:
      return getattr(self._current(), key)
    elif key in type(self).GLOBAL_KEYS:
      return getattr(self._globals, key)
    else:
      raise AttributeError(key)

  def _module(self, key):
    if key not in self._modules:
      self._modules[key] = argparse.Namespace()
    return self._modules[key]

  def _trymodule(self, key):
    if key not in self._modules:
      raise DFACCTOError('Undefined module "{}"'.format(key))
    return self._modules[key]

  def _current(self, newkey=None):
    if newkey is not None:
      self._current_key = newkey
    return self._module(self._current_key)

  def modules(self):
    return self._modules.keys()

  def cfgdirs(self, module=None):
    return getattr(self._trymodule(module), type(self).KEY_CFGDIRS, [])

  def tpldirs(self, module=None):
    return getattr(self._trymodule(module), type(self).KEY_TPLDIRS, [])

  def entry(self):
    return getattr(self._globals, type(self).KEY_ENTRY)

  def outdir(self):
    return getattr(self._globals, type(self).KEY_OUTDIR)

  def debug(self):
    return getattr(self._globals, type(self).KEY_DEBUG, False)


