'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Basic Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

# Standard sysOp modules
import sys
import json

# Import maya modules
import maya.cmds as cmds

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

# Import KstRig
import kcode.krig.KstRig as _KstRig_
reload(_KstRig_)
KstRig = _KstRig_.KstRig()

# Import KstAttrs
import kcode.kcore.kmaya.kattrs.KstAttrs as _KstAttrs_
reload(_KstAttrs_)
KstAttrs = _KstAttrs_.KstAttrs

# Kistie, Python path, change if you need
# sys.path.append('C:/DEV/Kistie/')

# Kistie class and class method
class KistieCore(object):

    # Debug module name variable
    _debug = 'KstCore'

    # __init__ method
    def __init__(self):

        # Kistie vars
        self._kst_attr_node_ = ''
        self._kst_attr_name_ = 'storageNode_KST'
        self._kst_naming_convention_data_ = ''

        # KstOut.debug('KstCore', 'Kistie Core module loaded...')

    def create_kistie_node(self, override = False):
        '''
        Desc:
        Create a Kistie node from scratch

        Parameter:
        override = if True will delete the existing node and you will lose ALL informations, so by default it's False, be carefull

        Return None
        '''
        if cmds.objExists(self._kst_attr_name_):
            if override:
                self.delete_kistie_node()
                self._kst_attr_node_ = KstRig.create_maya_node('transform', self._kst_attr_name_)
            else:
                # KstOut.debug(KistieCore._debug, self._kst_attr_name_+' is not overrideable, set override flag properly')
                pass
        else:
            self._kst_attr_node_ = KstRig.create_maya_node('transform', self._kst_attr_name_)

    def delete_kistie_node(self):
        '''
        Desc:
        Delete kistie node

        Parameter:
        self

        Return None
        '''
        cmds.delete(self._kst_attr_name_)
        # KstOut.debug(KistieCore._debug, self._kst_attr_name_+' deleted')

    def write_info_to_node(self, attr_name, attr_str):
        '''
        Desc:
        Write info inside Kistie node

        Parameter:
        attr_name = name of the attribute that will be created
        attr_str = attribute string that'll be contain the info

        Return None
        '''
        # Convert input in a string that can be used in the node
        attr_to_write = str(attr_str).replace("u'",'').replace('[',' ').replace(']',' ').replace("'",' ').replace(' ', '')

        # Write info in then node
        KstAttrs.create_string_attr(self._kst_attr_name_, attr_name, attr_to_write)

    def read_info_from_node(self, attr_name):
        '''
        Desc:
        Write info inside Kistie node

        Parameter:
        attr_name = name of the attribute that will be created
        attr_str = attribute string that'll be contain the info

        Return None
        '''

        objects_str = ''

        if cmds.objExists(self._kst_attr_name_):
            # Read info from node
            object_list_str = cmds.getAttr(self._kst_attr_name_+'.'+attr_name)

            # This part it's tricky, if is splittable, the original attr was a list
            try:
                objects_str = object_list_str.split(',', -1)

            # otherwise just get the value
            except:
                objects_str = object_list_str
                pass
        else:
            # KstOut.debug(KistieCore._debug, self._kst_attr_name_+' does not exists in scene')
            pass
        return objects_str


    def import_naming_convention(self, json_file):
        '''
        Desc:
        Import naming convention from a json file

        Parameter:
        json_file = json_file that contain the naming convention

        Return a dictionary with key:name
        ex. 'joint':'_JNT'
        '''
        pass