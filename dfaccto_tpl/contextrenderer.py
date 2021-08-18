from functools import partial
from pathlib import Path
import re
import shutil

from .template import parse, TemplateError
from .util import DFACCTOError, ModuleRef, resolve_path



class ContextRenderer:

  PARTIAL_FORMAT = re.compile('(?:(\w+):)?(\S+)')

  def __init__(self, args):
    self._args = args
    self._templates = dict()

  # def _load_templates(self):
  #   for module in self._args.modules():
  #     pattern = '*{}'.format(self._args.tplsuffix(module))
  #     partsuffix = self._args.partsuffix(module)
  #     for dir in self._args.tpldirs(module):
  #       for tpl_file in dir.rglob(pattern):
  #         tpl_name = str(tpl_file.relative_to(search_path))[:-len(tpl_suffix)]
  #         is_partial = name.endswith(partsuffix)
  #         tpl_content = tpl_file.read_text()
  #         try:
  #           tpl = parse(tpl_content, tpl_name, module=module)
  #         except TemplateError as e:
  #           raise DFACCTOError(str(e))
  #         if name.endswith(partsuffix):
  #           self._partials[(module, tpl_name)] = tpl
  #         else:
  #           self._templates[(module, tpl_name)] = tpl

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
    if out_spec.module is None:
      path = self._args.outdir() / out_spec.name
    else:
      path = self._args.outdir() / out_spec.module / out_spec.name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
      raise DFACCTOError('Error: would override existing file "{}"'.format(path))
    return path

  # def _get_statpath(self, stat_spec):
  #   if not isinstance(stat_spec, ModuleRef):
  #     raise DFACCTOError('Error: invalid file specification "{}"'.format(stat_spec))
  #   path = resolve_path(self._args.statdirs(stat_spec.module), stat_spec.name)
  #   if path is None:
  #     raise DFACCTOError('Error: Can not find static file "{}" in module {}'.format(stat_spec.name, stat_spec.module))
  #   return path

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
    except TemplateError as e:
      raise DFACCTOError(str(e))

  # def copy(self, stat_spec, out_spec):
  #   inpath = self._get_statpath(stat_spec)
  #   outpath = self._get_outpath(out_spec)
  #   shutil.copy(inpath, outpath)


