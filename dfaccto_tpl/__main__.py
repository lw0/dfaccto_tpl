import argparse
from itertools import chain
from pathlib import Path
import sys
import shutil
import traceback

from .configreader import ConfigReader
from .contextrenderer import ContextRenderer
from .util import DFACCTOError


def main(args):
  try:
    reader = ConfigReader()
    reader.read(args.config)

    context = reader.context
    if args.debug:
      breakpoint()

    renderer = ContextRenderer(args.outdir)
    renderer.load_templates(args.tpldir, '.tpl', '.part')

    element_iter = chain((context,), context.packages.contents(), context.entities.contents())
    for element in element_iter:
      for tpl_name,out_name in element.props.get('templates', {}).items():
        print('Rendering "{}" --{}:{}--> "{}"'.format(tpl_name, type(element).__name__, element, out_name or tpl_name))
        renderer.render(tpl_name, element, out_name)
  except DFACCTOError as e:
    print(e, file=sys.stderr)
    return 1
  except Exception as e:
    print('Unexpected error:', file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    return 1
  return 0


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
      if f.is_dir():
        shutil.rmtree(f)
      else:
        f.unlink()
  return path

def arg_file(arg):
  path = Path(arg).expanduser().resolve()
  if not path.is_file():
    msg = '{} does not exist or is not a file'.format(arg)
    raise argparse.ArgumentTypeError(msg)
  return path

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      prog='dfaccto_tpl',
      description='Build a data model from a config script and use it to render templates')
  parser.add_argument('--tpldir', required=True, type=arg_dir,
      help='Search for templates (*.tpl) and partials (*.part.tpl) here')
  parser.add_argument('--outdir', required=True, type=arg_emptydir,
      help='Place generated files here (WARNING: deletes existing content!)')
  parser.add_argument('--config', required=True, type=arg_file,
      help='Read this Python script to build the data model')
  parser.add_argument('--debug', action='store_true',
      help='Enter debugger after script is read')
  sys.exit(main(parser.parse_args()))

