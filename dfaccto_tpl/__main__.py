import argparse
from itertools import chain
from pathlib import Path
import pystache
import sys
import traceback

from . import DFACCTOError, Role, Seq, Context, Frontend


def load_templates(tpl_path, suffix):
  templates = dict()
  for tpl_file in tpl_path.rglob('*{}.tpl'.format(suffix)):
    name = str(tpl_file.relative_to(tpl_path))[:-4]
    template = pystache.parse(tpl_file.read_text())
    templates[name] = template
  return templates


class Executor:
  def __init__(self, context):
    self._frontend = Frontend(context)
    self._globals = {
      'Inc': self._execute,
      'Simple': Role.Simple,
      'Complex': Role.Complex,
      'Seq': Seq,
      'Gbl': self._frontend.Gbl,
      'Pkg': self._frontend.Pkg,
      'Ent': self._frontend.Ent }
    self._executed = set()
    self._base_path = list()

  def execute(self, path):
    self._base_path[:] = (path.parent,)
    self._execute(path.name)

  def _execute(self, name):
    path = self._base_path[-1] / name
    if path in self._executed:
      return
    self._executed.add(path)
    self._base_path.append(path.parent)
    code = compile(path.read_text(), path, 'exec')
    exec(code, self._globals)
    self._base_path.pop()


def main(args):
  templates = load_templates(args.tpldir, '.vhd')
  partials = load_templates(args.tpldir, '.part')

  context = Context()

  executor = Executor(context)
  executor.execute(args.config)
  # try:
  #   exec(script, globals)
  # except DFACCTOError:
  #   e_type,e_msg,e_tb = sys.exc_info()
  #   e_trace = traceback.extract_tb(e_tb)
  #   print('DFACCTOError: {}'.format(e_msg), file=sys.stderr)
  #   print(' at [{}:{}] "{}"'.format(os.path.relpath(e_trace[1][0]), e_trace[1][1], e_trace[1][3]), file=sys.stderr)
  #   sys.exit(1)

  if args.debug:
    breakpoint()

  renderer = pystache.Renderer(partials=partials, escape=lambda s: s)

  element_iter = chain((context,), context.packages.contents(), context.entities.contents())
  for element in element_iter:
    for tpl_name,out_name in element.props.get('templates', {}).items():
      template = templates[tpl_name] # TODO-lw handle potential KeyError
      path = args.outdir / (out_name or tpl_name)
      path.parent.mkdir(parents=True, exist_ok=True)
      print('Render "{}" ({}) -> "{}"'.format(tpl_name, element, path))
      path.write_text(renderer.render(template, context, element))


def arg_dir(arg):
  path = Path(arg).expanduser().resolve()
  if not path.is_dir():
    msg = '{} does not exist or is not a directory'.format(arg)
    raise argparse.ArgumentTypeError(msg)
  return path

def arg_emptydir(arg):
  path = Path(arg).expanduser().resolve()
  if not path.exists():
    path.mkdir(parents=True)
  elif not path.is_dir():
    msg = '{} is not a directory'.format(arg)
    raise argparse.ArgumentTypeError(msg)
  else:
    for f in path.iterdir():
      f.unlink()
  return path

def arg_file(arg):
  path = Path(arg).expanduser().resolve()
  if not path.is_file():
    msg = '{} does not exist or is not a file'.format(arg)
    raise argparse.ArgumentTypeError(msg)
  return path

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--tpldir', type=arg_dir)
  parser.add_argument('--outdir', type=arg_emptydir)
  parser.add_argument('--config', type=arg_file)
  parser.add_argument('--debug', action='store_true')
  main(parser.parse_args())

