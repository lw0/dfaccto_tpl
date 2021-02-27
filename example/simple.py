Inc('simple_types.py')


Ent('Inner',
    g_DataWidth='Size',
    g_PatternLength='Size',
    g_Pattern='Integer(PatternLength)',
      ps_hsIn='simple.Handshake', pm_hsOut='simple.Handshake',
      pi_dataIn='simple.Data(DataWidth)',
      po_dataOut='simple.Data(DataWidth)',
      # pi_dummy='Logic',
      po_done='simple.Logic')

Ent('Barrier',
    g_PortCount='Size',
    g_MaskCount='Size',
    g_Mask='Integer(MaskCount)',
      pi_doneIn='Logic(PortCount)',
      po_done='Logic')


e=Ent('Toplevel',
      g_DataWidth='Size',
      g_MaskCount='Size',
      g_Mask='Integer(MaskCount)',
      g_Dummy='Logic',
        ps_hsIn='Handshake',
        pm_hsOut='Handshake',
        pi_dataIn='Data(DataWidth)',
        po_dataOut='Data(DataWidth)',
        po_done='Logic',
      x_templates={'entity.vhd': 'Toplevel.vhd'})

e.Ins('Inner', name='mid',
      g_Pattern=(1,2,5),
        p_hsIn=e.To('hsIntFirst'),
        p_hsOut=e.To('hsIntMid'),
        p_dataIn=e.To('dataIntFirst'),
        p_dataOut=e.To('dataIntMid'),
        # p_dummy=e.Val('Dummy'),
        p_done=e.To('doneMid'))

e.Ins('Inner', name='first',
      g_Pattern=(2,3),
        p_hsIn=e.To('hsIn'),
        p_hsOut=e.To('hsIntFirst'),
        p_dataIn=e.To('dataIn'),
        p_dataOut=e.To('dataIntFirst'),
        # p_dummy=e.Val('LogicNull'),
        p_done=e.To('doneFirst'))

e.Ins('Inner', name='last',
      g_Pattern=(1,2,4,8),
        p_hsIn=e.To('hsIntMid'),
        p_hsOut=e.To('hsOut'),
        p_dataIn=e.To('dataIntMid'),
        p_dataOut=e.To('dataOut'),
        # p_dummy=e.Val('LogicNull'),
        p_done=e.To('doneLast'))

e.Ins('Barrier',
      g_Mask=e.Val('Mask'),
        p_doneIn=e.ToVec('doneFirst', 'doneMid', 'doneLast'),
        p_done=e.To('done'))

