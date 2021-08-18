library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

{{#dependencies}}
use work.{{identifier}};
{{/dependencies}}


{{>generic/entity_header.part.tpl}}

architecture Structure of {{identifier}} is

{{#signals}}
{{# is_complex}}
  signal {{identifier_ms}} : {{#is_vector}}{{type.qualified_v_ms}} (0 to {{=size}}{{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{/size}}-1){{|is_vector}}{{type.qualified_ms}}{{/is_vector}};
  signal {{identifier_sm}} : {{#is_vector}}{{type.qualified_v_sm}} (0 to {{=size}}{{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{/size}}-1){{|is_vector}}{{type.qualified_ms}}{{/is_vector}};
{{| is_complex}}
  signal {{identifier}} : {{#is_vector}}{{type.qualified_v}} (0 to {{=size}}{{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{/size}}-1){{|is_vector}}{{type.qualified}}{{/is_vector}};
{{/ is_complex}}
{{/signals}}

begin

{{#instances}}
  {{identifier}} : entity work.{{base.identifier}}
{{? generics}}
    generic map (
{{#  generics}}
{{?   is_assigned}}
{{?    is_complex}}
{{#     assignments}}
      {{..identifier_ms}}({{._idx}}) => {{?is_literal}}{{=value}}{{*type.x_format_ms}}{{/value}}{{|is_literal}}{{qualified_ms}}{{/is_literal}},
      {{..identifier_sm}}({{._idx}}) => {{?is_literal}}{{=value}}{{*type.x_format_sm}}{{/value}}{{|is_literal}}{{qualified_sm}}{{/is_literal}}{{?.._last}}{{?._last}}){{|._last}},{{/._last}}{{|.._last}},{{/.._last}}
{{/     assignments}}
{{#     assignment}}
      {{..identifier_ms}} => {{?is_literal}}{{=value}}{{*type.x_format_ms}}{{/value}}{{|is_literal}}{{qualified_ms}}{{/is_literal}},
      {{..identifier_sm}} => {{?is_literal}}{{=value}}{{*type.x_format_sm}}{{/value}}{{|is_literal}}{{qualified_sm}}{{/is_literal}}{{?.._last}}){{|.._last}},{{/.._last}}
{{/     assignment}}
{{|    is_complex}}
{{#     assignments}}
      {{..identifier}}({{._idx}}) => {{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{?.._last}}{{?._last}}){{|._last}},{{/._last}}{{|.._last}},{{/.._last}}
{{/     assignments}}
{{#     assignment}}
      {{..identifier}} => {{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{?.._last}}){{|.._last}},{{/.._last}}
{{/     assignment}}
{{/    is_complex}}
{{|   is_assigned}}
{{?    is_complex}}
      {{identifier_ms}} => open,
      {{identifier_sm}} => open{{?._last}}){{|._last}},{{/._last}}
{{|    is_complex}}
      {{identifier}} => open{{?._last}}){{|._last}},{{/._last}}
{{/    is_complex}}
{{/   is_assigned}}
{{/  generics}}
{{/ generics}}
    port map (
      pi_clk => pi_clk,
      pi_rst_n => pi_rst_n{{?ports}},{{|ports}});{{/ports}}
{{# ports}}
{{?  is_assigned}}
{{?   is_complex}}
{{#    assignments}}
      {{..identifier_ms}}({{._idx}}) => {{?is_literal}}{{=value}}{{*type.x_format_ms}}{{/value}}{{|is_literal}}{{qualified_ms}}{{/is_literal}},
      {{..identifier_sm}}({{._idx}}) => {{?is_literal}}{{=value}}{{*type.x_format_sm}}{{/value}}{{|is_literal}}{{qualified_sm}}{{/is_literal}}{{?.._last}}{{?._last}});{{|._last}},{{/._last}}{{|.._last}},{{/.._last}}
{{/    assignments}}
{{#    assignment}}
      {{..identifier_ms}} => {{?is_literal}}{{=value}}{{*type.x_format_ms}}{{/value}}{{|is_literal}}{{qualified_ms}}{{/is_literal}},
      {{..identifier_sm}} => {{?is_literal}}{{=value}}{{*type.x_format_sm}}{{/value}}{{|is_literal}}{{qualified_sm}}{{/is_literal}}{{?.._last}});{{|.._last}},{{/.._last}}
{{/    assignment}}
{{|   is_complex}}
{{#    assignments}}
      {{..identifier}}({{._idx}}) => {{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{?.._last}}{{?._last}});{{|._last}},{{/._last}}{{|.._last}},{{/.._last}}
{{/    assignments}}
{{#    assignment}}
      {{..identifier}} => {{?is_literal}}{{=value}}{{*type.x_format}}{{/value}}{{|is_literal}}{{qualified}}{{/is_literal}}{{?.._last}});{{|.._last}},{{/.._last}}
{{/    assignment}}
{{/   is_complex}}
{{|  is_assigned}}
{{?   is_complex}}
      {{identifier_ms}} => open,
      {{identifier_sm}} => open{{?._last}});{{|._last}},{{/._last}}
{{|   is_complex}}
      {{identifier}} => open{{?._last}});{{|._last}},{{/._last}}
{{/   is_complex}}
{{/  is_assigned}}
{{/ ports}}

{{/instances}}
end Structure;
