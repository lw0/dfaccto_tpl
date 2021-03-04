library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

{{#used_packages}}
use work.{{identifier}};
{{/used_packages}}


package {{identifier}} is

-- second constant: {{constants.1}}
-- type named "Logic": {{types.Logic}}
-- Type List:
{{#types}}
--   {{_idx}} - {{.}}
{{/types}}

{{#declarations}}
{{# is_a_type}}
  {{*x_definition}}
{{/ is_a_type}}
{{# is_a_constant}}
{{#  is_complex}}
  constant {{identifier_ms}} : {{type.qualified_ms}} := {{#is_reference}}{{value.qualified_ms}}{{|is_reference}}{{*type.x_format_ms}}{{/is_reference}};
  constant {{identifier_sm}} : {{type.qualified_sm}} := {{#is_reference}}{{value.qualified_sm}}{{|is_reference}}{{*type.x_format_sm}}{{/is_reference}};
{{|  is_complex}}
  constant {{identifier}} : {{type.qualified}} := {{#is_reference}}{{value.qualified}}{{|is_reference}}{{=value}}{{*type.x_format}}{{/value}}{{/is_reference}};
{{/  is_complex}}
{{/ is_a_constant}}

{{/declarations}}
end {{identifier}};
