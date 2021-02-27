with Pkg('simple',
         x_templates={'package.vhd': 'pkg_simple.vhd'}):

  Typ('Size', simple=True, x_min=0,
      x_definition='{{>t_integer.part}}')

  Typ('Integer', simple=True,
      x_definition='{{>t_integer.part}}')

  Typ('Logic', simple=True,
      x_definition='{{>t_logic.part}}')
  Con('LogicNull', 'Logic', value=False,
      x_definition='{{>c_logic.part}}')

  Typ('Data', simple=True,
      x_width=32,
      x_definition='{{>t_unsigned.part}}')
  Con('DataNull', 'Data', value=0,
      x_definition='{{>c_unsigned.part}}')

  Typ('Handshake', complex=True,
      x_definition='{{>t_handshake.part}}')

