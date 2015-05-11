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
import maya.OpenMaya as om

class kObj(object):

    # Define an abstract class obj for kobj
    ABSTRACT_TAG = "__ABSTRACT__"

    # Define kobj as abstract
    KOBJ = ABSTRACT_TAG

    def __init__(self, name=None):
        self.kobj_name = name