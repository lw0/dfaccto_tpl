p=Pkg('simple',
      x_templates={'package.vhd': 'pkg_simple.vhd'})

p.Typ('Size', simple=True, x_min=0,
      x_definition='{{>t_integer.part}}')

p.Typ('Integer', simple=True,
      x_definition='{{>t_integer.part}}')

p.Typ('Logic', simple=True,
      x_definition='{{>t_logic.part}}')
p.Con('LogicNull', 'Logic', value=False,
      x_definition='{{>c_logic.part}}')

p.Typ('Data', simple=True,
      x_width=32,
      x_definition='{{>t_unsigned.part}}')
p.Con('DataNull', 'Data', value=0,
      x_definition='{{>c_unsigned.part}}')

p.Typ('Handshake', complex=True,
      x_definition='{{>t_handshake.part}}')

