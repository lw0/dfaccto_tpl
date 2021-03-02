library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

{{#used_packages}}
use work.{{identifier}};
{{/used_packages}}


entity {{identifier}} is
{{?generics}}
  generic (
{{# generics}}
{{#  is_complex}}
    {{identifier_ms}} : {{#is_scalar}}{{type.qualified_ms}}{{|is_scalar}}{{type.qualified_v_ms}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{/is_scalar}}{{?_last}}){{/_last}};
    {{identifier_sm}} : {{#is_scalar}}{{type.qualified_sm}}{{|is_scalar}}{{type.qualified_v_sm}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{/is_scalar}}{{?_last}}){{/_last}};
{{|  is_complex}}
    {{identifier}} : {{#is_scalar}}{{type.qualified}}{{|is_scalar}}{{type.qualified_v}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{/is_scalar}}{{?_last}}){{/_last}};
{{/  is_complex}}
{{/ generics}}
{{/generics}}
  port (
    pi_clk : in std_logic;
    pi_rst_n : in std_logic{{^ports}}){{/ports}};
{{#ports}}
{{# is_complex}}
    {{identifier_ms}} : {{mode_ms}} {{#is_scalar}}{{type.qualified_ms}}{{|is_scalar}}{{type.qualified_v_ms}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{/is_scalar}};
    {{identifier_sm}} : {{mode_sm}} {{#is_scalar}}{{type.qualified_sm}}{{|is_scalar}}{{type.qualified_v_sm}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{/is_scalar}}{{?_last}}){{/_last}};
{{| is_complex}}
    {{identifier}} : {{mode}} {{#is_scalar}}{{type.qualified}}{{|is_scalar}}{{type.qualified_v}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{/is_scalar}}{{?_last}}){{/_last}};
{{/ is_complex}}
{{/ports}}
end {{identifier}};


architecture Structure of {{identifier}} is

{{#signals}}
{{# is_complex}}
  signal {{identifier_ms}} : {{#is_vector}}{{type.qualified_v_ms}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{|is_vector}}{{type.qualified_ms}}{{/is_vector}};
  signal {{identifier_sm}} : {{#is_vector}}{{type.qualified_v_sm}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{|is_vector}}{{type.qualified_ms}}{{/is_vector}};
{{| is_complex}}
  signal {{identifier}} : {{#is_vector}}{{type.qualified_v}} (0 to {{=size}}{{>part/put_value.part}}{{/size}}-1){{|is_vector}}{{type.qualified}}{{/is_vector}};
{{/ is_complex}}
{{/signals}}

begin

{{#instances}}
  {{identifier}} : entity work.{{base.identifier}}
{{? generics}}
    generic map (
{{#  generics}}
      -- {{name}}:
{{?   knows_value}}
{{#    values}}
{{?     is_literal}}
{{?      is_complex}}
      {{identifier_ms}}({{_idx}}) => {{*type.x_format_ms}},
      {{identifier_sm}}({{_idx}}) => {{*type.x_formst_sm}}{{?_last}}{{?'_last}}){{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{|      is_complex}}
      {{identifier}}({{_idx}}) => {{*type.x_format}}{{?_last}}{{?'_last}}){{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{/      is_complex}}
{{|     is_literal}}
{{?      is_complex}}
      {{'identifier_ms}}({{_idx}}) => {{qualified_ms}},
      {{'identifier_sm}}({{_idx}}) => {{qualified_sm}}{{?_last}}{{?'_last}}){{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{|      is_complex}}
      {{'identifier}}({{_idx}}) => {{qualified}}{{?_last}}{{?'_last}}){{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{/      is_complex}}
{{/     is_literal}}
{{/    values}}
{{#    value}}
{{?     is_literal}}
{{?      is_complex}}
      {{identifier_ms}} => {{*type.x_format_ms}},
      {{identifier_sm}} => {{*type.x_formst_sm}}{{?_last}}){{|_last}},{{/_last}}
{{|      is_complex}}
      {{identifier}} => {{*type.x_format}}{{?_last}}){{|_last}},{{/_last}}
{{/      is_complex}}
{{|     is_literal}}
{{?      is_complex}}
      {{'identifier_ms}} => {{qualified_ms}},
      {{'identifier_sm}} => {{qualified_sm}}{{?_last}}){{|_last}},{{/_last}}
{{|      is_complex}}
      {{'identifier}} => {{qualified}}{{?_last}}){{|_last}},{{/_last}}
{{/      is_complex}}
{{/     is_literal}}
{{/    value}}
{{|   knows_value}}
{{?    is_complex}}
      {{identifier_ms}} => open,
      {{identifier_sm}} => open{{?_last}}){{|_last}},{{/_last}}
{{|    is_complex}}
      {{identifier}} => open{{?_last}}){{|_last}},{{/_last}}
{{/    is_complex}}
{{/   knows_value}}
{{/  generics}}
{{/ generics}}
    port map (
      pi_clk => pi_clk,
      pi_rst_n => pi_rst_n{{?ports}},{{|ports}});{{/ports}}
{{# ports}}
{{#  connections}}
{{#   is_complex}}
      {{'identifier_ms}}({{_idx}}) => {{qualified_ms}},
      {{'identifier_sm}}({{_idx}}) => {{qualified_sm}}{{?_last}}{{?'_last}});{{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{|   is_complex}}
      {{'identifier}}({{_idx}}) => {{qualified}}{{?_last}}{{?'_last}});{{|'_last}},{{/'_last}}{{|_last}},{{/_last}}
{{/   is_complex}}
{{/  connections}}
{{#  connection}}
{{#   is_complex}}
      {{'identifier_ms}} => {{qualified_ms}},
      {{'identifier_sm}} => {{qualified_sm}}{{?_last}});{{|_last}},{{/_last}}
{{|   is_complex}}
      {{'identifier}} => {{qualified}}{{?_last}});{{|_last}},{{/_last}}
{{/   is_complex}}
{{/  connection}}
{{^  is_connected}}
{{?   is_complex}}
      {{identifier_ms}} => open,
      {{identifier_sm}} => open{{?_last}});{{|_last}},{{/_last}}
{{|   is_complex}}
      {{identifier}} => open{{?_last}});{{|_last}},{{/_last}}
{{/   is_complex}}
{{/  is_connected}}
{{/ ports}}

{{/instances}}
end Structure;
