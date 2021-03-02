with Pkg('simple',
         x_templates={'package.vhd': 'pkg_simple.vhd'}):


  Typ('Size', simple=True, x_min=0,
      x_definition='{{>part/t_integer.part}}',
      x_format='{{>part/f_integer.part}}')


  Typ('Integer', simple=True,
      x_definition='{{>part/t_integer.part}}',
      x_format='{{>part/f_integer.part}}')


  Typ('Logic', simple=True,
      x_definition='{{>part/t_logic.part}}',
      x_format='{{>part/f_logic.part}}')

  Con('LogicNull', 'Logic', value=Lit(False))


  Typ('Data', simple=True, x_width=32,
      x_definition='{{>part/t_unsigned.part}}',
      x_format='{{>part/f_unsigned.part}}')

  Con('DataNull', 'Data', value=Lit(0))


  Typ('Handshake', complex=True,
      x_definition='{{>part/t_handshake.part}}',
      x_format_ms='{{>part/f_handshake_ms.part}}',
      x_format_sm='{{>part/f_handshake_sm.part}}')

  Con('HandshakeNull', 'Handshake', value=Lit({'ms':False, 'sm':False}))

