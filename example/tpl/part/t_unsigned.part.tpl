subtype {{identifier}} is unsigned ({{x_width}}-1 downto 0);
type {{identifier_v}} is array (integer range <>) of {{identifier}};
{{#x_cnull}}
constant {{x_cnull}} : {{identifier}} := to_unsigned(0, {{x_width}});
{{/x_cnull}}
{{#x_cwidth}}
constant {{x_cwidth}} : integer := {{x_width}};
{{/x_cwidth}}

