Inc('definitions.py', abs='lib')


Ent('Inner',
    Generic('DataWidth',     T('Size')),
    Generic('PatternLength', T('Size')),
    Generic('Pattern',       T('Integer'), vector='PatternLength'),
    PortS('hsIn',    T('Handshake', pkg='types')),
    PortM('hsOut',   T('Handshake', pkg='types')),
    PortI('dataIn',  T('Data', pkg='types'), vector='DataWidth'),
    PortO('dataOut', T('Data', pkg='types'), vector='DataWidth'),
    PortI('dummy',   T('Logic')),
    PortO('done',    T('Logic')),
    x_templates={File('inner.vhd.tpl'): File('inner.vhd')})

Ent('Barrier',
    Generic('Dummy',     T('Logic')),
    Generic('PortCount', T('Size')),
    Generic('MaskCount', T('Size')),
    Generic('Mask',      T('Integer'), vector='MaskCount'),
    PortI('doneIn', T('Logic'), vector='PortCount'),
    PortO('done',   T('Logic'), x_depends=lambda e: e.ports['doneIn']),
    x_templates={File('barrier.vhd.tpl'): File('barrier.vhd')})

with Ent('Toplevel',
         Generic('DataWidth', T('Size')),
         Generic('MaskCount', T('Size')),
         Generic('Mask',      T('Integer'), vector='MaskCount'),
         Generic('Dummy',     T('Logic'), x_useless=True),
         PortS('hsIn',    T('Handshake')),
         PortM('hsOut',   T('Handshake')),
         PortI('dataIn',  T('Data'), vector='DataWidth'),
         PortO('dataOut', T('Data'), vector='DataWidth'),
         PortO('done',    T('Logic')),
         x_templates={File('generic/entity.vhd.tpl', mod='lib'): File('Toplevel.vhd')}):

  Ins('Inner', 'mid',
      MapGeneric('Pattern', LitV(1, 2, 5)),
      MapPort('hsIn',    S('hsIntFirst')),
      MapPort('hsOut',   S('hsIntMid')),
      MapPort('dataIn',  S('dataIntFirst')),
      MapPort('dataOut', S('dataIntMid')),
      MapPort('dummy',   G('Dummy')),
      MapPort('done',    S('doneMid')))

  Ins('Inner', 'first',
      MapGeneric('Pattern', LitV(2,3)),
      MapPort('hsIn',    S('hsIn')),
      MapPort('hsOut',   S('hsIntFirst')),
      MapPort('dataIn',  S('dataIn')),
      MapPort('dataOut', S('dataIntFirst')),
      MapPort('dummy',   C('LogicNull')),
      MapPort('done',    S('doneFirst')))

  Ins('Inner', 'last',
      MapGeneric('Pattern', LitV(1,2,4,8)),
      MapPort('hsIn',    S('hsIntMid')),
      MapPort('hsOut',   S('hsOut')),
      MapPort('dataIn',  S('dataIntMid')),
      MapPort('dataOut', S('dataOut')),
      MapPort('dummy',   Lit(False)),
      MapPort('done',    S('doneLast')))

  Ins('Barrier', None,
      MapGeneric('Dummy', C('LogicNull')),
      MapGeneric('Mask',  G('Mask')),
      MapPort('doneIn', SV('doneFirst', 'doneMid', 'doneLast')),
      MapPort('done',   S('done')))

