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
        p_hsIn=RefSig('hsIntFirst'),
        p_hsOut=RefSig('hsIntMid'),
        p_dataIn=RefSig('dataIntFirst'),
        p_dataOut=RefSig('dataIntMid'),
        p_dummy=RefCon('Dummy'),
        p_done=RefSig('doneMid'))

  Ins('Inner', name='first',
      g_Pattern=LitVec(2,3),
        p_hsIn=RefSig('hsIn'),
        p_hsOut=RefSig('hsIntFirst'),
        p_dataIn=RefSig('dataIn'),
        p_dataOut=RefSig('dataIntFirst'),
        p_dummy=RefCon('LogicNull'),
        p_done=RefSig('doneFirst'))

  Ins('Inner', name='last',
      g_Pattern=LitVec(1,2,4,8),
        p_hsIn=RefSig('hsIntMid'),
        p_hsOut=RefSig('hsOut'),
        p_dataIn=RefSig('dataIntMid'),
        p_dataOut=RefSig('dataOut'),
        p_dummy=Lit(False),
        p_done=RefSig('doneLast'))

  Ins('Barrier',
      g_Dummy=RefCon('LogicNull'),
      g_Mask=RefCon('Mask'),
        p_doneIn=RefSigVec('doneFirst', 'doneMid', 'doneLast'),
        p_done=RefSig('done'))

