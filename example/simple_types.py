p=Pkg('simple',
      x_templates={'package.vhd': 'pkg_simple.vhd'})

p.Typ('Size', Simple, x_min=0,
      x_definition='{{>integer.part}}')

p.Typ('Integer', Simple,
      x_definition='{{>integer.part}}')

p.Typ('Logic', Simple,
      x_definition='{{>logic.part}}')

p.Typ('Data', Simple,
      x_width=32,
      x_definition='{{>t_unsigned.part}}')
p.Con('DataNull', 'Data', value=0,
      x_definition='{{>c_unsigned.part}}')

p.Typ('Handshake', Complex,
      x_definition='{{>handshake.part}}')

