Inc('simple_types.py')


Ent('Inner',
    g_DataWidth='Size',
    g_PatternLength='Size',
    g_Pattern='Integer(PatternLength)',
      ps_hsIn='simple.Handshake', pm_hsOut='simple.Handshake',
      pi_dataIn='simple.Data(DataWidth)',
      po_dataOut='simple.Data(DataWidth)',
      pi_dummy='Logic',
      po_done='simple.Logic')

Ent('Barrier',
    g_Dummy='Logic',
    g_PortCount='Size',
    g_MaskCount='Size',
    g_Mask='Integer(MaskCount)',
      pi_doneIn='Logic(PortCount)',
      po_done='Logic')


with Ent('Toplevel',
         g_DataWidth='Size',
         g_MaskCount='Size',
         g_Mask='Integer(MaskCount)',
         g_Dummy='Logic',
           ps_hsIn='Handshake',
           pm_hsOut='Handshake',
           pi_dataIn='Data(DataWidth)',
           po_dataOut='Data(DataWidth)',
           po_done='Logic',
         x_templates={'entity.vhd': 'Toplevel.vhd'}):

  Ins('Inner', name='mid',
      g_Pattern=LitVec(1,2,5),
        p_hsIn=To('hsIntFirst'),
        p_hsOut=To('hsIntMid'),
        p_dataIn=To('dataIntFirst'),
        p_dataOut=To('dataIntMid'),
        p_dummy=Val('Dummy'),
        p_done=To('doneMid'))

  Ins('Inner', name='first',
      g_Pattern=LitVec(2,3),
        p_hsIn=To('hsIn'),
        p_hsOut=To('hsIntFirst'),
        p_dataIn=To('dataIn'),
        p_dataOut=To('dataIntFirst'),
        p_dummy=Val('LogicNull'),
        p_done=To('doneFirst'))

  Ins('Inner', name='last',
      g_Pattern=LitVec(1,2,4,8),
        p_hsIn=To('hsIntMid'),
        p_hsOut=To('hsOut'),
        p_dataIn=To('dataIntMid'),
        p_dataOut=To('dataOut'),
        p_dummy=Val('LogicNull'),
        p_done=To('doneLast'))

  Ins('Barrier',
      g_Dummy=Val('LogicNull'),
      g_Mask=Val('Mask'),
        p_doneIn=ToVec('doneFirst', 'doneMid', 'doneLast'),
        p_done=To('done'))

