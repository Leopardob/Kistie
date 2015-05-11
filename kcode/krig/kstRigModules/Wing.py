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

# Import Kistie
import Kistie.Kistie as _KstCore_
reload(_KstCore_)
KstCore = _KstCore_.KistieCore()

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

# Import KstMath
import kcode.kmath.KstMath as _KstMath_
reload(_KstMath_)
KstMath = _KstMath_.KstMath()

# Import KstRigModule.RTS_Rig
import kcode.krig.kstRigModules.RTS_Rig as _KstRigRts_
reload(_KstRigRts_)
KstRigRts = _KstRigRts_.RTS_Rig()

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

# Import KstOut
import kcode.kcore.KstDraw as _KstDraw_
reload(_KstDraw_)
KstDraw = _KstDraw_.KstDraw()

class Wing(object): # ToDo modify the skincluster influence( look file: Wings_redo_tmp_024_wingConstruction_endprototype.mb )
    # Debug module name variable
    '''
    Desc:
    This class contains all method used for build wings prototype, from user objects, to final rig
    '''

    _debug = 'Wing'

    def __init__(self, name, part):
        # Vars
        self._name = name
        self._part = part
        self._type = 'None'
        self._kname = self._name+'_'+self._part

        # Puppet soul vars
        self._mbr_name = '%s_%s_%s' % (self._type, self._name, self._part)
        self._ps_name = str(name).lower()+'_'+str(part).upper()
        #self._puppet_soul_attr_name = 'PUPuserChain' [0,2,3
        self._puppet_soul_all_chain_name = 'PUPuserChain'

        # The real hierarchy for joints
        self._puppet_soul_chain_list = str(KstAttrs.get_attr(self._ps_name, self._puppet_soul_all_chain_name)).split('/')

        # Kistie vars
        self._kst_attr_node_ = ''
        self._kst_attr_name_ = 'storageNode_KST'
        self._position_list_up = None
        self._position_list_down = None
        self._joint_list = None
        self._joint_interp_list = None
        self._joint_transform_list = None
        self._surfaces = None

        KstOut.debug(Wing._debug, 'Kistie Rig [module:WING] extension for RTS project loaded...')

    # Make guides
    def generate_guides(self, user_points=None):
        '''
        Desc:
        Generate guides wing

        Parameter:
        user point = if get a value, the guides down will be connected to the points defined by user

        Return: # ToDo check if we need all returns
        guide list sorted
        point list
        position list
        position list down
        '''

        # Variable for position list input storage
        user_position_list = []

        #KstOut.debug(Wing._debug, self._puppet_soul_name)
        #KstOut.debug(Wing._debug, self._puppet_soul_attr_name)

        # Varable for position list
        positions_list = []

        # The Puppet_Soul hierarchy object, it's quite complex, so instead query the world space position, i use a temp point constaint and after save object pos
        for jnt in self._puppet_soul_chain_list:
            if cmds.objExists(jnt):
                loc = KstRig.create_maya_node('transform', 'temp')
                KstMaya.make_constraint(jnt, loc, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')
                pos = cmds.xform(loc, q=True, t=True, ws=True)
                positions_list.append(pos)
                cmds.delete(loc)
            else:
                print('OBJECT DOES NOT EXISTS: ', jnt)

        # Create an object for storing info
        KstCore.create_kistie_node()

        # Extract world space position from Puppe Soul chain
        positions_list_down = []

        # If method has input then retrieve object input position
        if user_points:
            user_position_list = KstMaya.get_position_list_from_objs(user_points)

        # Make two list one for up_point and one for down_point, with an offset
        i=0
        for pos in positions_list:
            pos_up = KstMath.vec_from_point(pos)

            # If input position comes from user
            if user_points:
                pos_temp = om.MVector(user_position_list[i][0], user_position_list[i][1], user_position_list[i][2])
            else:
                pos_temp = pos_up+om.MVector(0, -10, 0)
            positions_list_down.append([pos_temp.x, pos_temp.y, pos_temp.z])
            i=i+1

        # Generate lines from Puppet Soul chain
        guides_list = KstRigRts.create_guides_from_object_list(self._puppet_soul_chain_list, positions_list, positions_list_down, guide_name=self._kname)

        # Store guides data in the KST node
        KstCore.write_info_to_node('guideList', guides_list[0])

        # Store objects data in the KST node
        KstCore.write_info_to_node('objectList', guides_list[1])

        return [guides_list[0], guides_list[1], positions_list, positions_list_down]

    # <editor-fold desc="generate_guides:CODE THAT WORKS IN MY PROTOTYPE">
    """
    # Make guides
    def generate_guides(self, user_points=None):
        '''
        Desc:
        Generate guides wing

        Parameter:
        user point = if get a value, the guides down will be connected to the points defined by user

        Return: # ToDo check if we need all returns
        guide list sorted
        point list
        position list
        position list down
        '''

        # Variable for position list input storage
        user_position_list = []

        KstOut.debug(Wing._debug, self._puppet_soul_name)
        KstOut.debug(Wing._debug, self._puppet_soul_attr_name)

        # Create an object for storing info
        KstCore.create_kistie_node()

        # Extract world space position from Puppe Soul chain
        positions_list= KstMaya.get_position_list_from_objs(self._puppet_soul_chain_list)
        positions_list_down = []

        if user_points:
            user_position_list = KstMaya.get_position_list_from_objs(user_points)

        # Make two list one for up_point and one for down_point, with an offset
        i=0
        for pos in positions_list:
            pos_up = KstMath.vec_from_point(pos)

            # If input position comes from user
            if user_points:
                pos_temp = om.MVector(user_position_list[i][0], user_position_list[i][1], user_position_list[i][2])
            else:
                pos_temp = pos_up+om.MVector(0, -10, 0)
            positions_list_down.append([pos_temp.x, pos_temp.y, pos_temp.z])
            i=i+1

        # Generate lines from Puppet Soul chain
        guides_list = KstRigRts.create_guides_from_object_list(self._puppet_soul_chain_list, positions_list, positions_list_down, guide_name=self._kname)

        # Store guides data in the KST node
        KstCore.write_info_to_node('guideList', guides_list[0])

        # Store objects data in the KST node
        KstCore.write_info_to_node('objectList', guides_list[1])

        return [guides_list[0], guides_list[1], positions_list, positions_list_down]
    """
    # </editor-fold>

    # Make surface from guides
    def generate_surface(self, guides_list=None, object_list=None, from_node=False):
        '''
        Desc:
        Generate surface wing, (interpolation surface and curved surface), ToDo: optimize numbers of surfaces

        Parameter:
        guide_list = the list of guides (lines)
        object_list = the list of the objects that generate the guides #optimize, i can get the position from the CV in world space
        from_node = if False, read data from input method, and not from Kistie node attribute

        Return the generated surface, and the guide list
        '''

        # Define a list for surfaces
        surfaces = []

        # Define an empty list for put follicles
        follicle_list = []
        joint_up_list = []

        # Check if data needs get from the KST node
        if from_node:
            guides_list = KstCore.read_info_from_node('guideList')
            object_list = KstCore.read_info_from_node('objectList')

        # Generate surface from input guides list
        # *IMPORTANT: by default the normalization is set to True, otherwise closestPontOnSurface is not calculated properly
        surface = KstRig.create_surface_from_curves(guides_list, surface_name='interp_'+self._kname)
        surfaces.append(surface[0])

        # Store surface params for rebuild
        surface_shape = KstMaya.get_shape_node(surface)

        # Store span UV
        su = cmds.getAttr(surface_shape+'.su')
        sv = cmds.getAttr(surface_shape+'.sv')

        # Build the skincluster and using Puppet Soul user joints as skin object
        # ToDo: Make a class for skinCluster in KstRig

        # Make a copy of global variable self._puppet_soul_chain_list and insert scapula or NOT ?!?
        #cp_puppet_soul_chain_list.insert(0, ('scapula'+'_'+self._part))

        # Ask to Cedric about real skin objects
        # Make skincluster
        skin_cluster = cmds.skinCluster(self._puppet_soul_chain_list, surface, sm=0, nw=1, tsb=True)

        # Make automatic skinning for the Wing surface order joint ['shoulder_L', 'elbow_L', 'wrist_L', 'hand2_L']
        # Shoulder
        cmds.skinPercent(skin_cluster[0], surface[0]+'.cv[0][1]', tv=[(self._puppet_soul_chain_list[0], 1), (self._puppet_soul_chain_list[1], 0.0), (self._puppet_soul_chain_list[2], 0.0), (self._puppet_soul_chain_list[3], 0.0)])

        # Elbow
        cmds.skinPercent(skin_cluster[0], surface[0]+'.cv[1][1]', tv=[(self._puppet_soul_chain_list[0], 0.5), (self._puppet_soul_chain_list[1], 0.4),(self._puppet_soul_chain_list[2], 0.05), (self._puppet_soul_chain_list[3], 0.05)])

        # Wrist
        cmds.skinPercent(skin_cluster[0], surface[0]+'.cv[2][1]', tv=[(self._puppet_soul_chain_list[0], 0.150), (self._puppet_soul_chain_list[1], 0.250), (self._puppet_soul_chain_list[2], 0.3), (self._puppet_soul_chain_list[3], 0.3)])

        # Hand
        cmds.skinPercent(skin_cluster[0], surface[0]+'.cv[3][1]', tv=[(self._puppet_soul_chain_list[0], 0.0), (self._puppet_soul_chain_list[1], 0.0), (self._puppet_soul_chain_list[2], 0.0), (self._puppet_soul_chain_list[3], 1)])

        # Rebuild the linear surface and make a copy of the original
        surface = cmds.rebuildSurface(surface, ch=True, replaceOriginal = True, rt = 0, su=su, sv = sv, du=3, dv=3, n=surface[0])

        # Make vars for separate object that will be on curve surface and object that will be on linear

        # All up objects will stay on linear surface
        up_objects = []

        # All down objects will stay on curve surface
        down_objects = []

        # Storage var for follicle_list
        follicle_list = []

        # Filters object and fill lists
        for obj in object_list:
            '''
            if 'up_' in obj:
                up_fol= KstRig.attach_object_to_surface(surface_linear, obj)
                follicle_list.append(up_fol)
            '''

            if 'down_' in obj:
                down_fol = KstRig.attach_object_to_surface(surface, obj)
                follicle_list.append(down_fol)

        # Store transform joint data in the KST node
        KstCore.write_info_to_node('follicleList', follicle_list)

        # Fill the member var with surfaces
        self._surfaces = surfaces

        return follicle_list

    # <editor-fold desc="generate_surface:CODE THAT WORKS IN MY PROTOTYPE">
    """
    # Make surface from guides
    def generate_surface(self, guides_list=None, object_list=None, from_node=False):
        '''
        Desc:
        Generate surface wing, (interpolation surface and curved surface), ToDo: optimize numbers of surfaces

        Parameter:
        guide_list = the list of guides (lines)
        object_list = the list of the objects that generate the guides #optimize, i can get the position from the CV in world space
        from_node = if False, read data from input method, and not from Kistie node attribute

        Return the generated surface, and the guide list
        '''

        # Define a list for surfaces
        surfaces = []

        # Define an empty list for put follicles
        follicle_list = []
        joint_up_list = []

        # Check if data needs get from the KST node
        if from_node:
            guides_list = KstCore.read_info_from_node('guideList')
            object_list = KstCore.read_info_from_node('objectList')

        # Generate surface from input guides list
        # *IMPORTANT: by default the normalization is set to True, otherwise closestPontOnSurface is not calculated properly
        surface_linear = KstRig.create_surface_from_curves(guides_list, surface_name='interp_'+self._kname)
        surfaces.append(surface_linear[0])

        # Store surface params for rebuild
        surface_shape = KstMaya.get_shape_node(surface_linear)

        # Store span UV
        su = cmds.getAttr(surface_shape+'.su')
        sv = cmds.getAttr(surface_shape+'.sv')

        # Build the skincluster and using Puppet Soul user joints as skin object
        # ToDo: Make a class for skinCluster in KstRig

        # Make a copy of global variable self._puppet_soul_chain_list and insert scapula
        cp_puppet_soul_chain_list = list(self._puppet_soul_chain_list)
        cp_puppet_soul_chain_list.insert(0, ('scapula'+'_'+self._part))

        # Ask to Cedric about real skin objects
        # Make skincluster
        skin_cluster = cmds.skinCluster(cp_puppet_soul_chain_list, surface_linear, sm=0, nw=1, tsb=True)

        # Make automatic skinning for the Wing surface order joint ['scapula_L', 'shoulder_L', 'elbow_L', 'wrist_L', 'hand2_L']
        # Shoulder
        cmds.skinPercent(skin_cluster[0], surface_linear[0]+'.cv[0][1]', tv=[(cp_puppet_soul_chain_list[0],.5), (cp_puppet_soul_chain_list[1],0.5),(cp_puppet_soul_chain_list[2],0.0),(cp_puppet_soul_chain_list[3],0.0), (cp_puppet_soul_chain_list[4],0.0)])

        # Elbow
        cmds.skinPercent(skin_cluster[0], surface_linear[0]+'.cv[1][1]', tv=[(cp_puppet_soul_chain_list[0],0), (cp_puppet_soul_chain_list[1],0.5),(cp_puppet_soul_chain_list[2],0.5),(cp_puppet_soul_chain_list[3],0.0), (cp_puppet_soul_chain_list[4],0.0)])

        # Wrist
        cmds.skinPercent(skin_cluster[0], surface_linear[0]+'.cv[2][1]', tv=[(cp_puppet_soul_chain_list[0],.25), (cp_puppet_soul_chain_list[1],0.25),(cp_puppet_soul_chain_list[2],0.25),(cp_puppet_soul_chain_list[3],0.25), (cp_puppet_soul_chain_list[4],0.0)])

        # Hand
        cmds.skinPercent(skin_cluster[0], surface_linear[0]+'.cv[3][1]', tv=[(cp_puppet_soul_chain_list[0],.0), (cp_puppet_soul_chain_list[1],0.0),(cp_puppet_soul_chain_list[2],0.0),(cp_puppet_soul_chain_list[3],.5), (cp_puppet_soul_chain_list[4],0.5)])

        # Rebuild the linear surface and make a copy of the original
        surface_curve = cmds.rebuildSurface(surface_linear, ch=True, replaceOriginal = False, rt = 0, su=su, sv = sv, du=3, dv=3, n=surface_linear[0].replace('interp','interpreb'))
        surfaces.append(surface_curve[0])

        # Make vars for separate object that will be on curve surface and object that will be on linear

        # All up objects will stay on linear surface
        up_objects = []

        # All down objects will stay on curve surface
        down_objects = []

        # Storage var for follicle_list
        follicle_list = []

        # Filters object and fill lists
        for obj in object_list:
            if 'up_' in obj:
                up_fol= KstRig.attach_object_to_surface(surface_linear, obj)
                follicle_list.append(up_fol)

            if 'down_' in obj:
                down_fol = KstRig.attach_object_to_surface(surface_curve, obj)
                follicle_list.append(down_fol)

        # Store transform joint data in the KST node
        KstCore.write_info_to_node('follicleList', follicle_list)

        # Fill the member var with surfaces
        self._surfaces = surfaces

        return follicle_list
    """
    # </editor-fold>

    # Make joint on surface
    def generate_joints_on_surface(self, follicle_list=None, radius=1.0, from_node=False):
        '''
        Desc:
        Generate joint on surface wing

        Parameter:
        follicle_list = list of follicles

        Return a list with generated joints
        '''

        # Make an empty list for store joints
        joint_list = ['shoulderDir_L_JNT_1', 'elbowDir_L_JNT_1', 'wristDir_L_JNT_1', 'armEndDir_L_JNT_1']

        # Check if data needs get from the KST node
        if from_node:
            follicle_list = KstCore.read_info_from_node('follicleList')

        i=0
        for i in range(0, len(joint_list)):
            #print('DEBUG current joint: ', joint_list[i], follicle_list[i])

            # Current joint
            jnt = joint_list[i]
            his_parent = cmds.listRelatives(jnt, p=True)
            print('DEBUG current_joint: ', jnt)
            print('DEBUG parent: ', his_parent)

            # Current parent for the NEW OBJECT THAT WILL BE PARENTED TO THE CHAIN
            obj_to_parent = KstRig.create_maya_node('transform', jnt.replace('JNT', 'PGRP'))
            KstMaya.make_constraint(his_parent, obj_to_parent, constraint_type='parent', maintain_offset=False, keep_constraint_node=True, name='temp_name')

            # Create the transform grp that will be driven by constraint
            trs = KstRig.create_maya_node('transform', jnt.replace('JNT', 'TGRP'))
            KstMaya.make_constraint(jnt, trs, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')

            # Parent transform to parent group
            cmds.parent(trs, obj_to_parent)

            # Change the joint parent to the new parent
            cmds.parent(jnt, trs)

            # Make the object upVector
            up_vec = KstRig.create_maya_node('locator', obj_to_parent.replace('_PGRP','_UPVEC'))
            print('DEBUG up_vec: ', trs)
            print''

            # Parent upVec to transform
            cmds.parent(up_vec, obj_to_parent)

            # Reset position and size to up_vec
            t_channels = ('tx', 'ty', 'tz')
            r_channels = ('rx', 'ry', 'rz')
            s_channels = ('sx', 'sy', 'sz')

            k = 0
            for chn in t_channels:
                cmds.setAttr(up_vec+'.'+chn, 0)
                cmds.setAttr(up_vec+'.'+r_channels[k], 0)
                cmds.setAttr(up_vec+'.'+s_channels[k], .2)
                k=k+1

            # Move the up_vec in the right position for a good aim
            cmds.xform(up_vec, t=[0, 3, 0])

            # Var for aim vec, in this version is directly the current follicle
            aim_vec = follicle_list[i]

            # Make aim constraint
            # NOTE* IT'S VALID IF THE WING IT'S ON Y/X PLANE AXIS

            aim_name = str(jnt).replace('_JNT','')

            # Make the aim constraint
            aim = KstMaya.make_constraint(aim_vec, trs, constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)

            # Put the genrated joint in the list
            joint_list.append(jnt)
            i=i+1


        # Fix the orient constraint, rough mode, ToDo fix
        #obj_to_fix = 'elbowDir_mid_L_JNT_1'
        #cmds.delete('elbowDir_mid_L_JNT_1_orientConstraint1')
        #pta = 'elbowDir_L_TGRP_1'
        #ptb = 'wristDir_L_TGRP_1'
        #cmds.orientConstraint(pta, ptb, obj_to_fix, mo=True)

        # Store transform joint data in the KST node
        KstCore.write_info_to_node('jointList', joint_list)

        # Store the list in the global var
        self._joint_list = joint_list

        return joint_list

    # <editor-fold desc="generate_joints_on_surface: CODE THAT WORKS IN MY PROTOTYPE">
    """
    # Make joint on surface
    def generate_joints_on_surface(self, follicle_list=None, radius=1.0, from_node=False):
        '''
        Desc:
        Generate joint on surface wing

        Parameter:
        follicle_list = list of follicles

        Return a list with generated joints
        '''

        # Make an empty list for store joints
        joint_list = []

        # Check if data needs get from the KST node
        if from_node:
            follicle_list = KstCore.read_info_from_node('follicleList')

        # Chunks string
        import string
        chunks_list = list(string.ascii_lowercase)

        # Split the object list by 2, that's perfect for create joint procedure
        nsplit = 2
        object_list_by_two = [follicle_list[x:x+nsplit] for x in xrange(0, len(follicle_list), 2)]
        chunks_list_by_two = [follicle_list[x:x+nsplit] for x in xrange(0, len(follicle_list), 2)]

        i = 0
        # For each couple joint couple, make the chain
        for chunk in object_list_by_two:

            # Define the object where will be parented the chain joint
            obj_to_parent = chunk[0]

            newname = chunk[0].replace(self._part+'_', '&')
            newname = newname.split('&', -1)[0]+self._part

            # Make the joint
            jnt = KstRig.create_joint_chain(newname+'_'+str(i+1).zfill(3), chunk, radius = radius)

            if 'up_' in obj_to_parent:
                # Make the object upVector
                up_vec = KstRig.create_maya_node('locator', obj_to_parent.replace('_TGRP','_UPVEC'))

                # Parent upVec to transform
                cmds.parent(up_vec, obj_to_parent)

                # Reset position and size to up_vec
                t_channels = ('tx', 'ty', 'tz')
                r_channels = ('rx', 'ry', 'rz')
                s_channels = ('sx', 'sy', 'sz')

                k = 0
                for chn in t_channels:
                    cmds.setAttr(up_vec+'.'+chn, 0)
                    cmds.setAttr(up_vec+'.'+r_channels[k], 0)
                    cmds.setAttr(up_vec+'.'+s_channels[k], .2)
                    k=k+1

                # Move the up_vec in the right position for a good aim
                cmds.xform(up_vec, t=[0, 0, 3])

                # Var for aim vec
                aim_vec = obj_to_parent.replace('up','down')

                # Make aim constraint
                # NOTE* IT'S VALID IF THE WING IT'S ON Y/X PLANE AXIS

                aim_name = str(jnt[0]).replace('_JNT','')

                # Add a transformation group
                trs = KstRig.create_maya_node('transform', node_name=newname+'_'+str(i+1).zfill(3)+'_TGRP')
                KstDraw.debug_axis(trs)

                # Parent transform to follicle
                cmds.parent(trs, obj_to_parent)

                # Put axis on up chain
                KstMaya.make_constraint(jnt[0], trs, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')

                # Make the aim constraint
                #aim = KstMaya.make_constraint(aim_vec, jnt[0], constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)
                aim = KstMaya.make_constraint(aim_vec, trs, constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)

            # Parent joint to trs
            cmds.parent(jnt[0], trs)

            # Put the genrated joint in the list
            joint_list.append(jnt)
            i=i+1

        # Store transform joint data in the KST node
        KstCore.write_info_to_node('jointList', joint_list)

        # Store the list in the global var
        self._joint_list = joint_list

        return joint_list
    """
    # </editor-fold>

    # Make surface from guides
    def create_interpolation_joints(self, input_points, radius=1.0, from_node = False):
        '''
        Desc:
        _

        Parameter:
        _

        Return:
        '''

        # curve = KstRig.create_line_from_objects(crv_name=self._kname, objects_list=input_points)
        # curve = cmds.rebuildCurve(curve, kcp=True, d=3)

        # Define variable for follicle_list
        follicle_interp_list = []

        # Split the object list by 2, that's perfect for create joint procedure
        nsplit = 2

        # Creating a list with points up
        input_points_temp = []
        for pt in input_points:
            pt_up = str(pt).replace('down', 'up')
            input_points_temp.append(pt_up)

        # Divide two list in chuncks every 2
        input_points_by_two_up = [input_points_temp[x:x+nsplit] for x in xrange(0, len(input_points_temp), 2)]
        input_points_by_two_down = [input_points[x:x+nsplit] for x in xrange(0, len(input_points), 2)]

        # Collect two list of middle point for up and down in the middle position of existing chunks list
        i = 0
        pt_mid_list_up = []
        pt_mid_list_down = []

        for pt in input_points:
            temp_pt = str(pt).replace('down', 'up')
            if i > 0 and i < len(input_points)-1:
                pt_mid_list_up.append(temp_pt)
                pt_mid_list_down.append(pt)
            i=i+1

        # Insert middle couple of point in the middle of existing list
        input_points_by_two_down.insert(1, pt_mid_list_down)
        input_points_by_two_up.insert(1, pt_mid_list_up)

        # Store mid locators created by chunks list in a list
        mid_locs=[]

        # For each couple joint couple, make the chain down list
        j = 0
        for chunk in input_points_by_two_down:
            pos_up = KstMaya.get_position_list_from_objs(input_points_by_two_up[j], coords_space='world')
            pos_down = KstMaya.get_position_list_from_objs(chunk, coords_space='world')
            loc_up = KstRig.create_maya_object('locator', '_midup_'+self._kname+'_'+str(j+1).zfill(3)+'_LOC')
            loc_down = KstRig.create_maya_object('locator', '_middown_'+self._kname+'_'+str(j+1).zfill(3)+'_LOC')
            mid_up = om.MVector(om.MVector(pos_up[0][0], pos_up[0][1], pos_up[0][2])+om.MVector(pos_up[1][0], pos_up[1][1], pos_up[1][2]))/2
            mid_down = om.MVector(om.MVector(pos_down[0][0], pos_down[0][1], pos_down[0][2])+om.MVector(pos_down[1][0], pos_down[1][1], pos_down[1][2]))/2

            # Set position for locator up
            cmds.setAttr(loc_up+'.tx', mid_up.x)
            cmds.setAttr(loc_up+'.ty', mid_up.y)
            cmds.setAttr(loc_up+'.tz', mid_up.z)
            cmds.setAttr(loc_up+'.overrideEnabled',1)
            cmds.setAttr(loc_up+'.overrideColor', 17)

            # Set position for locator down
            cmds.setAttr(loc_down+'.tx', mid_down.x)
            cmds.setAttr(loc_down+'.ty', mid_down.y)
            cmds.setAttr(loc_down+'.tz', mid_down.z)
            cmds.setAttr(loc_down+'.overrideEnabled',1)
            cmds.setAttr(loc_down+'.overrideColor', 17)

            # Append both locator to mid_locs list
            mid_locs.append(loc_up)
            mid_locs.append(loc_down)
            j=j+1

        # Project mid locators down on curve and change the final position
        for loc in mid_locs:
            if 'up' in loc:
                fol_up = KstRig.attach_object_to_surface(self._surfaces[0], loc)
                follicle_interp_list.append(fol_up)

            if 'down' in loc:
                fol_down = KstRig.attach_object_to_surface(self._surfaces[1], loc)
                follicle_interp_list.append(fol_down)

        # Reuse the method generate_joints_on_surface ToDo, put in a universal object and make class
        # Make an empty list for store joints
        joint_chain_interp = []

        # Redefine follicle list for comodity
        follicle_list = follicle_interp_list

        # Chunks string
        import string
        chunks_list = list(string.ascii_lowercase)

        # Split the object list by 2, that's perfect for create joint procedure
        nsplit = 2
        object_list_by_two = [follicle_list[x:x+nsplit] for x in xrange(0, len(follicle_list), 2)]
        chunks_list_by_two = [follicle_list[x:x+nsplit] for x in xrange(0, len(follicle_list), 2)]

        i = 0
        # For each couple joint couple, make the chain
        for chunk in object_list_by_two:

            # Define the object where will be parented the chain joint
            obj_to_parent = chunk[0]

            newname = chunk[0].replace(self._part+'_', '&')
            newname = newname.split('&', -1)[0]+self._part

            # Make the joint
            jnt = KstRig.create_joint_chain(newname+'_'+str(i+1).zfill(3), chunk, radius = radius)

            if 'up_' in obj_to_parent:
                # Make the object upVector
                up_vec = KstRig.create_maya_node('locator', obj_to_parent.replace('_TGRP','_UPVEC'))

                # Parent upVec to transform
                cmds.parent(up_vec, obj_to_parent)

                # Reset position and size to up_vec
                t_channels = ('tx', 'ty', 'tz')
                r_channels = ('rx', 'ry', 'rz')
                s_channels = ('sx', 'sy', 'sz')

                k = 0
                for chn in t_channels:
                    cmds.setAttr(up_vec+'.'+chn, 0)
                    cmds.setAttr(up_vec+'.'+r_channels[k], 0)
                    cmds.setAttr(up_vec+'.'+s_channels[k], .2)
                    k=k+1

                # Move the up_vec in the right position for a good aim
                cmds.xform(up_vec, t=[0, 0, 3])

                # Var for aim vec
                aim_vec = obj_to_parent.replace('up','down')

                # Make aim constraint
                # NOTE* IT'S VALID IF THE WING IT'S ON Y/X PLANE AXIS

                aim_name = str(jnt[0]).replace('_JNT','')

                # Add a transformation group
                trs = KstRig.create_maya_node('transform', node_name=newname+'_'+str(i+1).zfill(3)+'_TGRP')
                KstDraw.debug_axis(trs)

                # Parent transform to follicle
                cmds.parent(trs, obj_to_parent)

                # Put axis on up chain
                KstMaya.make_constraint(jnt[0], trs, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')

                #aim = KstMaya.make_constraint(aim_vec, jnt[0], constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)
                aim = KstMaya.make_constraint(aim_vec, trs, constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)

            # Parent joint to trs
            cmds.parent(jnt[0], trs)

            joint_chain_interp.append(jnt)
            i=i+1

        # Change color
        for jnt in joint_chain_interp:
            cmds.setAttr(jnt[0]+'.overrideEnabled',1)
            cmds.setAttr(jnt[0]+'.overrideColor', 20)

        # Store transform joint data in the KST node
        KstCore.write_info_to_node('interpJoints', joint_chain_interp)

        # Store the list in the global var
        self._joint_interp_list = joint_chain_interp

        return joint_chain_interp

    # <editor-fold desc="create_interpolation_joints: CODE THAT WORKS IN MY PROTOTYPE">
    """
    # Make surface from guides
    def create_interpolation_joints(self, input_points, radius=1.0, from_node = False):
        '''
        Desc:
        _

        Parameter:
        _

        Return:
        '''

        # curve = KstRig.create_line_from_objects(crv_name=self._kname, objects_list=input_points)
        # curve = cmds.rebuildCurve(curve, kcp=True, d=3)

        # Define variable for follicle_list
        follicle_interp_list = []

        # Split the object list by 2, that's perfect for create joint procedure
        nsplit = 2

        # Creating a list with points up
        input_points_temp = []
        for pt in input_points:
            pt_up = str(pt).replace('down', 'up')
            input_points_temp.append(pt_up)

        # Divide two list in chuncks every 2
        input_points_by_two_up = [input_points_temp[x:x+nsplit] for x in xrange(0, len(input_points_temp), 2)]
        input_points_by_two_down = [input_points[x:x+nsplit] for x in xrange(0, len(input_points), 2)]

        # Collect two list of middle point for up and down in the middle position of existing chunks list
        i = 0
        pt_mid_list_up = []
        pt_mid_list_down = []

        for pt in input_points:
            temp_pt = str(pt).replace('down', 'up')
            if i > 0 and i < len(input_points)-1:
                pt_mid_list_up.append(temp_pt)
                pt_mid_list_down.append(pt)
            i=i+1

        # Insert middle couple of point in the middle of existing list
        input_points_by_two_down.insert(1, pt_mid_list_down)
        input_points_by_two_up.insert(1, pt_mid_list_up)

        # Store mid locators created by chunks list in a list
        mid_locs=[]

        # For each couple joint couple, make the chain down list
        j = 0
        for chunk in input_points_by_two_down:
            pos_up = KstMaya.get_position_list_from_objs(input_points_by_two_up[j], coords_space='world')
            pos_down = KstMaya.get_position_list_from_objs(chunk, coords_space='world')
            loc_up = KstRig.create_maya_object('locator', '_midup_'+self._kname+'_'+str(j+1).zfill(3)+'_LOC')
            loc_down = KstRig.create_maya_object('locator', '_middown_'+self._kname+'_'+str(j+1).zfill(3)+'_LOC')
            mid_up = om.MVector(om.MVector(pos_up[0][0], pos_up[0][1], pos_up[0][2])+om.MVector(pos_up[1][0], pos_up[1][1], pos_up[1][2]))/2
            mid_down = om.MVector(om.MVector(pos_down[0][0], pos_down[0][1], pos_down[0][2])+om.MVector(pos_down[1][0], pos_down[1][1], pos_down[1][2]))/2

            # Set position for locator up
            cmds.setAttr(loc_up+'.tx', mid_up.x)
            cmds.setAttr(loc_up+'.ty', mid_up.y)
            cmds.setAttr(loc_up+'.tz', mid_up.z)
            cmds.setAttr(loc_up+'.overrideEnabled',1)
            cmds.setAttr(loc_up+'.overrideColor', 17)

            # Set position for locator down
            cmds.setAttr(loc_down+'.tx', mid_down.x)
            cmds.setAttr(loc_down+'.ty', mid_down.y)
            cmds.setAttr(loc_down+'.tz', mid_down.z)
            cmds.setAttr(loc_down+'.overrideEnabled',1)
            cmds.setAttr(loc_down+'.overrideColor', 17)

            # Append both locator to mid_locs list
            mid_locs.append(loc_up)
            mid_locs.append(loc_down)
            j=j+1

        # Project mid locators down on curve and change the final position
        for loc in mid_locs:
            if 'up' in loc:
                fol_up = KstRig.attach_object_to_surface(self._surfaces[0], loc)
                follicle_interp_list.append(fol_up)

            if 'down' in loc:
                fol_down = KstRig.attach_object_to_surface(self._surfaces[1], loc)
                follicle_interp_list.append(fol_down)

        # Reuse the method generate_joints_on_surface ToDo, put in a universal object and make class
        # Make an empty list for store joints
        joint_chain_interp = []

        # Redefine follicle list for comodity
        follicle_list = follicle_interp_list

        # Chunks string
        import string
        chunks_list = list(string.ascii_lowercase)

        # Split the object list by 2, that's perfect for create joint procedure
        nsplit = 2
        object_list_by_two = [follicle_list[x:x+nsplit] for x in xrange(0, len(follicle_list), 2)]
        chunks_list_by_two = [follicle_list[x:x+nsplit] for x in xrange(0, len(follicle_list), 2)]

        i = 0
        # For each couple joint couple, make the chain
        for chunk in object_list_by_two:

            # Define the object where will be parented the chain joint
            obj_to_parent = chunk[0]

            newname = chunk[0].replace(self._part+'_', '&')
            newname = newname.split('&', -1)[0]+self._part

            # Make the joint
            jnt = KstRig.create_joint_chain(newname+'_'+str(i+1).zfill(3), chunk, radius = radius)

            if 'up_' in obj_to_parent:
                # Make the object upVector
                up_vec = KstRig.create_maya_node('locator', obj_to_parent.replace('_TGRP','_UPVEC'))

                # Parent upVec to transform
                cmds.parent(up_vec, obj_to_parent)

                # Reset position and size to up_vec
                t_channels = ('tx', 'ty', 'tz')
                r_channels = ('rx', 'ry', 'rz')
                s_channels = ('sx', 'sy', 'sz')

                k = 0
                for chn in t_channels:
                    cmds.setAttr(up_vec+'.'+chn, 0)
                    cmds.setAttr(up_vec+'.'+r_channels[k], 0)
                    cmds.setAttr(up_vec+'.'+s_channels[k], .2)
                    k=k+1

                # Move the up_vec in the right position for a good aim
                cmds.xform(up_vec, t=[0, 0, 3])

                # Var for aim vec
                aim_vec = obj_to_parent.replace('up','down')

                # Make aim constraint
                # NOTE* IT'S VALID IF THE WING IT'S ON Y/X PLANE AXIS

                aim_name = str(jnt[0]).replace('_JNT','')

                # Add a transformation group
                trs = KstRig.create_maya_node('transform', node_name=newname+'_'+str(i+1).zfill(3)+'_TGRP')
                KstDraw.debug_axis(trs)

                # Parent transform to follicle
                cmds.parent(trs, obj_to_parent)

                # Put axis on up chain
                KstMaya.make_constraint(jnt[0], trs, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')

                #aim = KstMaya.make_constraint(aim_vec, jnt[0], constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)
                aim = KstMaya.make_constraint(aim_vec, trs, constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)

            # Parent joint to trs
            cmds.parent(jnt[0], trs)

            joint_chain_interp.append(jnt)
            i=i+1

        # Change color
        for jnt in joint_chain_interp:
            cmds.setAttr(jnt[0]+'.overrideEnabled',1)
            cmds.setAttr(jnt[0]+'.overrideColor', 20)

        # Store transform joint data in the KST node
        KstCore.write_info_to_node('interpJoints', joint_chain_interp)

        # Store the list in the global var
        self._joint_interp_list = joint_chain_interp

        return joint_chain_interp
        """
    # </editor-fold>

    def generate_wing_surfaces(self, points_list, offset=0, radius=1.0, from_node=True):
        '''
        Desc:
        _

        Parameter:
        _

        Return:
        '''

        # Make a variable for extra lovator for projection
        obj_to_project = []

        # Make var for surface list
        surfaces = []

        # Result points variable
        follicle_list = []

        # Variable for offset joints
        offset_joints_list = []

        # Duplicate object in list
        i=1
        for pt in points_list:
            if i > 1 and i < len(points_list):
                this_point_up = str(pt).replace('down', 'up')
                obj_to_project.append(this_point_up)
                obj_to_project.append(pt)
            i=i+1

        ext_follicle_list = []
        int_follicle_list = []

        for pt in obj_to_project:
            print ('CURRENT PT: ', pt)

            if 'up' in pt:
                # Create and store all external follicle up
                copy_left = KstMaya.duplicate_this(pt, 'ext_')
                cmds.parent(copy_left[0], pt)
                cmds.setAttr(copy_left[0]+'.tx', offset)
                foll=KstRig.attach_object_to_surface(self._surfaces[0], copy_left[0])
                ext_follicle_list.append(foll)

                # Create and store all internal follicle up
                copy_right = KstMaya.duplicate_this(pt, 'int_')
                cmds.parent(copy_right[0], pt)
                cmds.setAttr(copy_right[0]+'.tx', offset*-1)
                foll=KstRig.attach_object_to_surface(self._surfaces[0], copy_right[0])
                int_follicle_list.append(foll)

            if 'down' in pt:
                # Create and store all external follicle down
                copy_left = KstMaya.duplicate_this(pt, 'ext_')
                cmds.parent(copy_left[0], pt)
                cmds.setAttr(copy_left[0]+'.tx', offset)
                foll=KstRig.attach_object_to_surface(self._surfaces[1], copy_left[0])
                ext_follicle_list.append(foll)

                # Extract UV param for generate curve at that value


                # Create and store all internal follicle down
                copy_right = KstMaya.duplicate_this(pt, 'int_')
                cmds.parent(copy_right[0], pt)
                cmds.setAttr(copy_right[0]+'.tx', offset*-1)
                foll=KstRig.attach_object_to_surface(self._surfaces[1], copy_right[0])
                int_follicle_list.append(foll)

                # Extract UV param for generate curve at that value


        print ext_follicle_list
        print int_follicle_list

        # Chunks string
        import string
        chunks_list = list(string.ascii_lowercase)

        # Split the object list by 2, that's perfect for create joint procedure
        nsplit = 2
        object_list_by_two_ext = [ext_follicle_list[x:x+nsplit] for x in xrange(0, len(ext_follicle_list), 2)]
        object_list_by_two_int = [int_follicle_list[x:x+nsplit] for x in xrange(0, len(int_follicle_list), 2)]

        i = 0
        # For each couple joint couple, make the chain
        for chunk in object_list_by_two_ext:

            # Define the object where will be parented the chain joint
            obj_to_parent = chunk[0]

            newname = chunk[0].replace(self._part+'_', '&')
            newname = newname.split('&', -1)[0]+self._part

            # Make the joint
            jnt = KstRig.create_joint_chain(newname+'_'+str(i+1).zfill(3), chunk, radius = radius)

            if 'up_' in obj_to_parent:
                # Make the object upVector
                up_vec = KstRig.create_maya_node('locator', obj_to_parent.replace('_TGRP','_UPVEC'))

                # Parent upVec to transform
                cmds.parent(up_vec, obj_to_parent)

                # Reset position and size to up_vec
                t_channels = ('tx', 'ty', 'tz')
                r_channels = ('rx', 'ry', 'rz')
                s_channels = ('sx', 'sy', 'sz')

                k = 0
                for chn in t_channels:
                    cmds.setAttr(up_vec+'.'+chn, 0)
                    cmds.setAttr(up_vec+'.'+r_channels[k], 0)
                    cmds.setAttr(up_vec+'.'+s_channels[k], .2)
                    k=k+1

                # Move the up_vec in the right position for a good aim
                cmds.xform(up_vec, t=[0, 0, 3])

                # Var for aim vec
                aim_vec = obj_to_parent.replace('up','down')

                # Make aim constraint
                # NOTE* IT'S VALID IF THE WING IT'S ON Y/X PLANE AXIS

                aim_name = str(jnt[0]).replace('_JNT','')

                # Add a transformation group
                trs = KstRig.create_maya_node('transform', node_name=newname+'_'+str(i+1).zfill(3)+'_TGRP')
                KstDraw.debug_axis(trs)

                # Parent transform to follicle
                cmds.parent(trs, obj_to_parent)

                # Put axis on up chain
                KstMaya.make_constraint(jnt[0], trs, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')

                #aim = KstMaya.make_constraint(aim_vec, jnt[0], constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)
                aim = KstMaya.make_constraint(aim_vec, trs, constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)


            # Parent joint to trs
            cmds.parent(jnt[0], trs)

            offset_joints_list.append(jnt)
            i=i+1

        i = 0
        # For each couple joint couple, make the chain
        for chunk in object_list_by_two_int:

            # Define the object where will be parented the chain joint
            obj_to_parent = chunk[0]

            newname = chunk[0].replace(self._part+'_', '&')
            newname = newname.split('&', -1)[0]+self._part

            # Make the joint
            jnt = KstRig.create_joint_chain(newname+'_'+str(i+1).zfill(3), chunk, radius = radius)

            if 'up_' in obj_to_parent:
                # Make the object upVector
                up_vec = KstRig.create_maya_node('locator', obj_to_parent.replace('_TGRP','_UPVEC'))

                # Parent upVec to transform
                cmds.parent(up_vec, obj_to_parent)

                # Reset position and size to up_vec
                t_channels = ('tx', 'ty', 'tz')
                r_channels = ('rx', 'ry', 'rz')
                s_channels = ('sx', 'sy', 'sz')

                k = 0
                for chn in t_channels:
                    cmds.setAttr(up_vec+'.'+chn, 0)
                    cmds.setAttr(up_vec+'.'+r_channels[k], 0)
                    cmds.setAttr(up_vec+'.'+s_channels[k], .2)
                    k=k+1

                # Move the up_vec in the right position for a good aim
                cmds.xform(up_vec, t=[0, 0, 3])

                # Var for aim vec
                aim_vec = obj_to_parent.replace('up','down')

                # Make aim constraint
                # NOTE* IT'S VALID IF THE WING IT'S ON Y/X PLANE AXIS

                aim_name = str(jnt[0]).replace('_JNT','')

                # Add a transformation group
                trs = KstRig.create_maya_node('transform', node_name=newname+'_'+str(i+1).zfill(3)+'_TGRP')
                KstDraw.debug_axis(trs)

                # Parent transform to follicle
                cmds.parent(trs, obj_to_parent)

                # Put axis on up chain
                KstMaya.make_constraint(jnt[0], trs, constraint_type='parent', maintain_offset=False, keep_constraint_node=False, name='temp_name')

                #aim = KstMaya.make_constraint(aim_vec, jnt[0], constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)
                aim = KstMaya.make_constraint(aim_vec, trs, constraint_type='aim', maintain_offset=True, weight=1.0, aim_vec=[1,0,0], up_vec=[0,1,0], world_up_type='object', world_up_object=up_vec, name=aim_name)

            # Parent joint to trs
            cmds.parent(jnt[0], trs)

            offset_joints_list.append(jnt)
            i=i+1

        # Change color
        for jnt in offset_joints_list:
            cmds.setAttr(jnt[0]+'.overrideEnabled',1)
            cmds.setAttr(jnt[0]+'.overrideColor', 23)

        # List all joints for build final surfaces
        print('DEBUG joint_list: ', self._joint_list)
        print('DEBUG joint_interp_list: ', self._joint_interp_list)
        print('DEBUG offset_joint_list: ', offset_joints_list)

        i = 0
        # For each couple joint couple, make a line
        for chunk in self._joint_list:
            pt_a = chunk[0]
            pt_b = chunk[1]

            pt_pos = KstMaya.get_position_list_from_objs([pt_a, pt_b])
            KstRig.create_line_from_2_points(str(pt_a).replace('_JNT',''), pt_pos[0], pt_pos[1])

            #newname = chunk[0].replace(self._part+'_', '&')
            #newname = newname.split('&', -1)[0]+self._part
            i=i+1

        j = 0
        # For each couple joint couple, make a line
        for chunk in self._joint_interp_list:
            pt_a = chunk[0]
            pt_b = chunk[1]

            pt_pos = KstMaya.get_position_list_from_objs([pt_a, pt_b])
            KstRig.create_line_from_2_points(str(pt_a).replace('_JNT',''), pt_pos[0], pt_pos[1])

            #newname = chunk[0].replace(self._part+'_', '&')
            #newname = newname.split('&', -1)[0]+self._part
            j=j+1

        k = 0
        # For each couple joint couple, make a line
        for chunk in offset_joints_list:
            pt_a = chunk[0]
            pt_b = chunk[1]

            pt_pos = KstMaya.get_position_list_from_objs([pt_a, pt_b])
            KstRig.create_line_from_2_points(str(pt_a).replace('_JNT',''), pt_pos[0], pt_pos[1])

            #newname = chunk[0].replace(self._part+'_', '&')
            #newname = newname.split('&', -1)[0]+self._part
            k=k+1

        # Define the curves that will be compound the surfaces
        curves_surface_a = ['up_Wing_L_001_CRV', '_midup_Wing_L_001_CRV', 'int_up_Wing_L_001_CRV']
        curves_surface_b = ['ext_up_Wing_L_001_CRV', '_midup_Wing_L_002_CRV', 'int_up_Wing_L_002_CRV']
        curves_surface_c = ['ext_up_Wing_L_002_CRV', '_midup_Wing_L_003_CRV', 'up_Wing_L_004_CRV']

        # Generate surface from input guides list
        # *IMPORTANT: by default the normalization is set to True, otherwise closestPontOnSurface is not calculated properly
        surface_a = KstRig.create_surface_from_curves(curves_surface_a, surface_name='feathers_a_'+self._kname)
        surface_b = KstRig.create_surface_from_curves(curves_surface_b, surface_name='feathers_b_'+self._kname)
        surface_c = KstRig.create_surface_from_curves(curves_surface_c, surface_name='feathers_c_'+self._kname)

        return [surface_a, surface_b, surface_c]