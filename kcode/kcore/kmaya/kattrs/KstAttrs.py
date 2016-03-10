'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Attrs Class lib
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

import maya.cmds as cmds

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

class KstAttrs(object):

    # Debug module name variable
    _debug = 'KstAttrs'

    def __init__(self):
        KstOut.debug(KstAttrs._debug, 'Kistie Maya Attrs function module loaded...')


    # Lock attr function
    def lock_attr(self, obj_name, attr_name):
        '''
        Desc:
        Lock maya attr

        Parameter:
        obj_name = object name that contains the attr
        attr_name = attr name

        Return value
        '''
        cmds.setAttr(obj_name+'.'+attr_name, l=True, k=False)

    # Unlock attr function
    def unlock_attr(self, obj_name, attr_name):
        '''
        Desc:
        Unlock maya attr

        Parameter:
        obj_name = object name that contains the attr
        attr_name = attr name

        Return value
        '''
        cmds.setAttr(obj_name+'.'+attr_name, l=False, k=True)


    # Set function for maya attributes
    def set_attr(self, obj_name, attr_name, attr_value):
        '''
        Desc:
        Set maya attribute

        Parameter:
        obj_name = object name that contains the attr
        attr_name = attr name
        attr_value = attr value to set

        Return value
        '''
        cmds.setAttr(obj_name+'.'+attr_name, attr_value)
        return attr_value

    # Get function for maya attributes
    def get_attr(self, obj_name, attr_name):
        '''
        Desc:
        Get maya attribute

        Parameter:
        obj_name = object name that contains the attr
        attr_name = attr name

        Return value
        '''
        attr_value = cmds.getAttr(obj_name+'.'+attr_name)
        return attr_value

    @staticmethod
    def create_float_attr(obj, attr_name, default_value=0, limit_min=False, limit_max=False, min=0, max=1):
        '''
        Desc:
        Make float attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        default_value = attr default value
        limit_min = attr min value
        limit_max = attr max value
        min = min value
        max = max value

        Return string
        obj.attrname
        '''
        cmds.addAttr(obj, shortName=attr_name, longName=attr_name, dv=default_value, attributeType='float', min=min, max=max)
        cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True)
        return obj+'.'+attr_name

    @staticmethod
    def create_double_attr(obj, attr_name, default_value=0, limit_min=False, limit_max=False, min=0, max=1):
        '''
        Desc:
        Make double attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        default_value = attr default value
        limit_min = attr min value
        limit_max = attr max value
        min = min value
        max = max value

        Return string
        obj.attrname
        '''
        cmds.addAttr(obj, shortName=attr_name, longName=attr_name, dv=default_value, attributeType='double')
        cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True)
        return obj+'.'+attr_name

    @staticmethod
    def create_vector_attr(obj, attr_name, default_value=[0,0,0]):
        '''
        Desc:
        Make vector attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        default_value = attr default vector

        Return string
        obj.attrname
        '''
        cmds.addAttr(obj, shortName=attr_name, longName=attr_name, attributeType='double3')
        cmds.addAttr(obj, shortName=attr_name+'X', longName=attr_name+'X', attributeType='double', p=attr_name)
        cmds.addAttr(obj, shortName=attr_name+'Y', longName=attr_name+'Y', attributeType='double', p=attr_name)
        cmds.addAttr(obj, shortName=attr_name+'Z', longName=attr_name+'Z', attributeType='double', p=attr_name)
        cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True)
        cmds.setAttr(obj+'.'+attr_name+'X', e=True, keyable=True)
        cmds.setAttr(obj+'.'+attr_name+'Y', e=True, keyable=True)
        cmds.setAttr(obj+'.'+attr_name+'Z', e=True, keyable=True)
        return obj+'.'+attr_name

    @staticmethod
    def create_bool_attr(obj, attr_name, value=False):
        '''
        Desc:
        Make bool attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        default_value = attr default bool

        Return string
        obj.attrname
        '''
        cmds.addAttr(obj, shortName=attr_name, longName=attr_name, attributeType='bool')
        cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True)
        cmds.setAttr(obj+'.'+attr_name, value)
        return obj+'.'+attr_name

    @staticmethod
    def create_string_attr(obj, attr_name, str):
        '''
        Desc:
        Make string attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        str = string value

        Return string
        obj.attrname
        '''

        #print('current_obj: ', obj)
        #print('attr_name: ', attr_name)
        #print('str', str)

        # Check if current attribute exists, if not, will add
        if not cmds.attributeQuery(attr_name, node=obj, exists = True):
            cmds.addAttr(obj, shortName=attr_name, longName=attr_name, dt='string')
            cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True)
            cmds.setAttr(obj+'.'+attr_name, str, type='string')
        else:
            KstOut.debug(KstAttrs._debug, 'Attribute %s already exists on node %s, skipped' % (attr_name, obj))

        return obj+'.'+attr_name

    @staticmethod
    def create_enum_attr(obj, attr_name, enum_list):
        '''
        Desc:
        Make enum attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        enum_list = enum value list

        Return string
        obj.attrname
        '''
        cmds.addAttr(obj, shortName=attr_name, longName=attr_name, attributeType='enum', en=enum_list)
        cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True)
        return obj+'.'+attr_name

    @staticmethod
    def create_matrix_attr(obj, attr_name, matrix):
        '''
        Desc:
        Make matrix attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        matrix = matrix

        Return matrix
        obj.attrname
        '''
        KstOut.debug(KstAttrs._debug, 'Matrix attr, not implemented yet!')
        pass

    @staticmethod
    def create_separator_attr(obj, attr_name, enum_list='_'*16+':'):
        '''
        Desc:
        Make separator attr

        Parameter:
        obj = object to attach attr
        attr_name = attr name
        enum_list = enum value list

        Return string
        obj.attrname
        '''
        cmds.addAttr(obj, shortName=attr_name, longName=attr_name, attributeType='enum', en=enum_list)
        cmds.setAttr(obj+'.'+attr_name, e=True, keyable=True, lock=True)
        return obj+'.'+attr_name

    @staticmethod
    def read_message_attr(obj_attr_name, *args):
        '''
        Desc:
        Read a message attr

        Parameter:
        obj = object that contain message attr
        attr_name = attr name
        args = other inputs

        Return string
        obj.attrname
        '''

        # Object
        obj = str(obj_attr_name).split('.')[0]

        # Attr name
        attr_name = str(obj_attr_name).split('.')[1]

        # Connections
        connections = cmds.listConnections(obj+'.'+attr_name, s=1)
        return connections[0]

    def create_tag_attr(self, obj, tag_name, tag_value):
        '''
        Desc:
        Create a tag for selected object

        Parameter:
        obj = object that contain tag
        tag = tag name
        value = tag value

        Return:
        obj.tag_name
        '''

        # Check if obj is valid
        if (obj):
            if not cmds.attributeQuery(tag_name, node=obj, exists = True):
                cmds.addAttr(obj, shortName=tag_name, longName=tag_name, dt='string')
                cmds.setAttr(obj+'.'+tag_name, e=True, keyable=False)
                cmds.setAttr(obj+'.'+tag_name, tag_value, type='string')
                KstAttrs.lock_attr(self, obj, tag_name)
            else:
                pass
                #print('Attribute %s already exists on node %s, skipped' % (tag_name, obj))

        return obj+'.'+tag_name


    def __get__(self, instance, owner):
        '''
        :param instance:
        :param owner:
        :return:
        '''
        return self.getValue(instance)

    def __set__(self, instance, value):
        '''
        :param instance:
        :param value:
        :return:
        '''
        if not self.checkDataType(value):
            return

        self.setValue(instance, value)

    def setValue(self, instance, value):
        '''
        :param instance:
        :return:
        '''
        raise NotImplementedError()

    def getValue(self, instance):
        '''
        :param value:
        :return:
        '''
        raise NotImplementedError()

    def checkDataType(self, value):
        '''
        :param value:
        :return:
        '''
        if type(self.data_type).__name__ != 'list':
            if type(value).__name__ != self.data_type:
                raise ValueError("Attribute : expected {x} got {y})".format(x=self.data_type, y=type(value).__name__))
            else:
                return True
        else:
            if type(value).__name__ not in self.data_type:
                raise ValueError("Attribute : expected {x} got {y}".format(
                    x=self.data_type, y=type(value).__name__))
            else:
                return 1