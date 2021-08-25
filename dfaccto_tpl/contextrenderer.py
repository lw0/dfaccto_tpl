from functools import partial
from pathlib import Path
import re
import shutil

from .template import parse, TemplateError
from .util import DFACCTOError, ModuleRef, resolve_path



class ContextRenderer:

  def __init__(self, args):
    self._args = args
    self._templates = dict()
    self._rendered = list()

  def _get_template(self, tpl_spec):
    if not isinstance(tpl_spec, ModuleRef):
      raise DFACCTOError('Error: invalid template specification "{}"'.format(tpl_spec))
    if tpl_spec in self._templates:
      return self._templates[tpl_spec]

    tpl_path = resolve_path(self._args.tpldirs(tpl_spec.module), tpl_spec.name)
    if tpl_path is None:
      raise DFACCTOError('Error: Can not find template "{}" in module {}'.format(tpl_spec.name, tpl_spec.module))
    tpl_name = '{}:{}'.format(tpl_spec.module or '', tpl_spec.name)
    tpl_content = tpl_path.read_text()
    try:
      tpl = parse(tpl_content, tpl_name, module=tpl_spec.module)
    except TemplateError as e:
      raise DFACCTOError(str(e))
    self._templates[tpl_spec] = tpl

    return tpl

  PARTIAL_FORMAT = re.compile('(?:(\w*):)?(\S+)')

  def _get_partial(self, identifier, template):
    if m := type(self).PARTIAL_FORMAT.fullmatch(identifier):
      if m.group(1) is None: # "name" -> use module of invoking template
        module = template.module
      elif m.group(1): # "mod:name" -> use module "mod"
        module = m.group(1)
      else: # ":name" -> use default module
        module = None
      name = m.group(2)
      spec = ModuleRef(module, name)
      return self._get_template(spec)
    else:
      raise DFACCTOError('Error: Invalid partial identifier "{}"'.format(identifier))

  def _get_outpath(self, out_spec):
    if not isinstance(out_spec, ModuleRef):
      raise DFACCTOError('Error: invalid output file specification "{}"'.format(out_spec))
    module_dir = 'mod_{}'.format(out_spec.module) if out_spec.module is not None else 'mod'
    path = self._args.outdir() / module_dir / out_spec.name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
      raise DFACCTOError('Error: would override existing file "{}"'.format(path))
    return path

  def empty(self):
    for item in self._args.outdir().iterdir():
      if item.is_dir():
        shutil.rmtree(item)
      else:
        item.unlink()

  def render(self, tpl_spec, out_spec, context):
    template = self._get_template(tpl_spec)
    outpath = self._get_outpath(out_spec)
    try:
      outpath.write_text(template.render(context, partial=self._get_partial))
      self._rendered.append(outpath)
    except TemplateError as e:
      raise DFACCTOError(str(e))

  def write_rendered(self):
    self._rendered.append('')
    if self._args.outlist() is not None:
      self._args.outlist().write_text('\n'.join(str(path) for path in self._rendered))

