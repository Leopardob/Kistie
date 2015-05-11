'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Basic Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

import maya.OpenMaya as om
import maya.cmds as cmds
import sys


# Kistie class and class method
class KstOut(object):
    # Debug module name variable
    _debug = 'KstOut'

    # __init__ method
    def __init__(self):
        # self.debug(KstOut._debug, 'Kistie Output module loaded...')
        pass

    # Debug method
    def debug(self, class_name, *args):
        '''
        Desc:
        Debug method, print in debug mode

        Parameter:
        args = debug message

        Return void
        '''

        module_debug = ''

        if class_name == 'KstMaya':
            module_debug = '[Kistie Maya :DEBUG: ]: '

        elif class_name == 'KstAttrs':
            module_debug = '[Kistie Attrs :DEBUG: ]: '

        elif class_name == 'KstMath':
            module_debug = '[Kistie Math :DEBUG: ]: '

        elif class_name == 'KstDraw':
            module_debug = '[Kistie Draw :DEBUG: ]: '

        elif class_name == 'KstRig':
            module_debug = '[Kistie Rig :DEBUG: ]: '

        elif class_name == 'RTS_Rig':
            module_debug = '[Kistie RTS Rig :DEBUG: ]: '

        elif class_name == 'Wing':
            module_debug = '[Kistie RTS Rig -> Wing :DEBUG: ]: '

        elif class_name == 'KstOut':
            module_debug = '[Kistie Output  :DEBUG: ]: '

        elif class_name == 'KstCore':
            module_debug = '[Kistie Core  :DEBUG: ]: '

        debug_message = str(args).replace(',','').replace('(','').replace(')','').replace("'",'')
        # print (module_debug+debug_message)

    def error(self, class_name, *args):
        '''
        Desc:
        Error method, print in error mode

        Parameter:
        args = error message

        Return void
        '''

        module_error = ''

        if class_name == 'KstMaya':
            module_error = '[Kistie Maya :ERROR: ]: '

        elif class_name == 'KstAttrs':
            module_error = '[Kistie Attrs :ERROR: ]: '

        elif class_name == 'KstMath':
            module_error = '[Kistie Math :ERROR: ]: '

        elif class_name == 'KstDraw':
            module_error = '[Kistie Draw :ERROR: ]: '

        elif class_name == 'KstRig':
            module_error = '[Kistie Rig :ERROR: ]: '

        elif class_name == 'RTS_Rig':
            module_error = '[Kistie RTS Rig :ERROR: ]: '

        elif class_name == 'Wing':
            module_error = '[Kistie RTS Rig -> Wing :ERROR: ]: '

        elif class_name == 'KstOut':
            module_debug = '[Kistie Output  :ERROR: ]: '

        elif class_name == 'KstCore':
            module_debug = '[Kistie Core  :ERROR: ]: '

        error_message = str(args).replace(',','').replace('(','').replace(')','').replace("'",'')
        cmds.error(module_error+error_message)

    def call_back_ouput(msg, msg_type, filter_output, data):
        om.MScriptUtil.setBool(filter_output, True)
        line = str(msg)
        if msg_type == om.MCommandMessage.kWarning:
            line = 'W-->'
        if msg_type == om.MCommandMessage.kError:
            line = 'E-->'
        if msg_type == om.MCommandMessage.kResult:
            line = 'R-->'

        #sys.__stdout__.write(line)
        #sys.__stdout__.flush()

        '''
        # Call back add
        callback_id = om.MCommandMessage.addCommandOutputFilterCallback(KstOut.call_back_ouput, None)

        # Call back end
        om.MCommandMessage.removeCallback(KstOut.call_back_ouput)
        '''
