p=Pkg('simple',
      x_templates={'package.vhd': 'pkg_simple.vhd'})

p.Typ('Logic', Simple,
      x_definition=lambda:'{{>logic.part}}')

p.Typ('Data', Simple,
      x_width=32,
      x_definition=lambda:'{{>unsigned.part}}')

p.Typ('Handshake', Complex,
      x_definition=lambda:'{{>handshake.part}}')

