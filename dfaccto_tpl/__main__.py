import argparse
from itertools import chain
from pathlib import Path
import re
import sys
import shutil
import traceback

from .cmdline import Cmdline
from .configreader import ConfigReader
from .contextrenderer import ContextRenderer
from .util import DFACCTOError


def print_status(inspec, outspec, element=None):
  inname = '{}:{}'.format(inspec.module or '', inspec.name)
  outname = '{}:{}'.format(outspec.module or '', outspec.name)
  if element is not None:
    elementname = '{}:{}'.format(type(element).__name__, str(element))
  else:
    elementname = ''
  print('{:>32s} ---{:-^32s}---> {:<32s}'.format(inname, elementname, outname))

def main():
  args = Cmdline.parse()
  try:
    reader = ConfigReader(args)
    reader.read(args.entry(), abs=True)

    context = reader.context
    if args.debug():
      breakpoint()

    renderer = ContextRenderer(args)

    renderer.empty()

    element_iter = chain((context,), context.packages.contents(), context.entities.contents())
    for element in element_iter:
      for tpl_spec,out_spec in element.props.get('templates', {}).items():
        renderer.render(tpl_spec, out_spec, element)
        print_status(tpl_spec, out_spec, element)

    renderer.write_rendered()

  except DFACCTOError as e:
    print(e, file=sys.stderr)
    return 1

  except Exception as e:
    print('Unexpected error:', file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    return 1

  return 0


if __name__ == "__main__":
  sys.exit(main())

