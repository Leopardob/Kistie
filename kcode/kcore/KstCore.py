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

class KstCore(object):
    def __init__(self):
        pass

    def get_mobject_from_name(self, node_name):
        '''
        Desc:
        Get API MObject pointer from node name

        Parameter:
        node_name: object name that you want MObject pointer from

        Return MObject pointer or MObject pointers list
        '''

        # Define a variable for MSelectionList
        selection_list = OpenMaya.MSelectionList()

        # Add an empty MObject for DependencyNode get function
        mobject_node = OpenMaya.MObject()

        # Check if node_name is an array
        if isinstance(node_name, list):

            # Define an empty list
            mobject_list = []

            # Loop throught all input objects
            for mobject in mobject_list:
                # Add current objecy to current MSelectionList
                selection_list.add(mobject)

                # Dependency node get function
                selection_list.getDependNode(mobject_node)

                # Append current MObject to the list and return
                mobject_list.append(mobject_node)
            return mobject_list
        else:
            # Add current node_name to MSelectionList, with exceptions otherwise crash
            try:
                selection_list.add(node_name)
            except:
                return None

            # Dependency node get function and return
            selection_list.getDependNode(0, mobject_node)
            return mobject_node

    def get_dag_from_node_name(self, node_name):
        '''
        Desc:
        Get DAG object from node name

        Parameter:
        mobject: object name that you want DAG name from

        Return DagPath string
        '''

        # Define a variable for MSelectionList
        selection_list = OpenMaya.MSelectionList()

        # Add current node_name to MSelectionList, with exceptions otherwise crash
        try:
            selection_list.add(node_name)
        except:
            return None

        # Define a var for DagPath object
        dag_path = OpenMaya.MDagPath()

        # Get current DagPath from selection list
        selection_list.getDagPath(0, dag_path)

        # Return DagPath
        return dag_path

    def get_dag_from_mobject(self, mobject):
        '''
        Desc:
        Get DAG object from MObject pointer

        Parameter:
        mobject: MObject pointer that you want DAG name from

        Return DagPath string
        '''

        # Check if MObject mobject is valid
        if OpenMaya.MObject.hasFn(mobject, OpenMaya.MFn.kDagNode):
            dag_path = OpenMaya.MDagPath()
            OpenMaya.MDagPath.getAPathTo(mobject, dag_path)

            return dag_path