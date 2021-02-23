subtype {{identifier_ms}} is std_logic;
subtype {{identifier_sm}} is std_logic;
subtype {{identifier_v_ms}} is unsigned;
subtype {{identifier_v_sm}} is unsigned;
{{#x_cnull_ms}}
constant {{x_cnull_ms}} : {{identifier_ms}} := '0';
{{/x_cnull_ms}}
{{#x_cnull_sm}}
constant {{x_cnull_sm}} : {{identifier_sm}} := '0';
{{/x_cnull_sm}}
{{#x_cinfo}}
constant {{x_cinfo}} : integer := 108;
{{/x_cinfo}}
