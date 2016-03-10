'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Maya Module Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

#ToDo: implement a debug mode for print or not

import pymel as pm                                          # import pymel lib
import maya.cmds as cmds                                    # import maya cmds lib
import maya.mel as mel                                      # import maya mel lib
import maya.OpenMaya as om

# Import kstCore
import kcode.kcore.KstCore as _KstCore_
reload(_KstCore_)
KstCore = _KstCore_.KstCore()

# Import kstMath
import kcode.kmath.KstMath as _KstMath_
reload(_KstMath_)
KstMath = _KstMath_.KstMath()

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

class KstMaya(object):
    # Debug module name variable
    _debug = 'KstMaya'

    def __init__(self):
        KstOut.debug('Kistie Maya function module loaded... ')

    # Channels Operation method
    def channels_op(self, selections, channels_list, *args):
        '''
        Desc:
        Make operation on channels

        Parameter:
        selections = list of selection where perform operations
        *args = type of operation (lock, hide)
        channels_list = list of channels to perform operations

        Return void

        Example:
        KstMaya.channels_op(['selection'], ['ch','ch','ch'], 'lock=Bool', 'keyable=Bool', 'channelBox=Bool')
        '''

        # Declare variable for errors
        errors_list = []

        # Check if selections type input is valid
        if not type(selections) is list:
            KstOut.debug(KstMaya._debug, 'selections must be a list!')
            errors_list.append('selections')

        # Check if channels_list input is valid
        if not type(channels_list) is list:
            KstOut.debug(KstMaya._debug, 'channels_list must be a list!')
            errors_list.append('channels')

        try:
            # If there are no errors go
            if len(errors_list) == 0:
                # Create empty value for python command
                cmd = ''
                for sel in selections:
                    for ch in channels_list:
                        for count, arg in enumerate(args):
                            # Build string command
                            cmd = "cmds.setAttr('%s.%s', %s)" % (sel, ch, arg)

                            # Execute string command // ToDo, build a Kistie class for this
                            exec(cmd)

                            # Debug command
                            KstOut.debug(KstMaya._debug, cmd)

            # Otherwise stop and release errorsList
            else:
                KstOut.debug(KstMaya._debug, 'You have some errors: ', errors_list)
        except:
            KstOut.error(KstMaya._debug, 'Error found!!! '+str(errors_list))

    @staticmethod
    # Get Shape method
    def get_shape_node(transform):
        '''
        Desc:
        return a shape from a transform

        Parameter:
        transform = transform node that you want get the shape

        Return:
        Shape obj from the transform
        '''
        shape_list = cmds.listRelatives(transform, s=True)
        if shape_list:
            shape = shape_list[0]
            return shape
        else:
            #KstOut.debug(self._debug_msg, 'No shapes found in current transform, double check')
            return None

    # Get Transform method
    def get_transform_node(self, shape):
        '''
        Desc:
        return a transform from a shape

        Parameter:
        shape = shape node that you want get the transform

        Return:
        Transform obj from the shape
        '''
        try:
            transform_list = cmds.listRelatives(shape, p=True)
            if transform_list:
                transform = transform_list[0]
                return transform
        except:
            KstOut.debug(KstMaya._debug, 'No transform found in current shape, double check')
            pass

    # Get Parent method
    @staticmethod
    def get_his_parent(obj):
        '''
        Desc:
        return parent from an object

        Parameter:
        obj = object to get the parent

        Return:
        Parent object
        '''
        try:
            parent = cmds.listRelatives(obj, p=True)
            if parent:
                return parent
        except:
            KstOut.debug(KstMaya._debug, 'No parent object found, double check')
            pass

    # Get Parent method
    @staticmethod
    def get_his_child(obj):
        '''
        Desc:
        return child from an object

        Parameter:
        obj = object to get the child

        Return:
        Parent object
        '''
        try:
            child = cmds.listRelatives(obj, c=True)
            if child:
                return child
        except:
            KstOut.debug(KstMaya._debug, 'No child object found, double check')
            pass

    # Get all input type (nodeType) nodes in scene
    def get_node_type(self, node_type):
        '''
        Desc:
        return a list of node founded from nodeType parameter

        Parameter:
        node_type = nodes type to find

        Return:
        a list with node of that type defined in input
        '''
        node_list = cmds.ls(type=node_type)
        found_nodes = []
        if node_list:
            KstOut.debug(KstMaya._debug, str(node_type)+' nodes list: ')
            for node in node_list:
                KstOut.debug(KstMaya._debug, 'nodetype = '+str(node_type)+'-> '+str(node))
                found_nodes.append(node)
        else:
            KstOut.debug(KstMaya._debug, 'nodetype "'+str(node_type)+'" not exists!')
        return found_nodes

    # Get all input name (nodeName) nodes in scene
    def get_node_if_name_contains(self, node_name):
        '''
        Desc:
        return a list of node founded from nodeName parameter

        Parameter:
        node_name = nodes name to find

        Return:
        a list with node of that contains name defined in input
        '''
        node_list = cmds.ls()
        found_nodes = []
        if node_list:
            for node in node_list:
                if node_name in node:
                    KstOut.debug(KstMaya._debug, '-> '+str(node))
                    found_nodes.append(node)
        else:
            KstOut.debug(KstMaya._debug, str(node_name)+' not exists')
        return found_nodes

    # Make a copy of the inputObject
    def duplicate_this(self, input_object, copy_name='cpy_'):
        '''
        Desc:
        return a obj that is the copy of inputObject with a name defined in nameOfCopy

        Parameter:
        input_object = the object to be copied
        copy_name = the copy name

        Return:
        the obj copied from the original with the new name
        '''

        if input_object:
            #cmds.select(input_object)
            copy_object = cmds.duplicate(input_object, smartTransform=True, name = copy_name, renameChildren = True)
            copy_object[0] = cmds.rename(copy_object[0], copy_name+input_object)
            #print('DEBUG copy object: ', copy_object)

            # Search all children of the current object for renaming
            hierarchy = cmds.listRelatives(copy_object, c=True)
            if hierarchy:
                for child in hierarchy:
                    cmds.rename(child, copy_name+child[:-1])

                KstOut.debug(KstMaya._debug, str(copy_object[0])+" duplicated from "+str(input_object))
                return copy_object
        else:
            KstOut.debug(KstMaya._debug, ' inputObject empty, check selection, or array')

    # Make connection between two node with specified attributes ToDo: add code for test if connection is already in there or not, if it is force delete
    def node_op(self, src, op, dst):
        '''
        Desc:
        Make node operation between two object+attributes

        Parameter:
        src = source object and attr
        op = operator:
        this value can be
        >> connect SRC to DST
        << connect DST to SRC
        \\ disconnect SRC from DST
        dst = destinatin object and attr

        Return:
        bool attribute, True if connection was done, otherwise in all others case False
        '''
        stat = False
        if src and dst and op:
            if op == '>>':
                try:
                    cmds.connectAttr(src, dst, f=True)
                    stat = True
                except:
                    KstOut.debug(KstMaya._debug, 'Error occurred making connection src, dst')
                    KstOut.debug(KstMaya._debug, 'DEBUG DATA: ')
                    KstOut.debug(KstMaya._debug, '%s = SOURCE' % src)
                    KstOut.debug(KstMaya._debug, '%s = DESTINATION' % dst)
                    KstOut.debug(KstMaya._debug, '-> END DATA')
                    print 'CANNOT ', src, dst

            elif op == '<<':
                try:
                    cmds.connectAttr(dst, src, f=True)
                    stat = True
                except:
                    KstOut.debug(KstMaya._debug, 'Error occurred making connection dst, src')
                    KstOut.debug(KstMaya._debug,'DEBUG DATA: ')
                    KstOut.debug(KstMaya._debug, '%s = SOURCE' % src)
                    KstOut.debug(KstMaya._debug, '%s = DESTINATION' % dst)
                    KstOut.debug(KstMaya._debug, '-> END DATA')
                    # print ''

            elif op == '||':
                try:
                    cmds.disconnectAttr(src, dst, f=True)
                    stat = True
                except:
                    KstOut.debug(KstMaya._debug, 'Error occurred in disconnection')
                    KstOut.debug(KstMaya._debug, 'DEBUG DATA: ')
                    KstOut.debug(KstMaya._debug, '%s = SOURCE' % src)
                    KstOut.debug(KstMaya._debug, '%s = DESTINATION' % dst)
                    KstOut.debug(KstMaya._debug, '-> END DATA')
                    # print ''

            else:
                KstOut.debug(KstMaya._debug, ' symbol not defined, you can use (>>, <<, ||)')
                stat = False

            return stat
        else:
            KstOut.debug(KstMaya._debug, ' double check inputs (source, operator, destination)')
            KstOut.error(KstMaya._debug, ' double check inputs (source, operator, destination)')
            return None

    # Destroy all connections, finally works with keyframes and normal connections
    def destroy_channels_connections(self, sel, channels_list):
        '''
        Desc:
        Destroy connections for selected channels
        sel = current object
        *args = list of channels to disconnect in format [ch,ch,ch,...]
        '''

        for ch in channels_list:
            src_attr = cmds.connectionInfo(sel+'.'+ch, sourceFromDestination=True)
            if src_attr:
                KstOut.debug(KstMaya._debug, 'SOURCE: '+src_attr)
                KstOut.debug(KstMaya._debug, 'DEST: '+sel+'.'+ch)
                cmds.disconnectAttr(src_attr, sel+'.'+ch)

    # Make constraint in more simple mode
    def make_constraint(self, src, dst, constraint_type='aim', skip_translate='none', skip_rotate='none', maintain_offset=False, weight=1, aim_vec=[0,1,0], up_vec=[0,0,1], world_up_type='vector', world_up_vec=[0,0,1], world_up_object=None, keep_constraint_node = True, name = None):
        '''
        Desc:
        Make any contraint

        Parameter:
        src = source object object contraint from
        dst = destination object constraint to:
        constraintType = constraint type
        offset = mantaintOffset bool val

        Return:
        contraint str name
        '''
        # var for constraint name
        constraint = []
        type=''

        # Fix name
        name = str(name).replace("u'",'').replace('[',' ').replace(']',' ').replace("'",' ').replace(' ', '')

        # Parent constraint
        if constraint_type == 'parent':
            type='PAC'
            constraint = cmds.parentConstraint(src, dst, mo=maintain_offset, w=weight, st=skip_translate, name=name+'_'+type)

        # Point constraint
        elif constraint_type == 'point':
            type='PC'
            constraint = cmds.pointConstraint(src, dst, mo=maintain_offset, w=weight, sk=skip_translate, name=name+'_'+type)

        # Orient constraint
        elif constraint_type == 'orient':
            type='OC'
            constraint = cmds.orientConstraint(src, dst, mo=maintain_offset, w=weight, sk=skip_rotate, name=name+'_'+type)

        # Aim constraint, ToDo, optimize
        elif constraint_type == 'aim':
            type='AC'
            if world_up_type == 'object':
                if world_up_object == None:
                    KstOut.debug(KstMaya._debug, "Check object up variable, can't be set to None")
                else:
                    constraint = cmds.aimConstraint(src, dst, mo=maintain_offset, w=weight, sk=skip_rotate, aimVector=aim_vec, upVector=up_vec, worldUpType=world_up_type, worldUpVector=world_up_vec, worldUpObject=world_up_object, name=name+'_'+type)
            else:
                constraint = cmds.aimConstraint(src, dst, mo=maintain_offset, w=weight, sk=skip_rotate, aimVector=aim_vec, upVector=up_vec, worldUpType=world_up_type, worldUpVector=world_up_vec, name=name+'_'+type)

        #constraint = cmds.rename(constraint[0], '%s_%s' % (constraint[0], type))

        # Delete constraint node if needed
        if keep_constraint_node == False:
            cmds.delete(constraint)

        return constraint

    # Make multi constraint in more simple mode
    def make_multi_constraint(self, src_list, dst, constraint_type='aim', skip_translate='none', skip_rotate='none', maintain_offset=False, weights_list=[1.0], aim_vec=[0,1,0], up_vec=[0,0,1], world_up_type='vector', world_up_vec=[0,0,1], world_up_object=None, keep_constraint_node = True, name = None):
        '''
        Desc:
        Make multiconstraint for any contraint

        Parameter:
        src = source object object contraint from
        dst = destination object constraint to:
        constraintType = constraint type
        offset = mantaintOffset bool val

        Return:
        contraint str name
        '''
        # var for constraint name
        constraint = []
        type=''

        # Fix name
        name = str(name).replace("u'",'').replace('[',' ').replace(']',' ').replace("'",' ').replace(' ', '')

        # Loop each element in src_list
        i = 0
        for src in src_list:
            # Parent constraint
            if constraint_type == 'parent':
                type='PAC'
                constraint = cmds.parentConstraint(src, dst, mo=maintain_offset, w=weights_list[i], st=skip_translate, name=name+'_'+type)
                i = i+1

            # Point constraint
            elif constraint_type == 'point':
                type='PC'
                constraint = cmds.pointConstraint(src, dst, mo=maintain_offset, w=weights_list[i], sk=skip_translate, name=name+'_'+type)
                i = i+1

            # Orient constraint
            elif constraint_type == 'orient':
                type='OC'
                constraint = cmds.orientConstraint(src, dst, mo=maintain_offset, w=weights_list[i], sk=skip_rotate, name=name+'_'+type)
                i = i+1

            # Aim constraint, ToDo, optimize
            elif constraint_type == 'aim':
                type='AC'
                if world_up_type == 'object':
                    if world_up_object == None:
                        KstOut.debug(KstMaya._debug, "Check object up variable, can't be set to None")
                    else:
                        constraint = cmds.aimConstraint(src, dst, mo=maintain_offset, w=weights_list[i], sk=skip_rotate, aimVector=aim_vec, upVector=up_vec, worldUpType=world_up_type, worldUpVector=world_up_vec, worldUpObject=world_up_object, name=name+'_'+type)
                else:
                    constraint = cmds.aimConstraint(src, dst, mo=maintain_offset, w=weights_list[i], sk=skip_rotate, aimVector=aim_vec, upVector=up_vec, worldUpType=world_up_type, worldUpVector=world_up_vec, name=name+'_'+type)
                i = i+1

            #constraint = cmds.rename(constraint[0], '%s_%s' % (constraint[0], type))

            # Delete constraint node if needed
            if keep_constraint_node == False:
                cmds.delete(constraint)

        return constraint

    # Get position list from object position
    def get_position_list_from_objs(self, object_list, coords_space='world'):
        '''
        Desc:
        Get a position list from object list

        Parameter:
        object_list = the object list
        coords_space = the coordinat space, can be "world" (default), or "local"

        Return:
        list with positions
        '''
        position_list = []
        # Check if position list is valid
        if object_list:
            # Set coords to world
            if coords_space == 'world':
                world_space = True
                object_space = False

            # Set coord to local
            elif coords_space == 'local':
                world_space = False
                object_space = True

            for obj in object_list:
                KstOut.debug(KstMaya._debug, obj)
                obj_pos = cmds.xform(obj, q=True, t=True, ws=world_space, os=object_space)
                position_list.append(obj_pos)
            return position_list
        else:
            KstOut.debug(KstMaya._debug, 'Check if inputs are valid')
            return None

    # Get cvs list
    def get_num_cvs(self, curve):
        '''
        Desc:
        Get cvs lenght from a curve

        Parameter:
        curve = curve to get cvs positin list from
        coords_space = the coordinat space, can be "world" (default), or "local"

        Return:
        list with positions
        '''

        # If curve is nod define or not correct release error
        if curve:
            # Get curve shape
            curve_shape = KstMaya.get_shape_node(curve)

            # Get degree
            degree = cmds.getAttr(curve_shape+".degree")

            # Get spans
            spans = cmds.getAttr(curve_shape+".spans")

            # Calulating ncvs with formula spans+degree
            ncvs = spans+degree

            # Return the list
            return ncvs
        else:
            cmds.warning("Curve %s,  is not defined, or is not a curve, double check!" % curve)
            return None

    @staticmethod
    # Get position list from cvs position
    def get_cvs_position_list_from_curve(curve, coords_space='world'):
        '''
        Desc:
        Get cv position list from a curve

        Parameter:
        curve = curve to get cvs positin list from
        coords_space = the coordinat space, can be "world" (default), or "local"

        Return:
        list with positions
        '''

        # If curve is nod define or not correct release error
        if curve:
            # Define a list with all positions
            position_list = []

            # Define ws var
            ws = False

            # Get curve shape
            curve_shape = KstMaya.get_shape_node(curve)

            # Get degree
            degree = cmds.getAttr(curve_shape+".degree")

            # Get spans
            spans = cmds.getAttr(curve_shape+".spans")

            # Calulating ncvs with formula spans+degree
            ncvs = spans+degree

            # Define and set ws var for xform
            if coords_space=='world':
                ws = True

            # Iterate over curve cvs
            for i in range(0, ncvs):
                pos = cmds.xform(curve_shape+".cv[%s]" % i, q = True, t = True, ws = ws)
                position_list.append(pos)

            # Return the list
            return position_list
        else:
            cmds.warning("Curve %s,  is not defined, or is not a curve, double check!" % curve)
            return None

    def transfer_connections(self, src, dst, connections_list, mode = 'move'):
        '''
        Desc:
        Copy or Move, connections from one node to another one

        Parameter:
        src = source object move (or copy) connections from
        dst = destination object move (or copy) connections to
        connections_list = connections list to move or copy

        Return:
        None
        '''

        # List connections for src
        if len(connections_list):
            for conn in connections_list:
                src_connections = cmds.listConnections('%s.%s' % (src, conn), c = True, plugs = True)

                # Now in src_connections[0] there's the original src, and in src_connectons[0] the original destination
                # so, just replace the src_name
                # Store the current connection
                curr_conn = src_connections[0].split('.')[1]

                # If mode is setted on move disconnect old object
                if mode == 'move':
                    self.node_op(src_connections[0], '||', src_connections[1])

                # Exchange src with specified destination
                new_src = dst

                # Reconnect
                self.node_op('%s.%s' % (new_src, curr_conn), '>>', src_connections[1])


    # Insert element in hierarchy
    def insert_parent(self, src, dst, reset_src_trs = True):
        '''
        Desc:
        Insert an object in the middle of an existing hierarchy

        Parameter:
        src = object to insert
        dst = destination object that will be reparented

        Return:
        None
        '''
        # Check existing hierarchy
        # Who's the parent
        parent = KstMaya.get_his_parent(dst)

        # Who's the child
        child = KstMaya.get_his_child(dst)

        # Remake hiararchy
        cmds.parent(src, parent)
        cmds.parent(child, src)

        return parent, src, child

    def mirror_this(self, obj_to_mirror, plane = 'YZ'): # ToDo: finish and check
        '''
        Desc:
        Mirror object

        Parameter:
        src = object to insert
        dst = destination object that will be reparented

        Return:
        None
        '''
        mirrored = obj_to_mirror.replace('L','R')
        trs = cmds.xform(obj_to_mirror, q=True, t=True, ws=True)
        trs_vec = om.MVector(float(trs[0]), float(trs[1]), float(trs[2]))
        if plane == 'YZ':
            mirror_axis = om.MVector(-1, 1, 1)
        if plane == 'XZ':
            mirror_axis = om.MVector(1, -1, 1)
        if plane == 'YZ':
            mirror_axis = om.MVector(1, 1, -1)
        else:
            pass
        mirrored_coords = om.MVector(trs_vec.x * mirror_axis.x, trs_vec.y * mirror_axis.y, trs_vec.z * mirror_axis.z)
        cmds.setAttr('%s.%s' % (mirrored, 'tx'), mirrored_coords.x )
        cmds.setAttr('%s.%s' % (mirrored, 'ty'), mirrored_coords.y )
        cmds.setAttr('%s.%s' % (mirrored, 'tz'), mirrored_coords.z )
        return mirrored_coords

    # calculate the closest vertex from give distance
    def get_closest_vertices_between(self, src, dst, dist): # ToDo: check code
        '''
        Desc:
        Insert an object in the middle of an existing hierarchy

        Parameter:
        src = object to insert
        dst = destination object that will be reparented

        Return:
        None
        '''

        # Get the relative MObject for use method API for source and destination
        oSrc = KstCore.get_mobject_from_name(src)
        oDst = KstCore.get_mobject_from_name(dst)

        # Get the relative DAG for use method API for source and destination
        dSrc = KstCore.get_dag_from_node_name(src)
        dDst = KstCore.get_dag_from_node_name(dst)

        # Attach mesh functions to src and dst objects
        srcFnMesh = om.MFnMesh(dSrc)
        dstFnMesh = om.MFnMesh(dDst)

        # Define the list for closestVertex storage
        closest_vlist = list()

        # Check if the datatype is mesh
        if srcFnMesh.type() == om.MFn.kMesh and dstFnMesh.type() == om.MFn.kMesh:
            srcItVert = om.MItMeshVertex(oSrc)
            dstItVert = om.MItMeshVertex(oDst)

            # Define variables for mesh iterator
            srcVtxPos = om.MPoint()
            dstVtxPos = om.MPoint()
            ws = om.MSpace.kObject

            # Define empty point cloud for stora all position from the iterator
            srcVtxsPos = om.MPointArray()

            # Define empty point cloud for store closest points result
            closestPoints = om.MPointOnMesh()

            # Define MMeshIntersector on destination mesh for get closest point
            meshIntersector = om.MMeshIntersector()

            # Define a DAGPath for retrieve selection based on component
            selectionClosest = om.MSelectionList()
            selection_dag = om.MDagPath()

            # Iterate over all mesh vertices, and get all positions
            while not srcItVert.isDone():

                # Get current position
                srcVtxPos = srcItVert.position(ws)

                while not dstItVert.isDone():
                    srcVtxDest = dstItVert.position(ws)
                    mag = KstMath.get_mag(KstMath.vec_from_2_points(srcVtxPos, srcVtxDest))

                    if mag <= dist:
                        closest_vlist.append(dstItVert.index())
                        cmds.select(dst+'.vtx[%s]' % dstItVert.index(), add=True)
                    dstItVert.next()
                srcItVert.next()

            print('ARRAY CLOSEST: ', closest_vlist)


        '''
        clothRigGrp = "clothAnimRig_GRP"
        jntPos = cmds.xform(jnt, q=True, ws=True, t=True)
        sel = sel.replace("[u'","")
        sel = sel.replace("']","")
        scluster = str(sknMsh)
        scluster = scluster.replace("[u'","")
        scluster = scluster.replace("']","")
        vtxs = cmds.polyEvaluate(sel, v=True)
        ntotVtxs = vtxs/njoints
        closestPoints = []
        #print jntPos
        #for i in xrange(vtxs):
        for i in range(500):
            vtx = (sel+".vtx["+str(i)+"]")
            print " "
            print vtx
            if cmds.progressBar(progressControl, query = True, isCancelled = True):
                break
            #if i%2 == 1:
            ppos = []
            ppos = cmds.xform((sel+".vtx["+str(i)+"]"), q = True, ws = True, t = True)
            newpos = [ppos[0] - jntPos[0], ppos[1] - jntPos[1], ppos[2] - jntPos[2]]
            res = mag(newpos)
            cmds.text(stat, edit=True, label = (str(i)+"/"+str(vtxs)))
            skinJointsList = maya.mel.eval('skinPercent -query -transform %(scluster)s %(vtx)s' %vars())
            # ToDo: skinCluster conversion\
            trackers = []
            weights = []
            newjnt = []
            cpStra = 'pointConstraint -mo '
            cpStrb = ''
            for obj in skinJointsList:
                transform = obj
                joints = (obj+".vtx["+str(i)+"]JNT")
                skinValue = maya.mel.eval('skinPercent -transform %(transform)s -query -value %(scluster)s %(vtx)s' %vars())
                #print ("DEBUG: "+str(transform)+" VALUE: "+str(skinValue))
                if (res <= dist):
                    newjnt = cmds.joint(n = (obj+".vtx["+str(i)+"]JNT"),p = ppos)
                    cmds.setAttr((newjnt+'.radius'),.05)
                    cmds.parent(newjnt, clothRigGrp)
                    trackers.append(obj)
                    weights.append(skinValue)
            if len(trackers) > 0:
                print trackers
                print weights
                        #print trackers
                        #print weights
            #cmds.pointConstraint(trackers, newjnt, mo = True)
                #cpStra+= ('%(trackers)s ')
                #cpStrj= ('%(joints)s ')
                #cpStrb+= ('%(weights)s ')
            #print(cpStra+cpStrj)
            #print trackers
            #print weights

            cmds.progressBar(progressControl, edit = True, step = 1)
            '''

    # Abc code
    def abc_import(self, mode='Import', namespace='', file_path=''):
        cmdStr = ''
        # Import
        if mode == 'Import':
            cmds.file(file_path, i=True, type='Alembic', ignoreVersion=True, gl=True, rpr=namespace)

        # Reference
        if mode == 'Reference':
            cmds.file(file_path, r=True, type='Alembic', ignoreVersion=True, gl=True, rpr=namespace)

    def foo(self):
        pass