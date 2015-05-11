'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
MDR module, for Kistie Rig
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

# Import KstAttrs
import kcode.kcore.kmaya.kattrs.KstAttrs as _KstAttrs_
reload(_KstAttrs_)
KstAttrs = _KstAttrs_.KstAttrs()

# Import KstMaya
import kcode.kcore.KstMaya as _KstMaya_
reload(_KstMaya_)
KstMaya = _KstMaya_.KstMaya()

# Import KstRig
import kcode.krig.KstRig as _KstRig_
reload(_KstRig_)
KstRig = _KstRig_.KstRig()

# Import KstRig
import kcode.kmath.KstMath as _KstMath_
reload(_KstMath_)
KstMath = _KstMath_.KstMath()

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

class RTS_Rig(object):
    # Debug module name variable
    _debug = 'RTS_Rig'

    def __init__(self):
        KstOut.debug(RTS_Rig._debug, 'Kistie Rig extension for RTS project loaded...')

    # Create a curve degree 2 from 2 objects ToDo: make procedural and implement degree correctly
    @staticmethod
    def create_curve_from_2_obj(obja, objc, crv_name='name_part_idxxx_type'):
        '''
        Desc:
        Make a line between 2 objects

        Parameter:
        crvname = name of curve
        pta = first object
        ptb = second object

        Return: Curve name
        '''

        curve = ''
        objb = str(objc).replace('down', 'mid')

        # Create a locator in the middle of the point inputs
        objb = KstRig.create_maya_node('locator', name=objb)

        # Create a top group on locator and parent locator to it
        tgroup_objb = cmds.group(em=True, name=objb.replace('_LOC','_GRP'))
        cmds.parent(objb, tgroup_objb)

        # Make a point contraint between top transformation group and inputs locator, for get top group in the average position
        cmds.pointConstraint(obja, objc, tgroup_objb, mo=False)

        # Define generic curve
        curve=cmds.curve(d=1, p=[(0,0,0),(0,5,0),(0,10,0)], k=[0, 1, 2], n=crv_name)
        cmds.setAttr(curve+'.overrideEnabled',1)
        cmds.setAttr(curve+'.overrideColor', 13)
        cmds.setAttr(curve+'.dispCV', True)

        # Making connection in worldSpace using decomposeMatrix
        dMa= KstRig.create_maya_node('decomposeMatrix', name='_DMAT')
        dMb= KstRig.create_maya_node('decomposeMatrix', name='_DMAT')
        dMc= KstRig.create_maya_node('decomposeMatrix', name='_DMAT')

        # Connect control worldMatrix to decomposeMatrix.inputMatrix
        KstMaya.node_op(obja+'.worldMatrix','>>', dMa+'.inputMatrix')
        KstMaya.node_op(dMa+'.outputTranslate','>>',curve+'.controlPoints[0]')
        KstMaya.node_op(objb+'.worldMatrix','>>', dMb+'.inputMatrix')
        KstMaya.node_op(dMb+'.outputTranslate','>>',curve+'.controlPoints[1]')
        KstMaya.node_op(objc+'.worldMatrix','>>', dMc+'.inputMatrix')
        KstMaya.node_op(dMc+'.outputTranslate','>>',curve+'.controlPoints[2]')

        # Rebuild curve from linear to degree 2
        cmds.rebuildCurve(curve, ch=False, rpo=True, rt=0, end=True, kcp=True, kep=False, d=2, tol=.01)
        return curve, tgroup_objb

    # Create n segment lines
    def create_guides_from_object_list(self, object_list, position_list_up, position_list_down, guide_name = ''):
        '''
        Desc:
        Make n guide lines with locator and curve with structure group[loc_0, loc_1, line]

        Parameter:
        n_guide = numbers of guide that will be created
        name = guides name sorted

        Return guides list
        '''

        # Define variable for guide list
        guide_list = []
        point_list = []
        group_list = []

        # Create guides based on objects input
        i = 0
        for obj in object_list:
            point_a = KstRig.create_maya_object('locator', 'up_'+guide_name+'_'+str(i+1).zfill(3)+'_LOC', position_list_up[i])
            point_b = KstRig.create_maya_object('locator', 'down_'+guide_name+'_'+str(i+1).zfill(3)+'_LOC', position_list_down[i])
            group = KstRig.create_maya_object('transform', guide_name+'_'+str(i+1).zfill(3)+'_GRP')

            curve = KstRig.create_line_from_2_obj(point_a, point_b, guide_name+'_'+str(i+1).zfill(3)+'_CRV')
            cmds.setAttr(KstMaya.get_shape_node(curve)+'.dispCV', True)
            obj_to_parent = [point_a, point_b, curve]
            for obj in obj_to_parent:
                cmds.parent(obj, group)

            # Append the guide to the list
            guide_list.append(curve)

            # Append the points to the list
            point_list.append(point_a)
            point_list.append(point_b)
            group_list.append(group)
            i=i+1

        # Return sorted guide list sorted
        guide_list.sort()
        return guide_list, point_list, group_list
