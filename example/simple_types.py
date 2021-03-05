with Pkg('simple',
         x_templates={'package.vhd': 'pkg_simple.vhd'}):

  Typ('Integer', simple=True,
      x_definition='{{>part/t_integer.part}}',
      x_format='{{>part/f_integer.part}}',
      x_cnull=lambda: Con('IntegerNull', 'Integer', value=Lit(0)))

  Typ('Size', simple=True, x_min=0,
      x_definition='{{>part/t_integer.part}}',
      x_format='{{>part/f_integer.part}}',
      x_cnull=lambda: Con('SizeNull', 'Size', value=Lit(0)))

  Typ('Logic', simple=True,
      x_definition='{{>part/t_logic.part}}',
      x_format='{{>part/f_logic.part}}',
      x_cnull=lambda: Con('LogicNull', 'Logic', value=Lit(False)))

  Typ('Data', simple=True, x_width=32,
      x_definition='{{>part/t_unsigned.part}}',
      x_format='{{>part/f_unsigned.part}}',
      x_cnull=lambda: Con('DataNull', 'Data', value=Lit(0)))

  Typ('Handshake', complex=True,
      x_definition='{{>part/t_handshake.part}}',
      x_format_ms='{{>part/f_handshake_ms.part}}',
      x_format_sm='{{>part/f_handshake_sm.part}}',
      x_cnull=lambda: Con('HandshakeNull', 'Handshake', value=Lit({'ms':False, 'sm':False})))

  Typ('RegMap', simple=True,
      x_definition='{{>part/t_regmap.part}}',
      x_format='{{>part/f_regmap.part}}',
      x_tsize=RefTyp('Size'),
      x_cnull=lambda: Con('RegMapNull', 'RegMap', value=Lit({'offset': 0})))

  Con('TestMapSize', 'Size')
  Con('TestMap', 'RegMap(TestMapSize)',
      value=LitVec({'offset':0, 'count':4}, {'offset':4, 'count':2}, {'offset':8, 'count':8}))

