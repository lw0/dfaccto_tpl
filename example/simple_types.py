p=Pkg('simple',
      x_templates={'package.vhd': 'pkg_simple.vhd'})

p.Typ('Size', Simple, x_min=0,
      x_definition='{{>integer.part}}')

p.Typ('Logic', Simple,
      x_definition='{{>logic.part}}')

p.Typ('Data', Simple,
      x_width=32,
      x_definition='{{>unsigned.part}}')

p.Typ('Handshake', Complex,
      x_definition='{{>handshake.part}}')

