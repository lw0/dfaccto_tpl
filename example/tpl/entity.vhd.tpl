library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

{{#used_packages}}
use work.{{identifier}};
{{/used_types}}


entity {{identifier}} is
{{#has_generics}}
  generic (
{{# generics}}
{{#  is_complex}}
    {{identifier_ms}} : {{#is_scalar}}{{type.qualified_ms}}{{|is_scalar}}{{type.qualified_v_ms}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{/is_scalar}}{{#_last}}){{/_last}};
    {{identifier_sm}} : {{#is_scalar}}{{type.qualified_sm}}{{|is_scalar}}{{type.qualified_v_sm}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{/is_scalar}}{{#_last}}){{/_last}};
{{|  is_complex}}
    {{identifier}} : {{#is_scalar}}{{type.qualified}}{{|is_scalar}}{{type.qualified_v}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{/is_scalar}}{{#_last}}){{/_last}};
{{/  is_complex}}
{{/ generics}}
{{/has_generics}}
  port (
    pi_clk : in std_logic;
    pi_rst_n : in std_logic{{^has_ports}}){{/has_ports}};
{{#has_ports}}

{{#ports}}
{{# is_complex}}
    {{identifier_ms}} : {{mode_ms}} {{#is_scalar}}{{type.qualified_ms}}{{|is_scalar}}{{type.qualified_v_ms}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{/is_scalar}};
    {{identifier_sm}} : {{mode_sm}} {{#is_scalar}}{{type.qualified_sm}}{{|is_scalar}}{{type.qualified_v_sm}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{/is_scalar}}{{#_last}}){{/_last}};
{{| is_complex}}
    {{identifier}} : {{mode}} {{#is_scalar}}{{type.qualified}}{{|is_scalar}}{{type.qualified_v}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{/is_scalar}}{{#_last}}){{/_last}};
{{/ is_complex}}
{{/ports}}
{{/has_ports}}
end {{identifier}};


architecture Structure of {{identifier}} is

{{#signals}}
{{# is_complex}}
  signal {{identifier_ms}} : {{#is_vector}}{{type.qualified_v_ms}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{|is_vector}}{{type.qualified_ms}}{{/is_vector}};
  signal {{identifier_sm}} : {{#is_vector}}{{type.qualified_v_sm}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{|is_vector}}{{type.qualified_ms}}{{/is_vector}};
{{| is_complex}}
  signal {{identifier}} : {{#is_vector}}{{type.qualified_v}} (0 to {{#size}}{{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{/size}}-1){{|is_vector}}{{type.qualified}}{{/is_vector}};
{{/ is_complex}}
{{/signals}}

begin

{{#instances}}
  {{identifier}} : entity work.{{base.identifier}}
{{# has_generics}}
    generic map (
{{#  generics}}
{{#   has_value}}
{{#    is_complex}}
      {{identifier_ms}} => {{#is_reference}}{{value.qualified_ms}}{{|is_reference}}{{*type.x_format_ms}}{{/is_reference}},
      {{identifier_sm}} => {{#is_reference}}{{value.qualified_sm}}{{|is_reference}}{{*type.x_format_sm}}{{/is_reference}}{{#_last}}){{|_last}},{{/_last}}
{{|    is_complex}}
      {{identifier}} => {{#is_reference}}{{value.qualified}}{{|is_reference}}{{*type.x_format}}{{/is_reference}}{{#_last}}){{|_last}},{{/_last}}
{{/    is_complex}}
{{/   has_value}}
{{^   has_value}}
      {{identifier}} => open{{#_last}}){{|_last}},{{/_last}}
{{/   has_value}}
{{/  generics}}
{{/ has_generics}}
    port map (
      pi_clk => pi_clk,
      pi_rst_n => pi_rst_n,
{{# ports}}
{{^  is_connected}}
      {{identifier}} => open{{#_last}});{{|_last}},{{/_last}}
{{/  is_connected}}
{{#  connections}}
{{#   is_simple}}
      {{'identifier}}({{_idx}}) => {{qualified}}{{#_last}}{{#'_last}});{{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{/   is_simple}}
{{#   is_complex}}
      {{'identifier_ms}}({{_idx}}) => {{qualified_ms}},
      {{'identifier_sm}}({{_idx}}) => {{qualified_sm}}{{#_last}}{{#'_last}});{{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{/   is_complex}}
{{/  connections}}
{{#  connection}}
{{#   is_simple}}
      {{'identifier}} => {{qualified}}{{#_last}});{{|_last}},{{/_last}}
{{/   is_simple}}
{{#   is_complex}}
      {{'identifier_ms}} => {{qualified_ms}},
      {{'identifier_sm}} => {{qualified_sm}}{{#_last}});{{|_last}},{{/_last}}
{{/   is_complex}}
{{/  connection}}
{{/ ports}}

{{/instances}}
end Structure;
