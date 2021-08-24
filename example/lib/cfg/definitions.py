with Pkg('types',
         x_templates={File('generic/package.vhd.tpl'): File('pkg/types.vhd')}):

  TypeS('Integer',
        x_definition=Part('types/t_integer.part.tpl'),
        x_format=Part('types/f_integer.part.tpl'),
        x_cnull=lambda t: Con('IntegerNull', t, value=Lit(0)))

  TypeS('Size', x_min=0,
        x_definition=Part('types/t_integer.part.tpl'),
        x_format=Part('types/f_integer.part.tpl'),
        x_cnull=lambda t: Con('SizeNull', t, value=Lit(0)))

  TypeS('Logic',
        x_definition=Part('types/t_logic.part.tpl'),
        x_format=Part('types/f_logic.part.tpl'),
        x_cnull=lambda t: Con('LogicNull', t, value=Lit(False)))

  TypeS('Data', x_width=32,
        x_definition=Part('types/t_unsigned.part.tpl'),
        x_format=Part('types/f_unsigned.part.tpl'),
        x_cnull=lambda t: Con('DataNull', t, value=Lit(0)))

  TypeC('Handshake',
        x_definition=Part('types/t_handshake.part.tpl'),
        x_format_ms=Part('types/f_handshake_ms.part.tpl'),
        x_format_sm=Part('types/f_handshake_sm.part.tpl'),
        x_cnull=lambda t: Con('HandshakeNull', t, value=Lit({'ms':False, 'sm':False})))

  TypeS('RegMap',
        x_definition=Part('types/t_regmap.part.tpl'),
        x_format=Part('types/f_regmap.part.tpl'),
        x_tsize=T('Size'),
        x_cnull=lambda t: Con('RegMapNull', t, value=Lit({'offset': 0})))

  Con('TestMapSize', T('Size'))
  Con('TestMap', T('RegMap'), vector='TestMapSize',
      value=LitV({'offset':0, 'count':4}, {'offset':4, 'count':2}, {'offset':8, 'count':8}))

Pkg('util', x_templates={File('util.vhd'): File('pkg/util.vhd')})
