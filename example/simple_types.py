p=Pkg('simple',
      x_templates={'package.vhd': 'pkg_simple.vhd'})

p.Typ('Logic', Simple,
      x_definition='{{>logic.part}}')

p.Typ('Data', Simple,
      x_width=32,
      xI_cnull='c_{name}Null{dir}',
      xi_cwidth='c_{name}Width',
      x_definition='{{>unsigned.part}}')

p.Typ('Handshake', Complex,
      xi_cnull='c_{name}Null{dir}',
      xi_cinfo='c_{name}Info',
      x_definition='{{>handshake.part}}')

