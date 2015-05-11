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

# Import kstMath
import kcode.kmath.KstMath as _KstMath_
reload(_KstMath_)
KstMath = _KstMath_.KstMath()

# Import KstMaya
import kcode.kcore.KstMaya as _KstMaya_
reload(_KstMaya_)
KstMaya = _KstMaya_.KstMaya()

# Import KstDraw
import kcode.kcore.KstDraw as _KstDraw_
reload(_KstDraw_)
KstDraw = _KstDraw_.KstDraw()

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

class KstRig(object):
    # Debug module name variable
    _debug = 'KstRig'

    # Variables for naming convention ToDo class for get naming from a project
    _suffix_curve = 'CRV'
    _suffix_joint = 'JNT'
    _suffix_control = 'CTL'
    _suffix_group = 'GRP'
    _suffix_locator = 'LOC'

    def __init__(self):
        # KstOut.debug(KstRig._debug, 'Kistie Rig module loaded...')
        pass

    # Create a line from 2 points
    def create_line_from_2_points(self, crv_name, pta, ptb):
        '''
        Desc:
        Make a line between 2 points

        Parameter:
        pta = first point
        ptb = second point

        Return: Curve name
        '''

        pt_a = om.MPoint(pta[0],pta[1],pta[2])
        pt_b = om.MPoint(ptb[0],ptb[1],ptb[2])

        curve = cmds.curve(d=1, p=[(pt_a.x, pt_a.y, pt_a.z), (pt_b.x, pt_b.y, pt_b.z)], k=[0, 1], n=crv_name+'_CRV')
        cmds.setAttr(curve+'.overrideEnabled',1)
        cmds.setAttr(curve+'.overrideColor', 13)
        return curve

    # Create line from points
    def create_line_from_points(self, crv_name, points_list):
        '''
        Desc:
        Make a line between n points

        Parameter:
        crv_name = curve name

        points_list = list of position in this format [(pn,pn,pn), ]

        Return: Curve name
        '''

        # Define a var for curve cmd
        curve = ''

        # Define var for position and cast float in MPoint
        pt_n = om.MPoint()
        points_array = []

        # Define a variable for send the cmds.curve command
        str_curve = "cmds.curve(d=1, p=["
        str_degree = "k=["
        i = 0
        for point in points_list:
            pt_n.x = point[0]
            pt_n.y = point[1]
            pt_n.z = point[2]

            if i < len(points_list)-1:
                str_curve += str('('+str(pt_n.x)+','+str(pt_n.y)+','+str(pt_n.z)+'), ')
                str_degree += str(i)+','
            else:
                str_curve += str('('+str(pt_n.x)+','+str(pt_n.y)+','+str(pt_n.z)+')')
                str_degree += str(i)

            i += 1

        str_curve += str('], ')
        str_degree += str('], ')

        # Make the command that will be execute with exec function
        crv_cmd = 'curve='+str_curve+str_degree+"n='%s')" % (crv_name+'_CRV') # Make var curve on the fly
        KstOut.debug(KstRig._debug, crv_cmd)
        exec crv_cmd
        cmds.setAttr(curve+'.overrideEnabled',1) # Var curve seems not define, but it's in line 114 with a string var
        cmds.setAttr(curve+'.overrideColor', 13)
        return curve

    # Create a line from 2 objects
    def create_line_from_2_obj(self, obja, objb, crv_name='_curve_CRV'):
        '''
        Desc:
        Make a line between 2 objects

        Parameter:
        crv_name = name of curve
        pta = first object
        ptb = second object

        Return: Curve name
        '''

        # Define generic curve
        curve=cmds.curve(d=1, p=[(0,0,0),(0,0,0)], k=[0,1], n=crv_name)
        cmds.setAttr(curve+'.overrideEnabled',1)
        cmds.setAttr(curve+'.overrideColor', 13)

        # Making connection in worldSpace using decomposeMatrix
        dMa=cmds.createNode('decomposeMatrix', n='_DMAT')
        dMb=cmds.createNode('decomposeMatrix', n='_DMAT')

        # Connect control worldMatrix to decomposeMatrix.inputMatrix
        KstMaya.node_op(obja+'.worldMatrix','>>', dMa+'.inputMatrix')
        KstMaya.node_op(dMa+'.outputTranslate','>>',curve+'.controlPoints[0]')
        KstMaya.node_op(objb+'.worldMatrix','>>', dMb+'.inputMatrix')
        KstMaya.node_op(dMb+'.outputTranslate','>>',curve+'.controlPoints[1]')
        return curve

    # Create line from objects
    def create_line_from_objects(self, crv_name, objects_list):
        '''
        Desc:
        Make a line between n objects

        Parameter:
        crv_name = curve name

        objects_list = list of objects

        Return: Curve name
        '''

        # Check if object_list is valid
        if(objects_list):
            # Define var for position and cast float in MPoint
            pt_n = om.MPoint()
            points_array = []

            # Define a generic curve
            str_curve = "cmds.curve(d=1, p=["
            str_degree = "k=["
            i = 0
            for obj in objects_list:
                if i < len(objects_list)-1:
                    str_curve += str("(0, 0, 0), ")
                    str_degree += str(i)+','
                else:
                    str_curve += str("(0, 0, 0)")
                    str_degree += str(i)

                i += 1

            str_curve += str('], ')
            str_degree += str('], ')

            # Make the command that will be execute with exec function
            crv_cmd = 'curve='+str_curve+str_degree+"n='%s')" % (crv_name+'_CRV') # Make var curve on the fly
            KstOut.debug(KstRig._debug, crv_cmd)
            exec crv_cmd
            curve_shape = KstMaya.get_shape_node(curve)
            cmds.setAttr(curve+'.overrideEnabled',1) # Var curve seems not define, but it's in line 114 with a string var
            cmds.setAttr(curve+'.overrideColor', 13)

            # Make connection between CV[n] and decomposed position
            j = 0
            for obj in objects_list:
                # Making connection in worldSpace using decomposeMatrix
                d_matrix = self.create_maya_node('decomposeMatrix', node_name=('d_matrix_'+str(j)))

                # Connect control worldMatrix to decomposeMatrix.inputMatrix
                KstMaya.node_op('%s.worldMatrix' % obj, '>>', '%s.inputMatrix' % d_matrix)
                KstMaya.node_op('%s.outputTranslate' % d_matrix, '>>', '%s.controlPoints[%s]' % (curve_shape, j))
                j += 1
            return curve
        else:
            KstOut.debug(KstRig._debug, 'Check if object list is valid!')
            KstOut.error(KstRig._debug, 'Check if object list is valid!')
            return None

    """
    # Divide line with a locator in the middle ToDo: Fix does not work !!!
    def divide_curve_with(self, curve, obj_type, ndiv):
        '''
        Desc:
        Divide a line with a object default "locator"

        Parameter:
        curve = str name of curve to divide
        obj_type = str of object type
        ndiv = int division numbers

        Return: NULL
        '''
        curve_shape = KstMaya.get_shape_node(curve)
        curveInfo = cmds.createNode('curveInfo')
        KstMaya.node_op(curve_shape+'.worldSpace[0]', '>>', curveInfo+'.inputCurve')
        curve_len = cmds.getAttr(curveInfo+'.arcLength')
        print('Curve Len: ', curve_len)
        seg_len = curve_len/ndiv
        print('Seg Len: ', seg_len)
        norm_seg_len = float(float(1)/float(ndiv)) # normalized = (x-min(x))/(max(x)-min(x))
        print('Normalized Seg Len: ', norm_seg_len)
        step = 0
        norm_step = 0.0

        for i in xrange(0,(ndiv-1)):
            print(i)
            if obj_type == 'locator':
                loc = cmds.spaceLocator(n='segment_'+str(i)+'_LOCA')
                locShape = KstMaya.get_shape_node(loc)
                transform = loc[0]
                cmds.setAttr(locShape+'.localScaleX', 50)
                cmds.setAttr(locShape+'.localScaleY', 50)
                cmds.setAttr(locShape+'.localScaleZ', 50)
                POCI = cmds.createNode('pointOnCurveInfo', n='locatorPointCurveInfo_'+str(i)+'_POCI')
                KstMaya.node_op(curve_shape+'.worldSpace[0]', '>>', POCI+'.inputCurve')
                KstMaya.node_op(POCI+'.position', '>>', transform+'.translate')
                cmds.setAttr(POCI+'.parameter', norm_step)
                step += seg_len
                print('STEP: ', step)
                norm_step = float(float(1)/float(step))
                print('NORM STEP', norm_step)
    """

    # Create control for this object
    def create_anim_control(self, control_name, control_type='sphere', pos=[0, 0, 0], vector=[0, 1, 0], size=1, transform_on_top = False, color=1):
        '''
        Desc:
        Create animation control at position pos

        Parameter:
        control_name = control name
        control_type = control type str ['circle','cross','arrow']
        pos = control position in worldSpace
        vector = control vector direction ex: 0,1,0 the control will be on XZ plane\

        return control
        ToDo: Change with custom locator
        '''

        # Define empty var for ctl
        animCtl = ''

        # Draw a curve sphere
        if control_type == 'sphere':
            animCtl = cmds.curve(d=1, n=control_name+'_MANIP', p=[(0.0, 0.0, 1), (0.0, 0.5, 0.866025), (0.0 ,0.866025, 0.5),(0.0, 1, 0.0),(0.0, 0.866025, -0.5), (0.0, 0.5, -0.866025), (0.0, 0.0, -1), (0.0, -0.5, -0.866025), (0.0, -0.866025, -0.5), (0.0, -1,0.0), (0.0, -0.866025, 0.5), (0.0, -0.5, 0.866025), (0.0, 0.0, 1), (0.707107, 0.0, 0.707107), (1, 0.0, 0.0), (0.707107, 0.0, -0.707107), (0.0, 0.0, -1), (-0.707107, 0.0, -0.707107), (-1, 0.0, 0.0), (-0.866025, 0.5, 0.0), (-0.5, 0.866025, 0.0), (0.0, 1, 0.0), (0.5, 0.866025, 0.0), (0.866025, 0.5, 0.0), (1, 0.0, 0.0), (0.866025, -0.5, 0.0), (0.5, -0.866025, 0.0), (0.0, -1, 0.0), (-0.5, -0.866025, 0.0), (-0.866025, -0.5, 0.0), (-1, 0.0, 0.0), (-0.707107, 0.0, 0.707107), (0.0, 0.0, 1)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
            cmds.makeIdentity(apply=True, t=1, r=1, s=1)
            cmds.setAttr(animCtl+'.overrideEnabled',1)
            cmds.setAttr(animCtl+'.overrideColor',color)

        elif control_type == 'circle':
            animCtl = cmds.circle(n = control_name+'_CTL', c=pos, nr = vector)
            cmds.makeIdentity(apply=True, t=1, r=1, s=1)
            cmds.setAttr(animCtl[0]+'.overrideEnabled',1)
            cmds.setAttr(animCtl[0]+'.overrideColor',color)

        if (transform_on_top):
            animGrp = cmds.group(em=True, n=control_name+'_TGRP') # Change for pipeline also for _CTRL
            cmds.parent(animCtl[0], animGrp)
            cmds.xform(animGrp, t=pos, s=[size, size, size], ws=True)
            return [animGrp, animCtl]
        else:
            cmds.xform(animCtl, t=pos, s=[size, size, size], ws=True)
            return animCtl

    # Create locator in fastest way
    def create_maya_object(self, obj_type, obj_name='_LOCA', pos = (0, 0, 0), parent=None):
        '''
        Desc:
        Create every maya object

        Parameter:
        obj_type = maya object
        name = maya object name
        pos = control position in worldSpace

        return maya object
        '''
        maya_obj = cmds.createNode(str(obj_type))
        maya_obj = KstMaya.get_transform_node(maya_obj)
        maya_obj = cmds.rename(maya_obj, obj_name)

        # Set the position to the defined transform
        cmds.setAttr(maya_obj+'.translateX', pos[0])
        cmds.setAttr(maya_obj+'.translateY', pos[1])
        cmds.setAttr(maya_obj+'.translateZ', pos[2])

        if parent:
            cmds.parent(maya_obj, parent)
        return maya_obj

    # Create every node in fastest way
    def create_maya_node(self, node_type, node_name='_node'):
        '''
        Desc:
        Create every maya node

        Parameter:
        node_type = maya node
        name = maya object name
        pos = control position in worldSpace

        return maya object
        '''
        node = cmds.createNode(str(node_type))
        transform = KstMaya.get_transform_node(node)
        if cmds.nodeType(node)=='locator':
            maya_node = cmds.rename(transform, node_name)
        else:
            maya_node = cmds.rename(node, node_name)
        return maya_node

    # Create joint with special features
    @staticmethod
    def create_joint(jnt_name=None, pos=(0, 0, 0), orient_joint= 'xyz', up_axis_joint='yup', show_axis=True, radius=0.5):
        '''
        Desc:
        Create special joint

        Parameter:
        name = jont name
        pos = joint position
        showAxis = if True, show joint local axis
        radius = joint display radius
        '''
        joint = cmds.joint(p=pos, n=jnt_name)
        cmds.setAttr(joint+'.radius', radius)
        if show_axis:
            cmds.setAttr(joint+'.displayLocalAxis',1)
        return joint

    # Create a joint chain
    @staticmethod
    def create_joint_chain(chain_name, points_list, orient_chain='xyz', up_axis_chain='yup', show_axis=True, radius=0.5, reverse=False):
        '''
        Desc:
        Create oriented chain

        Parameter:
        chain_name = joint chain name
        points_list = point position list for each joint
        orient_chain = orient axis (aim, up)for all chain
        up_axis_change = up axis, default 'yup', but with Puppet Soul will be 'zup'
        showAxis = if True, show joint chain local axis
        radius = joint chain display radius

        Return joint chain
        '''
        #print('----------------------------- DEBUG CHAIN ---------------------------------')
        i = 0
        j = 0

        if reverse:
            points_list = sorted(points_list, reverse=True)

        position_list = KstMaya.get_position_list_from_objs(points_list)
        joint_list = []

        for pos in position_list:
            if i==0:
                cmds.select(cl=True)
            else:
                cmds.select(joint_list[i-1])

            if i == len(position_list)-1:
                suffix = '_endJnt'
            else:
                suffix = '_JNT'
            #jnt = KstRig.create_joint(chain_name+suffix, pos, show_axis=show_axis, radius=radius)
            jnt = KstRig.create_joint('%s_%s%s' % (chain_name, str(j+1).zfill(3), suffix), pos, show_axis=show_axis, radius=radius)
            cmds.setAttr(jnt+'.overrideEnabled',1)
            cmds.setAttr(jnt+'.overrideColor', 17)
            joint_list.append(jnt)
            i=i+1
            j=j+1

        # Orient the entire chain with specified orientation
        for j in range(0, len(joint_list)):
            KstOut.debug(KstRig._debug, 'Reorient current joint:' )
            KstOut.debug(KstRig._debug, 'joint: %s' % jnt)
            #print ''
            try:
                cmds.joint(joint_list[j], e=True, zso=True, oj=orient_chain, sao=up_axis_chain, ch=True)
            except:
                print('Error on reorient, check the rotations')

            # If it's the last joint reset rotation axis
            if j >= len(joint_list)-1:
                rot_axis = ['X','Y','Z']
                for axis in rot_axis:
                    cmds.setAttr(joint_list[j]+'.jointOrient'+axis, 0)

        return joint_list

    @staticmethod
    def create_ik(jnt_start, jnt_end, type = 'RPS', up_vec = [0,1,0], name = '_IKH'):
        solver = None
        if type == 'RPS':
            solver = 'ikRPsolver'
        elif type == 'SCS':
            solver = 'ikSCsolver'
        elif type == 'SS':
            solver = 'ikSplineSolver'
        ikh = cmds.ikHandle(name = name, sj = jnt_start, ee = jnt_end, solver = solver)
        return ikh

    # Modify existing orientation of the current chain
    @staticmethod
    def modifiy_joint_chain_axis(joint_chain, orient_chain='xyz', up_axis_chain='yup'):
        for i in range(0, len(joint_chain)):
            KstOut.debug(KstRig._debug, 'Reorient current joint:' )
            KstOut.debug(KstRig._debug, 'joint: %s' % joint_chain[i])
            try:
                cmds.joint(joint_chain[i], e=True, zso=True, oj=orient_chain, sao=up_axis_chain, ch=True)
            except:
                print('Error on reorient, check the rotations')

            # If it's the last joint reset rotation axis
            if i == len(joint_chain)-1:
                rot_axis = ['X','Y','Z']
                for axis in rot_axis:
                    cmds.setAttr(joint_chain[i]+'.jointOrient'+axis, 0)

    """
    # Create mirror rig
    def create_mirror_rig(self, sel, axis='x'):
        '''
        Desc:
        Make a mirror rig using multiplyDivide node

        Parameter:
        sel = selection
        axis = current axis default 'X' or 'x'
        '''
        otherPart = ''
        # Make generic
        if '_GRUP' in sel:
            # Check the part if is L
            if '_L_' in sel:
                new_name=str(sel).replace('_L_','_R_')

            # Check the part if is R
            if '_R_' in sel:
                new_name=str(sel).replace('_R_','_L_')

            otherPart = new_name
            mdv_node = cmds.createNode('multiplyDivide', n=sel+'_MDV')
            attr_list_base=['1X','1Y','1Z']
            attr_list_mirror=['2X','2Y','2Z']
            for attr in attr_list_mirror:
                cmds.setAttr(mdv_node+'.input'+attr, 1)
                if axis == 'x' or 'X':
                    cmds.setAttr(mdv_node+'.input2X', -1)

                elif axis == 'y' or 'Y':
                    cmds.setAttr(mdv_node+'.input2Y', -1)

                elif axis == 'z' or 'Z':
                    cmds.setAttr(mdv_node+'.input2Z', -1)

                else:
                    print('You must define an axis for mirror')

                # Making all connections
                KstMaya.node_op(mdv_node+'.input1X', '<<', sel+'.tx')
                KstMaya.node_op(mdv_node+'.input1Y', '<<', sel+'.ty')
                KstMaya.node_op(mdv_node+'.input1Z', '<<', sel+'.tz')
                KstMaya.node_op(mdv_node+'.outputX', '>>', new_name+'.tx')
                KstMaya.node_op(mdv_node+'.outputY', '>>', new_name+'.ty')
                KstMaya.node_op(mdv_node+'.outputZ', '>>', new_name+'.tz')

            # Set the operation on MULTIPLY
            cmds.setAttr(mdv_node+'.operation', 1)
        else:
            KstOut.debug(KstRig._debug, 'Wrong type, please double check!')

    # Get closest vertex from an object
    def get_closest_vertex(self, msh, obj, distance):
        '''
        Description: return the list of closest vertices
        msh = mesh selection
        dist = threshold distance for vertex neighbour
        jnt = list of joints
        jntName = name of joint

        return vertex list in selected distance
        '''
        vtx_list = []
        obj_pos = cmds.xform(obj, q=True, ws=True, t=True)
        vtxs = cmds.polyEvaluate(msh, v=True)
        closestPoints = []
        for i in xrange(0, vtxs):
            vtx = (msh+".vtx["+str(i)+"]")
            ppos = []
            ppos = cmds.xform((msh+".vtx["+str(i)+"]"), q = True, ws = True, t = True)
            newpos = [ppos[0] - obj_pos[0], ppos[1] - obj_pos[1], ppos[2] - obj_pos[2]]
            res = KstMath.get_mag(newpos)
            if (res <= distance):
                vtx_list.append(vtx)
        return vtx_list
    """

    # Attach object to a surface
    def attach_object_to_surface(self, srf, projection_point_obj, obj_to_attach='axis', stick_to_surface = True):
        '''
        Description: attach the projection point object (projection_point_obj) to the surface (srf)
        srf = surface
        obj_to_attach = object to attach to the surface

        return object_to_attach
        '''
        # Check if axis is defined by user or not
        if obj_to_attach=='axis':
            obj_to_attach = cmds.group(em=True, n='%s' % str(projection_point_obj)+'_AXIS')
        else:
            obj_to_attach = obj_to_attach

        # Check if all variables are valid
        if srf and projection_point_obj and obj_to_attach:

            # Create closestPointOnSurface Maya node
            cp_on_srf = self.create_maya_node('closestPointOnSurface', '%s_CPOS' % projection_point_obj)

            # Create decomposeMatrix Maya node
            d_matrix = self.create_maya_node('decomposeMatrix', '_DMAT')

            # Attach surface shape to closestSurface inputSurface
            srf_shape = KstMaya.get_shape_node(srf)
            KstMaya.node_op('%s.worldSpace[0]' % srf_shape, '>>' , '%s.inputSurface' % cp_on_srf)

            # Attach projection world matrix position to decompose matrix input
            KstMaya.node_op('%s.worldMatrix[0]' % projection_point_obj, '>>', '%s.inputMatrix' % d_matrix)

            # Connect decompose matrix in closestPoint input pos
            KstMaya.node_op('%s.outputTranslate' % d_matrix, '>>', '%s.inPosition' % cp_on_srf)

            # Set the position in output on axis or custom obj
            KstMaya.node_op('%s.result.position' % cp_on_srf, '>>', '%s.translate' % obj_to_attach)
            KstDraw.debug_axis(obj_to_attach)

            # Check if stick param is true
            if(stick_to_surface):
                # Create follicle Maya node
                follicle = self.create_maya_node('follicle', '%s_FOLL' % obj_to_attach)
                obj_to_delete = KstMaya.get_transform_node(follicle)

                try:
                    # Attach surface to follicle
                    KstMaya.node_op('%s.worldMatrix[0]' % srf_shape, '>>', '%s.inputWorldMatrix' % follicle)
                    KstMaya.node_op('%s.local' % srf_shape, '>>', '%s.inputSurface' % follicle)
                except:
                    KstOut.debug(KstRig._debug, 'SURFACE -> FOLLICLE')

                try:
                    # Attach closestPoint output to UV follicle position
                    KstMaya.node_op('%s.result.parameterU' % cp_on_srf, '>>', '%s.parameterU' % follicle)
                    KstMaya.node_op('%s.result.parameterV' % cp_on_srf, '>>', '%s.parameterV' % follicle)
                except:
                    KstOut.debug(KstRig._debug, 'CLOSEST -> FOLLICLE')

                try:
                    # Attach follicle output transformations to axis
                    KstMaya.node_op('%s.outTranslate' % follicle, '>>', '%s.translate' % obj_to_attach)
                    KstMaya.node_op('%s.outRotate' % follicle, '>>', '%s.rotate' % obj_to_attach)
                except:
                    KstOut.debug(KstRig._debug, 'FOLLICLE -> AXIS')

                # Delete closestPoint node
                cmds.delete(cp_on_srf)

                # Parent follicle shape to AXIS transform
                cmds.parent(follicle, obj_to_attach, s=True, r=True)

                # print ''
                # print ('OBJ TO ATTACH: ', obj_to_attach)
                # print ''

                # Delete the empty transform for the follicle
                cmds.delete(obj_to_delete)
            return obj_to_attach
        else:
            KstOut.debug(KstRig._debug, 'Check if inputs are valid')
            KstOut.error(KstRig._debug, 'Check if inputs are valid')

    # Attach object to a curve, ToDo add axis object
    def attach_object_to_curve(self, curve, projection_point_obj):
        '''
        Description: attach the projection point object (projection_point_obj) to the curve in input
        curve = curve
        obj_to_attach = object to attach to the curve

        return object_to_attach
        '''

        # Check if all variables are valid
        if curve and projection_point_obj:
            #print 'DEBUG curve: ', curve
            #print 'DEBUG projection_point_obj', projection_point_obj

            # Create closestPointOnSurface Maya node
            np_on_curve = self.create_maya_node('nearestPointOnCurve', '%s_NPOC' % projection_point_obj)

            # Create pointOnCurveInfo Maya node
            point_on_curve_info = self.create_maya_node('pointOnCurveInfo', '%s_POCI' % projection_point_obj)

            # Create decomposeMatrix Maya node
            d_matrix = self.create_maya_node('decomposeMatrix', '_DMAT')

            # Attach curve shape to nearestPointOnCurve inputCurve
            crv_shape = KstMaya.get_shape_node(curve)
            KstMaya.node_op('%s.worldSpace[0]' % crv_shape, '>>' , '%s.inputCurve' % np_on_curve)

            # Attach curve shape to pointOnCurveInfo
            KstMaya.node_op('%s.worldSpace[0]' % crv_shape, '>>' , '%s.inputCurve' % point_on_curve_info)

            # Attach projection world matrix position to decompose matrix input
            KstMaya.node_op('%s.worldMatrix[0]' % projection_point_obj, '>>', '%s.inputMatrix' % d_matrix)

            # Store decompose matrix data position
            pos = cmds.getAttr('%s.outputTranslate' % d_matrix)

            # Set stored transformation in nearestPointOnCurve inPosition
            cmds.setAttr('%s.inPositionX' % np_on_curve, pos[0][0])
            cmds.setAttr('%s.inPositionY' % np_on_curve, pos[0][1])
            cmds.setAttr('%s.inPositionZ' % np_on_curve, pos[0][2])

            # Store param nearestPointOnCurve data value
            param = cmds.getAttr('%s.parameter' % np_on_curve)

            # Set param to pointOnCurveInfo
            cmds.setAttr('%s.parameter' % point_on_curve_info, param)

            # Set the position in output on axis or custom obj
            KstMaya.node_op('%s.result.position' % point_on_curve_info, '>>', '%s.translate' % projection_point_obj)
            KstDraw.debug_axis(projection_point_obj)

            return projection_point_obj
        else:
            KstOut.debug(KstRig._debug, 'Check if inputs are valid')
            KstOut.error(KstRig._debug, 'Check if inputs are valid')

    # Create surface from n curves ToDo, add and fic the code if the output is mesh
    def create_surface_from_curves(self, curves_list, surface_degree = 'linear', surface_type = 'nurbs', normalize = True, surface_name=''):
        '''
        Description: create a surface (poly or nurbs) froma a curve list
        curve_list = curve list
        surface_degree = surface degree can be: "linear" or "cubic"
        surface_type = type of surface output can be: "mesh" or "nurbs"
        normalize = if True normalize the surface from 0 to 1, reccomended, default in fact is True

        return surface
        '''

        # Check if curve_list is valid
        if(curves_list):
            # Create and empty var for loft command
            loft_srf = ''

            # Define variables for loft based on inputs
            # degree
            if surface_degree == 'linear':
                srf_deg = 1

            elif surface_degree == 'cubic':
                srf_deg = 3

            # output surface
            if surface_type == 'mesh':
                srf_type = 1

            elif surface_type == 'nurbs':
                srf_type = 0

            # Build the command that will be execute
            str_loft = "loft_srf = cmds.loft("
            for crv in curves_list:
                str_loft += "'%s'," % crv
            str_loft += "ch=True, u=True, c=False, ar=True, d=%s, ss=True, rn=False, po=%s" % (srf_deg, srf_type)
            str_loft +=')'
            KstOut.debug(KstRig._debug, 'Command that will be executed:')
            #print(str_loft)
            #print ''

            # Execute the builded command
            try:
                exec(str_loft)
            except:
                KstOut.debug(KstRig._debug, 'Error on execute command !!!')
                pass

            loft_srf = cmds.rename(loft_srf[0], surface_name+'_SRF')

            if normalize:
                loft_srf = cmds.rebuildSurface(loft_srf, ch=True, rpo=True, rt=0, end=1, kr=0, kcp=True, kc=False, su=3, du=1, sv=1, dv=1, tol=0.01, fr=0, dir=2)

            return loft_srf
        else:
            KstOut.debug(KstRig._debug, 'Check if input are valid')
            KstOut.error(KstRig._debug, 'Check if input are valid')