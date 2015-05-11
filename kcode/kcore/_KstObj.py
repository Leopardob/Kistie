'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Core Module Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

# The basic idea is that core modules contains also all extras
# ex . kstCore.Fabric should contains all Fabric Engine calls
#      kstCore.HDN should contains all Houdini commands
#      kstCore.Blend should contains all Blender commands

# Create _KCORE global var and make it False

import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
from attrs import kstAttrs

class kObj(object):
    def __init__(self):
        name = ''
        id = ''

class nameAttr(kstAttrs.kstAttr):
    def __init__(self):
        self.debug('Kistie Obj function module loaded...')
        kstAttrs.kstAttrs.__init__(self,'name',['str', 'unicode'])

    def set_value(self, instance, value):
        instance.internal_name=cmds.rename(instance.internal_name, value)

    def get_value(self, instance, value):
        return instance.internal_name

    # Debug method
    def debug(self, *args):
        print('[Kistie Core]: '+str(args[0]))

    def name(self):
        kObj=OpenMaya.MObject()
        return kObj