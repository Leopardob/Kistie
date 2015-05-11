'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Rig Module Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

class kstSym(object):
    # Debug module name variable
    _debug = 'KstSim'

    def __init__(self):
        KstOut.debug(KstOut._debug, 'Kistie Simulation module loaded...')

    #ToDo