from pathlib import Path
import pystache

from . import DFACCTOError, Role, Seq, Context, Frontend


class ContextRenderer:

  def __init__(self, out_path):
    self._out_path = Path(out_path)
    self._templates = dict()
    self._partials = dict()
    self._renderer = pystache.Renderer(partials=self._partials, escape=lambda s: s)

  def load_template(self, tpl_path, tpl_name, is_partial=False):
    tpl_path = Path(tpl_path)
    template = tpl_path.read_text()
    if is_partial:
      self._partials[tpl_name] = template
    else:
      self._templates[tpl_name] = template

  def load_templates(self, search_path, tpl_suffix, partial_suffix=None):
    search_path = Path(search_path)
    for tpl_file in search_path.rglob('*{}'.format(tpl_suffix)):
      name = str(tpl_file.relative_to(search_path))[:-len(tpl_suffix)]
      is_partial = partial_suffix is not None and name.endswith(partial_suffix)
      self.load_template(tpl_file, name, is_partial)

  def render(self, tpl_name, context, out_name=None):
    if tpl_name not in self._templates:
      raise DFACCTOError('Error: unknown template "{}"'.format(tpl_name))
    template = self._templates[tpl_name]
    path = self._out_path / (out_name or tpl_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(self._renderer.render(template, context))


