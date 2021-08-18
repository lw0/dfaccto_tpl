library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

{{#dependencies}}
use work.{{identifier}};
{{/dependencies}}


{{>lib:generic/entity_header.part.tpl}}


architecture Behavior of {{identifier}} is


begin

  -- Implementation

end Behavior;
