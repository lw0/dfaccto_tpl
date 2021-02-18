p=Pkg('simple',
      x_templates={'package.vhd': 'pkg_simple.vhd'})

p.Typ('Logic', Simple,
      x_definition='{{>logic.part}}')

p.Typ('Data', Simple,
      x_width=32,
      x_definition='{{>unsigned.part}}')

p.Typ('Handshake', Complex,
      x_definition='{{>handshake.part}}')

