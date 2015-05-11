'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie OpenGL Module Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

#ToDo: implement a debug mode for print or not, and for pass data to OpenGL

import pymel as pm                                          # import pymel lib
import maya.cmds as cmds                                    # import maya cmds lib

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

class KstDraw(object):
    # Debug module name variable
    _debug = 'KstDraw'

    def __init__(self):
        KstOut.debug('Kistie Draw function module loaded...')

    def debug_axis(self, selections, bool=True):
        '''
        Desc:
        Debug joint axis

        Parameter:
        selections = objec to draw debug
        bool = boolean status

        Return void
        '''
        if (selections):
            try:
                for sel in selections:
                    cmds.setAttr(sel+'.displayLocalAxis', bool)
            except:
                cmds.setAttr(selections+'.displayLocalAxis', bool)
        else:
            KstOut.error(KstDraw._debug, 'You must have a valid selection!')
            KstOut.debug(KstDraw._debug, 'You must have a valid selection!')