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

# Import kstMaya
import kcode.kcore.KstMaya as kstMaya
reload(kstMaya)
kstMaya=kstMaya.kstMaya()

# Import kstRig
import kcode.krig.KstRig as kstRig
reload(kstRig)
kstRig=kstRig.kstRig()

class MDR_Rig(object):
    def __init__(self):
        self.debug('MDR_Rig module loaded...')

    # Debug method for rig
    def debug(self, message):
        '''
        Desc:
        Make a debug message with description

        Parameter:
        message = str('whatever message')

        Return: None
        '''
        print('[Kistie Rig module MDR]: '+str(message))

    def renameDeformedShape(self):
        '''
        Desc:
        Rename shapes in according to Sanity Check

        Parameter: None

        Return None
        '''
        selected = cmds.ls(sl=True, dag=True, shapes=True)
        for sel in selected:
            if 'Deformed' in sel:
                self.debug('Processing objec: '+str(sel))
                name=sel.split('_',-1)
                end='_'+name[1]+'_'+name[2]+'_DMSH01Shape'
                newName=name[0]+'Deformed'+end
                try:
                    cmds.rename(sel, newName)
                except:
                    self.debug('Skip object: '+str(sel))
                self.debug('Object '+str(sel)+' renamed to '+str(newName))

    def doRig(self, mode='static'):
        '''
        Desc:
        Do the automatic rig for each part of boat 'static', 'ropes', 'deformed'

        Parameter:
        mode = define the mode for the autorig

        Return: None
        '''
        # Procedure that attach all static object to main control
        if mode=='static':
            # Parent static object to ship HOOK
            staticObjects=['static_C_001_GRUP', 'mast_C_005_GRUP', 'mast_C_004_GRUP', 'mast_C_003_GRUP','mast_C_002_GRUP','rutter_C_001_GRUP']
            kstRig.constraintObjectTo('boatHook_C_001_GRUP', staticObjects, 'parent', True)
            self.debug('Static object attached')

            '''
            # Delete autorig guides
            mastGrp=cmds.ls('MASTRIG_GRUP')
            children=cmds.listRelatives(mastGrp, c=True)
            for c in children:
                cc=cmds.listRelatives(c, c=True)
                for d in cc:
                    if cmds.nodeType(d)!='joint':
                        cmds.delete(d)
            self.debug('Autorig guides deleted')

            # Delete unused constraint
            cnstrToDelete=cmds.ls('*_TRAN*_PACN')
            for cnstr in cnstrToDelete:
                cmds.delete(cnstr)
            self.debug('Unused constraints deleted')

            # Show local axis for joints
            joints=cmds.ls('*_JOIN')
            for jnt in joints:
                cmds.setAttr(jnt+'.displayLocalAxis',1)
            self.debug('Local axis visibility activated')

            # Attach controls to Joint
            mastCtrls=cmds.ls('MAST*CTRL')
            for mast in mastCtrls:
                yard=mast.replace('_MAST','_YARD').replace('_CTRL','_JOIN')
                kstMaya.makeConstraint(mast, yard, 'parent', True)
            self.debug('Anim controls attacched to the joints')

        elif mode=='ropes':
            pass
            '''

    def createTag(self, obj, tagValue='UNTAGGED'):
        '''
        Desc:
        Create rig tag for filters mesh and skin based on tag

        Parameter:
        obj = current object
        tagValue = current tag filter, if still UNTAGGED, the current mesh, will be out of filter

        Return: None
        '''
        cmds.addAttr(obj, longName='RigTag', dt="string")
        cmds.setAttr(obj+'.RigTag', str(tagValue), type="string", k=True, e=True)

    def createRopesRig(self, name, ropeType='4anchorPoints'):
        '''
        Desc:
        Create ropes rig

        Parameter:
        name = name of the final rope group
        numberOfRopes = number of ropes
        mirror = True if you want make mirror controls

        Return: rope group ropeGroup
        '''

        # Create rope group
        ropeGroup=cmds.group(em=True, n=name+'Rig_C_001_GRUP')

        # Create manipulator controls
        if ropeType=='2anchorPoints':
            # Single rope creation
            ropeBottom = kstRig.createAnimControl(controlName=(name+'_C_001'), controlType='sphere', pos=[0,-15,0], vector=[0,1,0], size=5, transformOnTop=True)
            cmds.setAttr(ropeBottom[0]+'.displayHandle',1)
            locatorBottom = kstRig.createMayaObject('locator', name=name+'_C_001', parent=ropeBottom[1])
            jointBottom = kstRig.createJoint(pos=[0,0,0], name=name+'_C_001', showAxis=True)
            jointBottomEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_C_002', showAxis=True)
            cmds.xform(locatorBottom, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            ropeTop = kstRig.createAnimControl(controlName=(name+'_C_002'), controlType='sphere', pos=[0,15,0], vector=[0,1,0], size=5, transformOnTop=True)
            locatorTop = kstRig.createMayaObject('locator', name=name+'_C_002', parent=ropeTop[1])
            jointTop = kstRig.createJoint(pos=[0,0,0], name=name+'_C_002', showAxis=True)
            jointTopEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_C_003', showAxis=True)
            cmds.xform(locatorTop, t=[0,0,0], ro=[0,0,0], s=[1,1,1])

            # Create ropes line
            ropeCurve=kstRig.createLineFrom2Obj(name+'_L_001', ropeTop[1], ropeBottom[1])

            # Parent ropes to rope group
            cmds.parent(ropeTop[0], ropeGroup)
            cmds.parent(ropeBottom[0], ropeGroup)
            cmds.parent(ropeCurve, ropeGroup)

            # Create AIM constraint
            aimCstrBottom=kstMaya.makeConstraint(locatorTop, jointBottom, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])
            aimCstrTop=kstMaya.makeConstraint(locatorBottom, jointTop, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])

            return ropeGroup


        if ropeType=='3anchorPoints':
            # Left rope creation
            ropeLBottom = kstRig.createAnimControl(controlName=(name+'_L_001'), controlType='sphere', pos=[5,-15,0], vector=[0,1,0], size=5, transformOnTop=True)
            cmds.setAttr(ropeLBottom[0]+'.displayHandle',1)
            locatorLBottom = kstRig.createMayaObject('locator', name=name+'_L_001', parent=ropeLBottom[1])
            jointLBottom = kstRig.createJoint(pos=[0,0,0], name=name+'_L_001', showAxis=True)
            jointLBottomEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_L_002', showAxis=True)
            cmds.xform(locatorLBottom, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            ropeTop = kstRig.createAnimControl(controlName=(name+'_C_001'), controlType='sphere', pos=[0,15,0], vector=[0,1,0], size=5, transformOnTop=True)
            locatorTop = kstRig.createMayaObject('locator', name=name+'_C_002', parent=ropeTop[1])
            jointTop = kstRig.createJoint(pos=[0,0,0], name=name+'_C_002', showAxis=True)
            cmds.xform(locatorTop, t=[0,0,0], ro=[0,0,0], s=[1,1,1])

            # R
            ropeRBottom = kstRig.createAnimControl(controlName=(name+'_R_001'), controlType='sphere', pos=[-5,-15,0], vector=[0,1,0], size=5, transformOnTop=True)
            cmds.setAttr(ropeRBottom[0]+'.displayHandle',1)
            locatorRBottom = kstRig.createMayaObject('locator', name=name+'_R_001', parent=ropeRBottom[1])
            jointRBottom = kstRig.createJoint(pos=[0,0,0], name=name+'_R_001', showAxis=True)
            jointRBottomEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_R_002', showAxis=True)
            cmds.xform(locatorRBottom, t=[0,0,0], ro=[0,0,0], s=[1,1,1])

            # Create ropes line
            ropeLCurve=kstRig.createLineFrom2Obj(name+'_L_001', ropeTop[1], ropeLBottom[1])

            # R
            ropeRCurve=kstRig.createLineFrom2Obj(name+'_R_001', ropeTop[1], ropeRBottom[1])

            # Parent ropes to rope group
            cmds.parent(ropeTop[0], ropeGroup)
            cmds.parent(ropeLBottom[0], ropeGroup)
            cmds.parent(ropeLCurve, ropeGroup)

            # R
            cmds.parent(ropeRBottom[0], ropeGroup)
            cmds.parent(ropeRCurve, ropeGroup)

            # Create mirror controls
            kstRig.createMirrorRig(ropeLBottom[0])

            # Create AIM constraint
            aimCstrLBottom=kstMaya.makeConstraint(locatorTop, jointLBottom, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])
            aimCstrRBottom=kstMaya.makeConstraint(locatorTop, jointRBottom, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])

            return ropeGroup

        if ropeType=='4anchorPoints':
            # Left rope creation
            ropeLBottom = kstRig.createAnimControl(controlName=(name+'_L_001'), controlType='sphere', pos=[5,-15,0], vector=[0,1,0], size=5, transformOnTop=True)
            cmds.setAttr(ropeLBottom[0]+'.displayHandle',1)
            locatorLBottom = kstRig.createMayaObject('locator', name=name+'_L_001', parent=ropeLBottom[1])
            jointLBottom = kstRig.createJoint(pos=[0,0,0], name=name+'_L_001', showAxis=True)
            jointLBottomEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_L_002', showAxis=True)
            cmds.xform(locatorLBottom, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            ropeLTop = kstRig.createAnimControl(controlName=(name+'_L_002'), controlType='sphere', pos=[5,15,0], vector=[0,1,0], size=5, transformOnTop=True)
            locatorLTop = kstRig.createMayaObject('locator', name=name+'_L_002', parent=ropeLTop[1])
            jointLTop = kstRig.createJoint(pos=[0,0,0], name=name+'_L_002', showAxis=True)
            jointLTopEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_L_003', showAxis=True)
            cmds.xform(locatorLTop, t=[0,0,0], ro=[0,0,0], s=[1,1,1])

            # R
            ropeRBottom = kstRig.createAnimControl(controlName=(name+'_R_001'), controlType='sphere', pos=[-5,-15,0], vector=[0,1,0], size=5, transformOnTop=True)
            cmds.setAttr(ropeRBottom[0]+'.displayHandle',1)
            locatorRBottom = kstRig.createMayaObject('locator', name=name+'_R_001', parent=ropeRBottom[1])
            jointRBottom = kstRig.createJoint(pos=[0,0,0], name=name+'_R_001', showAxis=True)
            jointRBottomEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_R_002', showAxis=True)
            cmds.xform(locatorRBottom, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            ropeRTop = kstRig.createAnimControl(controlName=(name+'_R_002'), controlType='sphere', pos=[-5,15,0], vector=[0,1,0], size=5, transformOnTop=True)
            locatorRTop = kstRig.createMayaObject('locator', name=name+'_R_002', parent=ropeRTop[1])
            jointRTop = kstRig.createJoint(pos=[0,0,0], name=name+'_R_002', showAxis=True)
            jointRTopEnd = kstRig.createJoint(pos=[0,1,0], name=name+'_R_003', showAxis=True)
            cmds.xform(locatorRTop, t=[0,0,0], ro=[0,0,0], s=[1,1,1])

            # Create ropes line
            ropeLCurve=kstRig.createLineFrom2Obj(name+'_L_001', ropeLTop[1], ropeLBottom[1])

            # R
            ropeRCurve=kstRig.createLineFrom2Obj(name+'_R_001', ropeRTop[1], ropeRBottom[1])

            # Parent ropes to rope group
            cmds.parent(ropeLTop[0], ropeGroup)
            cmds.parent(ropeLBottom[0], ropeGroup)
            cmds.parent(ropeLCurve, ropeGroup)

            # R
            cmds.parent(ropeRTop[0], ropeGroup)
            cmds.parent(ropeRBottom[0], ropeGroup)
            cmds.parent(ropeRCurve, ropeGroup)

            # Create mirror controls
            kstRig.createMirrorRig(ropeLBottom[0])
            kstRig.createMirrorRig(ropeLTop[0])

            # Create AIM constraint
            aimCstrLBottom=kstMaya.makeConstraint(locatorLTop, jointLBottom, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])
            aimCstrRBottom=kstMaya.makeConstraint(locatorRTop, jointRBottom, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])
            aimCstrLBottom=kstMaya.makeConstraint(locatorLBottom, jointLTop, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])
            aimCstrRBottom=kstMaya.makeConstraint(locatorRBottom, jointRTop, 'aim', False, 1.0, [0,1,0], [0,0,1], 'vector', [1,0,0])

            return ropeGroup

        else:
            self.debug('This anchor point number is not valid, can be 2, 3 or 4, double check please !!!')
            cmds.delete(ropeGroup)
            return None

    def setYardLimit(self, selections, limit):
        '''
        Desc:
        Set rotation limit for the mast

        Parameter:
        selections = list of object to limit
        limit = angle

        Return: None
        '''
        for sel in selections:
            cmds.transformLimits(sel, ry=[-limit,limit], ery=[1,1])

    def addAttribForSails(self):
        '''
        Desc:
        Add Attributes for sails
        '''
        selections = cmds.ls('*MAST*_*CTRL*')
        for sel in selections:
            if cmds.nodeType(sel)=='transform':
                # Add separator
                cmds.addAttr(sel, ln='CSTATTR', at='enum', en="___________:")
                cmds.setAttr(sel+'.CSTATTR', e=True, keyable=True)
                cmds.setAttr(sel+'.CSTATTR', lock=True, keyable=True)

                # Add sail roll attrib
                cmds.addAttr(sel, ln='Sail', at='enum', en="Up:Down")
                cmds.setAttr(sel+'.Sail', e=True, keyable=True)

    def importDynCache(self, currentSet='Sail_A', variation='VarA', cachePath=''): # ToDo: implement twin sails (A=a,B=b,C=c) / Change code for work with reference
        # Modified for works on library directory
        '''
        Desc:
        Import dynCache from cloth for sails/flag

        Parameter:
        currentSet = sets for sail or flag
        type = type, can be or sail or flag
        cachePath = alembic simulation path
        '''
        import os

        toCheck=''
        cacheList=[]

        # Define top controller for parent cache grp and pass sanity check
        checkTopGrp='top_C_001_CTRL'
        if cmds.objExists(checkTopGrp):
            topCtl=checkTopGrp
        else:
            self.debug('No top GRUP in this scene')

        if currentSet=='Sail_A':
            toCheck='SAIA01'
        elif currentSet=='Sail_B':
            toCheck='SAIB01'
        elif currentSet=='Sail_C':
            toCheck='SAIC01'
        elif currentSet=='Sail_D1':
            toCheck='SAID01'
        elif currentSet=='Sail_D2':
            toCheck='SAID02'
        elif currentSet=='Sail_D3':
            toCheck='SAID03'
        elif currentSet=='Sail_E':
            toCheck='SAIE01'
        elif currentSet=='Sail_F':
            toCheck='SAIF01'
        elif currentSet=='Flag_1':
            toCheck='FLGT01'
        elif currentSet=='Flag_2':
            toCheck='FLGT02'
        elif currentSet=='Flag_3':
            toCheck='FLGT03'
        elif currentSet=='Flag_4':
            toCheck='FLGT04'
        elif currentSet=='Flag_5':
            toCheck='FLGT05'
        else:
            toCheck=None
            self.debug('DEBUG ERROR on Sail SET description')

        # Check in the given path all .abc, and put in a list
        if(toCheck):
            for root, dirs, files in os.walk(cachePath):
                for file in files:
                    if 'cloth' in file and file.endswith('.abc'):
                        if toCheck in os.path.join(root, file) and variation in os.path.join(root, file):
                            #print('CURRENT FILE: ',root, file) # Added
                            buffer=os.path.join(root).split('/v')
                            versions=os.listdir(os.path.join(buffer[0]))
                            sortedVersion=sorted(versions, reverse=True)
                            fixBasePath=os.path.join(buffer[0],sortedVersion[0],'abc','fix-base',file)
                            retakeFixPath=os.path.join(buffer[0],sortedVersion[0],'abc','retakeFix-base',file)

                            # Store current version
                            if os.path.exists(fixBasePath):
                                #print('Current version: ', fixBasePath)
                                cacheList.append(fixBasePath)

                            # Store retake version
                            if os.path.exists(retakeFixPath):
                                #print('Retake version: ', retakeFixPath)
                                cacheList.append(retakeFixPath)

        # Remove duplicated from the list
        cacheListNoDup=set(cacheList)

        '''
        for cache in cacheListNoDup:
            print('DEBUG CURRENT CACHE: ', cache)
        '''

        # Load cloth .abc in Maya scene
        i=1

        # Create a name for variation
        tempBuff=(currentSet+variation).split('_',1)
        identifier=tempBuff[0]+tempBuff[1]

        # Make first letter lower for sanity check pass...
        identifier=identifier[0].lower()+identifier[1:]

        # Make empty group for cloth cache parenting
        clothCacheStorage='clothCacheStorage_C_001_GRUP'
        if not cmds.objExists(clothCacheStorage):
            clothCacheGrp=cmds.group(em=True, n=clothCacheStorage)
        else:
            clothCacheGrp=clothCacheStorage

        # Create a group for control all sails BS and test if exist (will use the existing) or not (will create a newone)
        BSGroupName='cacheBSCtls_C_001_GRUP'
        if cmds.objExists(BSGroupName):
            BS=BSGroupName
        else:
            # Create blendShape group and lock all attrs
            BS=cmds.group(em=True, n=BSGroupName)
            attrs=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
            for attr in attrs:
                cmds.setAttr(BS+attr, k=False)

            # Add separator for blendShape list
            cmds.addAttr(BS, ln='CACHELIST', at='enum', en="___________:")
            cmds.setAttr(BS+'.CACHELIST', e=True, keyable=True)
            cmds.setAttr(BS+'.CACHELIST', lock=True, keyable=True)

        # Dictionary for twin sails

        twinSail=\
        {\
            # Sail_A -> Sail_a
            'ropeSail_C_001_DMSH':'ropeSail_C_002_DMSH','sailSail_C_003_DMSH':'sailSail_C_005_DMSH','ropeSail_L_016_DMSH':'ropeSail_L_022_DMSH','ropeSail_L_017_DMSH':'ropeSail_L_023_DMSH',\
            'handleSail_L_014_DMSH':'handleSail_L_022_DMSH','knotSail_L_015_DMSH':'knotSail_L_019_DMSH','handleSail_L_002_DMSH':'handleSail_L_059_DMSH','knotSail_L_005_DMSH':'knotSail_L_055_DMSH',\
            'ropeSail_L_282_DMSH':'ropeSail_L_133_DMSH','pulleyRopeSail_L_018_DMSH':'pulleyRopeSail_L_005_DMSH','pulleySail_L_014_DMSH':'pulleySail_L_001_DMSH','ropeSail_L_281_DMSH':'ropeSail_L_278_DMSH',\
            'ropeSail_L_283_DMSH':'ropeSail_L_277_DMSH','ropePegSail_L_002_DMSH':'ropePegSail_L_001_DMSH','ropeSail_R_013_DMSH':'ropeSail_R_028_DMSH','ropeSail_R_014_DMSH':'ropeSail_R_029_DMSH',\
            'handleSail_R_002_DMSH':'handleSail_R_011_DMSH','knotSail_R_012_DMSH':'knotSail_R_016_DMSH','handleSail_R_003_DMSH':'handleSail_R_012_DMSH','knotSail_R_014_DMSH':'knotSail_R_021_DMSH',\
            'ropeSail_R_483_DMSH':'ropeSail_R_486_DMSH','pulleyRopeSail_R_018_DMSH':'pulleyRopeSail_R_005_DMSH','pulleySail_R_016_DMSH':'pulleySail_R_002_DMSH','ropeSail_R_481_DMSH':'ropeSail_R_485_DMSH',\
            'ropeSail_R_482_DMSH':'ropeSail_R_484_DMSH','ropePegSail_R_002_DMSH':'ropePegSail_R_001_DMSH','ropeSail_L_019_DMSH':'ropeSail_L_025_DMSH','ropeSail_L_014_DMSH':'ropeSail_L_020_DMSH',\
            'handleSail_L_018_DMSH':'handleSail_L_026_DMSH','knotSail_L_013_DMSH':'knotSail_L_017_DMSH','pulleySail_L_085_DMSH':'pulleySail_L_080_DMSH','pulleySail_L_008_DMSH':'pulleySail_L_017_DMSH',\
            'pulleySail_L_083_DMSH':'pulleySail_L_082_DMSH','pulleySail_L_006_DMSH':'pulleySail_L_015_DMSH','ropeSail_L_018_DMSH':'ropeSail_L_024_DMSH','ropeSail_L_015_DMSH':'ropeSail_L_021_DMSH',\
            'handleSail_L_015_DMSH':'handleSail_L_025_DMSH','knotSail_L_014_DMSH':'knotSail_L_018_DMSH','pulleySail_L_086_DMSH':'pulleySail_L_079_DMSH','pulleySail_L_009_DMSH':'pulleySail_L_018_DMSH',\
            'pulleySail_L_084_DMSH':'pulleySail_L_081_DMSH','pulleySail_L_007_DMSH':'pulleySail_L_016_DMSH','ropeSail_R_016_DMSH':'ropeSail_R_030_DMSH','ropeSail_R_011_DMSH':'ropeSail_R_026_DMSH',\
            'pulleySail_R_074_DMSH':'pulleySail_R_070_DMSH','pulleySail_R_010_DMSH':'pulleySail_R_019_DMSH','pulleySail_R_072_DMSH':'pulleySail_R_061_DMSH','pulleySail_R_008_DMSH':'pulleySail_R_017_DMSH',\
            'handleSail_R_010_DMSH':'handleSail_R_014_DMSH','knotSail_R_011_DMSH':'knotSail_R_015_DMSH','ropeSail_R_025_DMSH':'ropeSail_R_031_DMSH','ropeSail_R_012_DMSH':'ropeSail_R_027_DMSH','handleSail_R_005_DMSH':'handleSail_R_013_DMSH',\
            'knotSail_R_013_DMSH':'knotSail_R_020_DMSH','pulleySail_R_075_DMSH':'pulleySail_R_067_DMSH','pulleySail_R_007_DMSH':'pulleySail_R_020_DMSH','pulleySail_R_073_DMSH':'pulleySail_R_071_DMSH','pulleySail_R_009_DMSH':'pulleySail_R_018_DMSH',\

            # Sail_B -> Sail_b
            'sailSail_C_002_DMSH':'sailSail_C_012_DMSH','ropeSail_L_035_DMSH':'ropeSail_L_044_DMSH','knotSail_L_032_DMSH':'knotSail_L_028_DMSH','handleSail_L_030_DMSH':'handleSail_L_036_DMSH','ropeSail_R_042_DMSH':'ropeSail_R_051_DMSH','knotSail_R_019_DMSH':'knotSail_R_032_DMSH',\
            'handleSail_R_028_DMSH':'handleSail_R_034_DMSH','ropeSail_C_030_DMSH':'ropeSail_C_032_DMSH','ropeSail_L_038_DMSH':'ropeSail_L_047_DMSH','ropeSail_L_032_DMSH':'ropeSail_L_041_DMSH','handleSail_L_033_DMSH':'handleSail_L_043_DMSH','knotSail_L_011_DMSH':'knotSail_L_033_DMSH',\
            'ropeSail_R_036_DMSH':'ropeSail_R_045_DMSH','ropeSail_R_041_DMSH':'ropeSail_R_050_DMSH','handleSail_R_025_DMSH':'handleSail_R_032_DMSH','knotSail_R_018_DMSH':'knotSail_R_031_DMSH','ropeSail_R_035_DMSH':'ropeSail_R_044_DMSH','ropeSail_R_039_DMSH':'ropeSail_R_048_DMSH',\
            'handleSail_R_030_DMSH':'handleSail_R_036_DMSH','knotSail_R_017_DMSH':'knotSail_R_030_DMSH','pulleySail_R_045_DMSH':'pulleySail_R_056_DMSH','pulleySail_R_064_DMSH':'pulleySail_R_049_DMSH','pulleySail_R_046_DMSH':'pulleySail_R_055_DMSH','pulleySail_R_063_DMSH':'pulleySail_R_050_DMSH',\
            'ropeSail_R_034_DMSH':'ropeSail_R_043_DMSH','ropeSail_R_040_DMSH':'ropeSail_R_049_DMSH','ropeSail_R_039_DMSH':'ropeSail_R_048_DMSH','handleSail_R_031_DMSH':'handleSail_R_039_DMSH','knotSail_R_029_DMSH':'knotSail_R_028_DMSH','pulleySail_R_048_DMSH':'pulleySail_R_053_DMSH','pulleySail_R_066_DMSH':'pulleySail_R_052_DMSH',\
            'ropeSail_R_037_DMSH':'ropeSail_R_046_DMSH','ropeSail_R_036_DMSH':'ropeSail_R_045_DMSH','ropeSail_R_034_DMSH':'ropeSail_R_043_DMSH','ropeSail_R_035_DMSH':'ropeSail_R_044_DMSH',
            'pulleySail_R_047_DMSH':'pulleySail_R_054_DMSH','pulleySail_R_068_DMSH':'pulleySail_R_051_DMSH','ropeSail_L_036_DMSH':'ropeSail_L_045_DMSH','ropeSail_L_034_DMSH':'ropeSail_L_043_DMSH','handleSail_L_031_DMSH':'handleSail_L_038_DMSH','knotSail_L_026_DMSH':'knotSail_L_034_DMSH',\
            'pulleySail_L_056_DMSH':'pulleySail_L_067_DMSH','pulleySail_L_072_DMSH':'pulleySail_L_060_DMSH','pulleySail_L_058_DMSH':'pulleySail_L_065_DMSH','pulleySail_L_077_DMSH':'pulleySail_L_062_DMSH','ropeSail_L_037_DMSH':'ropeSail_L_046_DMSH','ropeSail_L_033_DMSH':'ropeSail_L_042_DMSH',\
            'handleSail_L_032_DMSH':'handleSail_L_040_DMSH','knotSail_L_027_DMSH':'knotSail_L_035_DMSH','pulleySail_L_057_DMSH':'pulleySail_L_066_DMSH','pulleySail_L_071_DMSH':'pulleySail_L_061_DMSH','pulleySail_L_059_DMSH':'pulleySail_L_064_DMSH','pulleySail_L_073_DMSH':'pulleySail_L_063_DMSH',\

            # Sail_C -> Sail_c
            'ropeSail_L_050_DMSH':'ropeSail_L_055_DMSH','knotSail_L_046_DMSH':'knotSail_L_048_DMSH','handleSail_L_034_DMSH':'handleSail_L_044_DMSH','ropeSail_R_055_DMSH':'ropeSail_R_060_DMSH','knotSail_R_039_DMSH':'knotSail_R_041_DMSH','handleSail_R_027_DMSH':'handleSail_R_040_DMSH','ropeSail_C_033_DMSH':'ropeSail_C_034_DMSH',\
            'sailSail_C_004_DMSH':'sailSail_C_013_DMSH','ropeSail_R_056_DMSH':'ropeSail_R_061_DMSH','ropeSail_R_052_DMSH':'ropeSail_R_057_DMSH','knotSail_R_038_DMSH':'knotSail_R_040_DMSH','handleSail_R_029_DMSH':'handleSail_R_044_DMSH','pulleySail_R_081_DMSH':'pulleySail_R_040_DMSH','pulleySail_R_086_DMSH':'pulleySail_R_088_DMSH',\
            'pulleySail_R_087_DMSH':'pulleySail_R_039_DMSH','pulleySail_R_080_DMSH':'pulleySail_R_022_DMSH','ropeSail_L_048_DMSH':'ropeSail_L_051_DMSH','ropeSail_L_049_DMSH':'ropeSail_L_054_DMSH','knotSail_L_045_DMSH':'knotSail_L_047_DMSH','handleSail_L_035_DMSH':'handleSail_L_052_DMSH','pulleySail_L_108_DMSH':'pulleySail_L_050_DMSH',\
            'pulleySail_L_089_DMSH':'pulleySail_L_021_DMSH','pulleySail_L_090_DMSH':'pulleySail_L_051_DMSH','pulleySail_L_107_DMSH':'pulleySail_L_109_DMSH'
        }\

        # Check why does not work
        for cache in cacheListNoDup:
            #Check if cache exists
            if os.path.exists(cache):
                print('Current cache >> ', cache)


                # Create a list for all BS types
                BSList=[]

                # Find version from fullBuffer
                fullBuffer=cache.split('/',-1)
                sailType=fullBuffer[9]

                # Add attr to blendShape storage and connect
                cmds.addAttr(BSGroupName, ln=currentSet+'_'+sailType, at='double', min=0, max=1, dv=0)
                cmds.setAttr(BSGroupName+'.'+currentSet+'_'+sailType, e=True, k=True)

                kstMaya.abcImport('Reference', sailType, cache)
                grpToCheck=['wire_C_001_GRUP','toWire_C_001_GRUP','fabric_C_001_GRUP','ropes_C_001_GRUP']
                cacheGrp=cmds.group(em=True, n=sailType+'_clothCache_C_'+str(i).zfill(3)+'_GRUP')
                for grp in grpToCheck:
                    currentGrp=(sailType+'_'+grp)
                    if cmds.objExists(currentGrp):
                        # Cycle throught group and make BS with current geo and original geo
                        children=cmds.listRelatives(currentGrp, c=True)
                        for c in children:
                            currentGeo=c
                            print('> DEBUG CURRENT GEO: ', currentGeo)
                            rigBuffer=c.split('_',1)[1].split('_',1)
                            print('> RIG BUFFER: ', rigBuffer)
                            rigName=(rigBuffer[0]+'Sail')
                            print('> RIGNAME: ', rigName)
                            rigGeo=rigName+'_'+rigBuffer[1]
                            print('> RIG GEO: ', rigGeo)
                            checkName=c.split('_',1)[1]
                            BSName=checkName.replace('_DMSH','_CLBS')

                            # Check if rigGeo contains already a blendShape

                            # List all connections from ffd, because the blendShape if exists should be in frontOfChain # ToDo implement twin shapes this is the correct way ? Boh
                            if rigGeo[-4:]=='DMSH':
                                if rigGeo in twinSail:
                                    twinGeo=twinSail[rigGeo]
                                    shape=cmds.listRelatives(twinGeo, s=True)
                                    currentBS=''
                                    # Original geo
                                    if(shape):
                                        # If Blendshape doesn't exists create
                                        self.debug('Creating BS between '+str(currentGeo)+' >>>>> '+str(twinGeo))
                                        try:
                                            BSNode = cmds.blendShape(currentGeo, twinGeo, frontOfChain=True, n=sailType+'_'+BSName)
                                            kstMaya.nodeOp(BS+'.'+currentSet+'_'+sailType,'>>',BSNode[0]+'.weight[0]')
                                            BSList.append(BSNode)
                                        except:
                                            self.debug('Blendshape creation failed!')
                                    # Twin geo
                                    shape=cmds.listRelatives(rigGeo, s=True)
                                    currentBS=''
                                    if(shape):
                                        # If Blendshape doesn't exists create
                                        self.debug('Creating BS between '+str(currentGeo)+' >>>>> '+str(rigGeo))
                                        try:
                                            BSNode = cmds.blendShape(currentGeo, rigGeo, frontOfChain=True, n=sailType+'_'+BSName)
                                            kstMaya.nodeOp(BS+'.'+currentSet+'_'+sailType,'>>',BSNode[0]+'.weight[0]')
                                            BSList.append(BSNode)
                                        except:
                                            self.debug('Blendshape creation failed!')
                                else:
                                    shape=cmds.listRelatives(rigGeo, s=True)
                                    currentBS=''
                                    if(shape):
                                        # If Blendshape doesn't exists create
                                        self.debug('Creating BS between '+str(currentGeo)+' >>>>> '+str(rigGeo))
                                        try:
                                            BSNode = cmds.blendShape(currentGeo, rigGeo, frontOfChain=True, n=sailType+'_'+BSName)
                                            kstMaya.nodeOp(BS+'.'+currentSet+'_'+sailType,'>>',BSNode[0]+'.weight[0]')
                                            BSList.append(BSNode)
                                        except:
                                            self.debug('Blendshape creation failed!')
                            else:
                                print('Skipped Object: ', rigGeo)

                        # Parent current grp to cache grp
                        cmds.parent(currentGrp, cacheGrp)
                print('DEBUG BS LIST: ', BSList)
                # Parent cacheGrp type to cloth cache grp
                cmds.parent(cacheGrp, clothCacheGrp)
                i=i+1
            else:
                self.debug('CACHE DOES NOT EXISTS: '+str(cache))

        # Parent clothCacheGrp under top_C_001_CTRL for Sanity check
        try:
            cmds.parent(clothCacheGrp, checkTopGrp)
        except:
            pass

    def importDynCache2(self, currentSet='Sail_A', variation='VarA', cachePath=''): # ToDo: implement twin sails (A=a,B=b,C=c) / Change code for work with reference
        # Modified for works on library directory
        '''
        Desc:
        Import dynCache from cloth for sails/flag

        Parameter:
        currentSet = sets for sail or flag
        type = type, can be or sail or flag
        cachePath = alembic simulation path
        '''
        import os

        toCheck=''
        cacheList=[]

        # Define top controller for parent cache grp and pass sanity check
        checkTopGrp='top_C_001_CTRL'
        if cmds.objExists(checkTopGrp):
            topCtl=checkTopGrp
        else:
            self.debug('No top GRUP in this scene')

        if currentSet=='Sail_A':
            toCheck='SAIA01'
        elif currentSet=='Sail_B':
            toCheck='SAIB01'
        elif currentSet=='Sail_C':
            toCheck='SAIC01'
        elif currentSet=='Sail_D1':
            toCheck='SAID01'
        elif currentSet=='Sail_D2':
            toCheck='SAID02'
        elif currentSet=='Sail_D3':
            toCheck='SAID03'
        elif currentSet=='Sail_E':
            toCheck='SAIE01'
        elif currentSet=='Sail_F':
            toCheck='SAIF01'
        elif currentSet=='Flag_1':
            toCheck='FLGT01'
        elif currentSet=='Flag_2':
            toCheck='FLGT02'
        elif currentSet=='Flag_3':
            toCheck='FLGT03'
        elif currentSet=='Flag_4':
            toCheck='FLGT04'
        elif currentSet=='Flag_5':
            toCheck='FLGT05'
        else:
            toCheck=None
            self.debug('DEBUG ERROR on Sail SET description')

        # Check in the given path all .abc, and put in a list
        if(toCheck):
            for root, dirs, files in os.walk(cachePath):
                for file in files:
                    if 'cloth' in file and file.endswith('.abc'):
                        if toCheck in os.path.join(root, file) and variation in os.path.join(root, file):
                            fixBasePath=os.path.join(root, file)

                            # Store current version
                            if os.path.exists(fixBasePath):
                                #print('Current version: ', fixBasePath)
                                cacheList.append(fixBasePath)

        # Remove duplicated from the list
        cacheListNoDup=set(cacheList)

        '''
        for cache in cacheListNoDup:
            print('DEBUG CURRENT CACHE: ', cache)

        '''
        # Load cloth .abc in Maya scene
        i=1

        # Create a name for variation
        tempBuff=(currentSet+variation).split('_',1)
        identifier=tempBuff[0]+tempBuff[1]

        # Make first letter lower for sanity check pass...
        identifier=identifier[0].lower()+identifier[1:]

        # Make empty group for cloth cache parenting
        clothCacheStorage='clothCacheStorage_C_001_GRUP'
        if not cmds.objExists(clothCacheStorage):
            clothCacheGrp=cmds.group(em=True, n=clothCacheStorage)
        else:
            clothCacheGrp=clothCacheStorage

        # Create a group for control all sails BS and test if exist (will use the existing) or not (will create a newone)
        BSGroupName='cacheBSCtls_C_001_GRUP'
        if cmds.objExists(BSGroupName):
            BS=BSGroupName
        else:
            # Create blendShape group and lock all attrs
            BS=cmds.group(em=True, n=BSGroupName)
            attrs=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
            for attr in attrs:
                cmds.setAttr(BS+attr, k=False)

            # Add separator for blendShape list
            cmds.addAttr(BS, ln='CACHELIST', at='enum', en="___________:")
            cmds.setAttr(BS+'.CACHELIST', e=True, keyable=True)
            cmds.setAttr(BS+'.CACHELIST', lock=True, keyable=True)

        # Check why does not work
        for cache in cacheListNoDup:
            #Check if cache exists
            if os.path.exists(cache):
                print('Current cache >> ', cache)


                # Create a list for all BS types
                BSList=[]

                # Find version from fullBuffer
                fullBuffer=cache.split('/',-1)
                sailType=fullBuffer[9]

                # Add attr to blendShape storage and connect
                cmds.addAttr(BSGroupName, ln=currentSet+'_'+sailType, at='double', min=0, max=1, dv=0)
                cmds.setAttr(BSGroupName+'.'+currentSet+'_'+sailType, e=True, k=True)

                kstMaya.abcImport('Reference', sailType, cache)
                grpToCheck=['wire_C_001_GRUP','toWire_C_001_GRUP','fabric_C_001_GRUP','ropes_C_001_GRUP']
                cacheGrp=cmds.group(em=True, n=sailType+'_clothCache_C_'+str(i).zfill(3)+'_GRUP')
                for grp in grpToCheck:
                    currentGrp=(sailType+'_'+grp)
                    if cmds.objExists(currentGrp):
                        # Cycle throught group and make BS with current geo and original geo
                        children=cmds.listRelatives(currentGrp, c=True)
                        for c in children:
                            currentGeo=c
                            print('> DEBUG CURRENT GEO: ', currentGeo)
                            rigBuffer=c.split('_',1)[1].split('_',1)
                            print('> RIG BUFFER: ', rigBuffer)
                            rigName=(rigBuffer[0]+'Sail')
                            print('> RIGNAME: ', rigName)
                            rigGeo=rigName+'_'+rigBuffer[1]
                            print('> RIG GEO: ', rigGeo)
                            checkName=c.split('_',1)[1]
                            BSName=checkName.replace('_DMSH','_CLBS')

                            # Check if rigGeo contains already a blendShape

                            # List all connections from ffd, because the blendShape if exists should be in frontOfChain # ToDo implement twin shapes this is the correct way ? Boh
                            if rigGeo[-4:]=='DMSH':
                                shape=cmds.listRelatives(rigGeo, s=True)
                                currentBS=''
                                if(shape):
                                    # If Blendshape doesn't exists create
                                    self.debug('Creating BS between '+str(currentGeo)+' >>>>> '+str(rigGeo))
                                    try:
                                        BSNode = cmds.blendShape(currentGeo, rigGeo, frontOfChain=True, n=sailType+'_'+BSName)
                                        print('DETAILS: ',BS+'.'+currentSet+'_'+sailType,'>>',BSNode[0]+'.weight[0]')
                                        kstMaya.nodeOp(BS+'.'+currentSet+'_'+sailType,'>>',BSNode[0]+'.weight[0]')
                                        BSList.append(BSNode)
                                    except:
                                        pass
                                        #self.debug('Blendshape creation failed!')
                            else:
                                print('Skipped Object: ', rigGeo)

                        # Parent current grp to cache grp
                        cmds.parent(currentGrp, cacheGrp)
                #print('DEBUG BS LIST: ', BSList)
                # Parent cacheGrp type to cloth cache grp
                cmds.parent(cacheGrp, clothCacheGrp)
                i=i+1
            else:
                self.debug('CACHE DOES NOT EXISTS: '+str(cache))

        # Parent clothCacheGrp under top_C_001_CTRL for Sanity check
        try:
            cmds.parent(clothCacheGrp, checkTopGrp)
        except:
            pass

    def importTwinCache(self, currentSet='Sail_A', variation='VarA', cachePath=''): # ToDo: implement twin sails (A=a,B=b,C=c) / Change code for work with reference
        # Modified for works on library directory
        '''
        Desc:
        Import dynCache from cloth for sails/flag

        Parameter:
        currentSet = sets for sail or flag
        type = type, can be or sail or flag
        cachePath = alembic simulation path
        '''
        import os

        toCheck=''
        cacheList=[]

        # Define top controller for parent cache grp and pass sanity check
        checkTopGrp='top_C_001_CTRL'
        if cmds.objExists(checkTopGrp):
            topCtl=checkTopGrp
        else:
            self.debug('No top GRUP in this scene')

        if currentSet=='Sail_A':
            toCheck='SAIA01'
        elif currentSet=='Sail_B':
            toCheck='SAIB01'
        elif currentSet=='Sail_C':
            toCheck='SAIC01'
        else:
            toCheck=None
            self.debug('DEBUG ERROR on Sail SET description')

        # Check in the given path all .abc, and put in a list
        if(toCheck):
            for root, dirs, files in os.walk(cachePath):
                for file in files:
                    if 'cloth' in file and file.endswith('.abc'):
                        if toCheck in os.path.join(root, file) and variation in os.path.join(root, file):
                            buffer=os.path.join(root).split('/v')
                            versions=os.listdir(os.path.join(buffer[0]))
                            sortedVersion=sorted(versions, reverse=True)
                            fixBasePath=os.path.join(buffer[0],sortedVersion[0],'abc','fix-base',file)
                            retakeFixPath=os.path.join(buffer[0],sortedVersion[0],'abc','retakeFix-base',file)

                            # Store current version
                            if os.path.exists(fixBasePath):
                                print('Current version: ', fixBasePath)
                                cacheList.append(fixBasePath)

                            # Store retake version
                            if os.path.exists(retakeFixPath):
                                print('Retake version: ', retakeFixPath)
                                cacheList.append(retakeFixPath)

        # Remove duplicated from the list
        cacheListNoDup=set(cacheList)

        # Load cloth .abc in Maya scene
        i=1

        # Create a name for variation
        tempBuff=(currentSet+variation).split('_',1)
        identifier=tempBuff[0]+tempBuff[1]

        # Make first letter lower for sanity check pass...
        identifier=identifier[0].lower()+identifier[1:]

        # Make empty group for cloth cache parenting
        clothCacheStorage='clothCacheStorage_C_001_GRUP'
        if not cmds.objExists(clothCacheStorage):
            clothCacheGrp=cmds.group(em=True, n=clothCacheStorage)
        else:
            clothCacheGrp=clothCacheStorage

        # Create a group for control all sails BS and test if exist (will use the existing) or not (will create a newone)
        BSGroupName='twinCacheBSCtls_C_001_GRUP'
        if cmds.objExists(BSGroupName):
            BS=BSGroupName
        else:
            # Create blendShape group and lock all attrs
            BS=cmds.group(em=True, n=BSGroupName)
            attrs=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
            for attr in attrs:
                cmds.setAttr(BS+attr, k=False)

            # Add separator for blendShape list
            cmds.addAttr(BS, ln='CACHELIST', at='enum', en="___________:")
            cmds.setAttr(BS+'.CACHELIST', e=True, keyable=True)
            cmds.setAttr(BS+'.CACHELIST', lock=True, keyable=True)

        # Dictionary for twin sails

        twinSail=\
        {\
            # Sail_A -> Sail_a
            'ropeSail_C_001_DMSH':'ropeSail_C_002_DMSH','sailSail_C_003_DMSH':'sailSail_C_005_DMSH','ropeSail_L_016_DMSH':'ropeSail_L_022_DMSH','ropeSail_L_017_DMSH':'ropeSail_L_023_DMSH',\
            'handleSail_L_014_DMSH':'handleSail_L_022_DMSH','knotSail_L_015_DMSH':'knotSail_L_019_DMSH','handleSail_L_002_DMSH':'handleSail_L_059_DMSH','knotSail_L_005_DMSH':'knotSail_L_055_DMSH',\
            'ropeSail_L_282_DMSH':'ropeSail_L_133_DMSH','pulleyRopeSail_L_018_DMSH':'pulleyRopeSail_L_005_DMSH','pulleySail_L_014_DMSH':'pulleySail_L_001_DMSH','ropeSail_L_281_DMSH':'ropeSail_L_278_DMSH',\
            'ropeSail_L_283_DMSH':'ropeSail_L_277_DMSH','ropePegSail_L_002_DMSH':'ropePegSail_L_001_DMSH','ropeSail_R_013_DMSH':'ropeSail_R_028_DMSH','ropeSail_R_014_DMSH':'ropeSail_R_029_DMSH',\
            'handleSail_R_002_DMSH':'handleSail_R_011_DMSH','knotSail_R_012_DMSH':'knotSail_R_016_DMSH','handleSail_R_003_DMSH':'handleSail_R_012_DMSH','knotSail_R_014_DMSH':'knotSail_R_021_DMSH',\
            'ropeSail_R_483_DMSH':'ropeSail_R_486_DMSH','pulleyRopeSail_R_018_DMSH':'pulleyRopeSail_R_005_DMSH','pulleySail_R_016_DMSH':'pulleySail_R_002_DMSH','ropeSail_R_481_DMSH':'ropeSail_R_485_DMSH',\
            'ropeSail_R_482_DMSH':'ropeSail_R_484_DMSH','ropePegSail_R_002_DMSH':'ropePegSail_R_001_DMSH','ropeSail_L_019_DMSH':'ropeSail_L_025_DMSH','ropeSail_L_014_DMSH':'ropeSail_L_020_DMSH',\
            'handleSail_L_018_DMSH':'handleSail_L_026_DMSH','knotSail_L_013_DMSH':'knotSail_L_017_DMSH','pulleySail_L_085_DMSH':'pulleySail_L_080_DMSH','pulleySail_L_008_DMSH':'pulleySail_L_017_DMSH',\
            'pulleySail_L_083_DMSH':'pulleySail_L_082_DMSH','pulleySail_L_006_DMSH':'pulleySail_L_015_DMSH','ropeSail_L_018_DMSH':'ropeSail_L_024_DMSH','ropeSail_L_015_DMSH':'ropeSail_L_021_DMSH',\
            'handleSail_L_015_DMSH':'handleSail_L_025_DMSH','knotSail_L_014_DMSH':'knotSail_L_018_DMSH','pulleySail_L_086_DMSH':'pulleySail_L_079_DMSH','pulleySail_L_009_DMSH':'pulleySail_L_018_DMSH',\
            'pulleySail_L_084_DMSH':'pulleySail_L_081_DMSH','pulleySail_L_007_DMSH':'pulleySail_L_016_DMSH','ropeSail_R_016_DMSH':'ropeSail_R_030_DMSH','ropeSail_R_011_DMSH':'ropeSail_R_026_DMSH',\
            'pulleySail_R_074_DMSH':'pulleySail_R_070_DMSH','pulleySail_R_010_DMSH':'pulleySail_R_019_DMSH','pulleySail_R_072_DMSH':'pulleySail_R_061_DMSH','pulleySail_R_008_DMSH':'pulleySail_R_017_DMSH',\
            'handleSail_R_010_DMSH':'handleSail_R_014_DMSH','knotSail_R_011_DMSH':'knotSail_R_015_DMSH','ropeSail_R_025_DMSH':'ropeSail_R_031_DMSH','ropeSail_R_012_DMSH':'ropeSail_R_027_DMSH','handleSail_R_005_DMSH':'handleSail_R_013_DMSH',\
            'knotSail_R_013_DMSH':'knotSail_R_020_DMSH','pulleySail_R_075_DMSH':'pulleySail_R_067_DMSH','pulleySail_R_007_DMSH':'pulleySail_R_020_DMSH','pulleySail_R_073_DMSH':'pulleySail_R_071_DMSH','pulleySail_R_009_DMSH':'pulleySail_R_018_DMSH',\

            # Sail_B -> Sail_b
            'sailSail_C_002_DMSH':'sailSail_C_012_DMSH','ropeSail_L_035_DMSH':'ropeSail_L_044_DMSH','knotSail_L_032_DMSH':'knotSail_L_028_DMSH','handleSail_L_030_DMSH':'handleSail_L_036_DMSH','ropeSail_R_042_DMSH':'ropeSail_R_051_DMSH','knotSail_R_019_DMSH':'knotSail_R_032_DMSH',\
            'handleSail_R_028_DMSH':'handleSail_R_034_DMSH','ropeSail_C_030_DMSH':'ropeSail_C_032_DMSH','ropeSail_L_038_DMSH':'ropeSail_L_047_DMSH','ropeSail_L_032_DMSH':'ropeSail_L_041_DMSH','handleSail_L_033_DMSH':'handleSail_L_043_DMSH','knotSail_L_011_DMSH':'knotSail_L_033_DMSH',\
            'ropeSail_R_036_DMSH':'ropeSail_R_045_DMSH','ropeSail_R_041_DMSH':'ropeSail_R_050_DMSH','handleSail_R_025_DMSH':'handleSail_R_032_DMSH','knotSail_R_018_DMSH':'knotSail_R_031_DMSH','ropeSail_R_035_DMSH':'ropeSail_R_044_DMSH','ropeSail_R_039_DMSH':'ropeSail_R_048_DMSH',\
            'handleSail_R_030_DMSH':'handleSail_R_036_DMSH','knotSail_R_017_DMSH':'knotSail_R_030_DMSH','pulleySail_R_045_DMSH':'pulleySail_R_056_DMSH','pulleySail_R_064_DMSH':'pulleySail_R_049_DMSH','pulleySail_R_046_DMSH':'pulleySail_R_055_DMSH','pulleySail_R_063_DMSH':'pulleySail_R_050_DMSH',\
            'ropeSail_R_034_DMSH':'ropeSail_R_043_DMSH','ropeSail_R_040_DMSH':'ropeSail_R_049_DMSH','ropeSail_R_039_DMSH':'ropeSail_R_048_DMSH','handleSail_R_031_DMSH':'handleSail_R_039_DMSH','knotSail_R_029_DMSH':'knotSail_R_028_DMSH','pulleySail_R_048_DMSH':'pulleySail_R_053_DMSH','pulleySail_R_066_DMSH':'pulleySail_R_052_DMSH',\
            'ropeSail_R_037_DMSH':'ropeSail_R_046_DMSH','ropeSail_R_036_DMSH':'ropeSail_R_045_DMSH','ropeSail_R_034_DMSH':'ropeSail_R_043_DMSH','ropeSail_R_035_DMSH':'ropeSail_R_044_DMSH',
            'pulleySail_R_047_DMSH':'pulleySail_R_054_DMSH','pulleySail_R_068_DMSH':'pulleySail_R_051_DMSH','ropeSail_L_036_DMSH':'ropeSail_L_045_DMSH','ropeSail_L_034_DMSH':'ropeSail_L_043_DMSH','handleSail_L_031_DMSH':'handleSail_L_038_DMSH','knotSail_L_026_DMSH':'knotSail_L_034_DMSH',\
            'pulleySail_L_056_DMSH':'pulleySail_L_067_DMSH','pulleySail_L_072_DMSH':'pulleySail_L_060_DMSH','pulleySail_L_058_DMSH':'pulleySail_L_065_DMSH','pulleySail_L_077_DMSH':'pulleySail_L_062_DMSH','ropeSail_L_037_DMSH':'ropeSail_L_046_DMSH','ropeSail_L_033_DMSH':'ropeSail_L_042_DMSH',\
            'handleSail_L_032_DMSH':'handleSail_L_040_DMSH','knotSail_L_027_DMSH':'knotSail_L_035_DMSH','pulleySail_L_057_DMSH':'pulleySail_L_066_DMSH','pulleySail_L_071_DMSH':'pulleySail_L_061_DMSH','pulleySail_L_059_DMSH':'pulleySail_L_064_DMSH','pulleySail_L_073_DMSH':'pulleySail_L_063_DMSH',\

            # Sail_C -> Sail_c
            'ropeSail_L_050_DMSH':'ropeSail_L_055_DMSH','knotSail_L_046_DMSH':'knotSail_L_048_DMSH','handleSail_L_034_DMSH':'handleSail_L_044_DMSH','ropeSail_R_055_DMSH':'ropeSail_R_060_DMSH','knotSail_R_039_DMSH':'knotSail_R_041_DMSH','handleSail_R_027_DMSH':'handleSail_R_040_DMSH','ropeSail_C_033_DMSH':'ropeSail_C_034_DMSH',\
            'sailSail_C_004_DMSH':'sailSail_C_013_DMSH','ropeSail_R_056_DMSH':'ropeSail_R_061_DMSH','ropeSail_R_052_DMSH':'ropeSail_R_057_DMSH','knotSail_R_038_DMSH':'knotSail_R_040_DMSH','handleSail_R_029_DMSH':'handleSail_R_044_DMSH','pulleySail_R_081_DMSH':'pulleySail_R_040_DMSH','pulleySail_R_086_DMSH':'pulleySail_R_088_DMSH',\
            'pulleySail_R_087_DMSH':'pulleySail_R_039_DMSH','pulleySail_R_080_DMSH':'pulleySail_R_022_DMSH','ropeSail_L_048_DMSH':'ropeSail_L_051_DMSH','ropeSail_L_049_DMSH':'ropeSail_L_054_DMSH','knotSail_L_045_DMSH':'knotSail_L_047_DMSH','handleSail_L_035_DMSH':'handleSail_L_052_DMSH','pulleySail_L_108_DMSH':'pulleySail_L_050_DMSH',\
            'pulleySail_L_089_DMSH':'pulleySail_L_021_DMSH','pulleySail_L_090_DMSH':'pulleySail_L_051_DMSH','pulleySail_L_107_DMSH':'pulleySail_L_109_DMSH'
        }\

        # Check why does not work
        for cache in cacheListNoDup:
            #Check if cache exists
            if os.path.exists(cache):
                print('Current cache >> ', cache)

                # Create a list for all BS types
                BSList=[]

                # Find version from fullBuffer
                fullBuffer=cache.split('/',-1)
                sailType=fullBuffer[9]

                # Add attr to blendShape storage and connect
                cmds.addAttr(BSGroupName, ln=currentSet+'_'+sailType, at='double', min=0, max=1, dv=0)
                cmds.setAttr(BSGroupName+'.'+currentSet+'_'+sailType, e=True, k=True)

                kstMaya.abcImport('Reference', sailType, cache)
                grpToCheck=['wire_C_001_GRUP','toWire_C_001_GRUP','fabric_C_001_GRUP','ropes_C_001_GRUP']
                cacheGrp=cmds.group(em=True, n=sailType+'_clothCache_C_'+str(i).zfill(3)+'_GRUP')
                for grp in grpToCheck:
                    currentGrp=(sailType+'_'+grp)
                    if cmds.objExists(currentGrp):
                        # Cycle throught group and make BS with current geo and original geo
                        children=cmds.listRelatives(currentGrp, c=True)
                        for c in children:
                            currentGeo=c
                            print('> DEBUG CURRENT GEO: ', currentGeo)
                            rigBuffer=c.split('_',1)[1].split('_',1)
                            print('> RIG BUFFER: ', rigBuffer)
                            rigName=(rigBuffer[0]+'Sail')
                            print('> RIGNAME: ', rigName)
                            rigGeo=rigName+'_'+rigBuffer[1]
                            print('> RIG GEO: ', rigGeo)
                            checkName=c.split('_',1)[1]
                            BSName=checkName.replace('_DMSH','_CLBS')

                            # Check if rigGeo contains already a blendShape

                            # List all connections from ffd, because the blendShape if exists should be in frontOfChain # ToDo implement twin shapes this is the correct way ? Boh
                            if rigGeo[-4:]=='DMSH':
                                if rigGeo in twinSail:
                                    twinGeo=twinSail[rigGeo]
                                    shape=cmds.listRelatives(twinGeo, s=True)
                                    currentBS=''
                                    # Original geo
                                    if(shape):
                                        # If Blendshape doesn't exists create
                                        self.debug('Creating BS between '+str(currentGeo)+' >>>>> '+str(twinGeo))
                                        try:
                                            BSNode = cmds.blendShape(currentGeo, twinGeo, frontOfChain=True, n=sailType+'_'+BSName)
                                            kstMaya.nodeOp(BS+'.'+currentSet+'_'+sailType,'>>',BSNode[0]+'.weight[0]')
                                            BSList.append(BSNode)
                                        except:
                                            self.debug('Blendshape creation failed!')
                            else:
                                print('Skipped Object: ', rigGeo)

                        # Parent current grp to cache grp
                        cmds.parent(currentGrp, cacheGrp)
                print('DEBUG BS LIST: ', BSList)
                # Parent cacheGrp type to cloth cache grp
                cmds.parent(cacheGrp, clothCacheGrp)
                i=i+1
            else:
                self.debug('CACHE DOES NOT EXISTS: '+str(cache))

        # Parent clothCacheGrp under top_C_001_CTRL for Sanity check
        try:
            cmds.parent(clothCacheGrp, checkTopGrp)
        except:
            pass

    def createDrivenKeys(self, driver, driven): # ToDo deep debug
        '''
        Desc:
        Set driven keys in a superfast way

        Parameter:
        driver = object attribute that drive
        driven = object wich all driven attr
        '''
        currentAttr=cmds.getAttr(driver, asString=True)

        if 'SAIL' in driver:
            attrNameBuffer=currentAttr.split('_')
            driverAttrName=driver.split('.')[1].replace('SAIL','Sail')
            compoundName=attrNameBuffer[0]+attrNameBuffer[1]

        if 'FLAG' in driver:
            compoundName=currentAttr
            driverAttrName=driver.split('.')[1].replace('FLAG','Flag')

        attrInList=cmds.listAttr(driven, k=True)

        for attr in attrInList:
            if compoundName in attr and driverAttrName in attr:
                cmds.setDrivenKeyframe((driven+'.'+attr),cd=driver, v=1)
            elif 'Strong' in compoundName:
                compoundName=compoundName.replace('Strong','Str')
                if compoundName in attr and driverAttrName in attr:
                    cmds.setDrivenKeyframe((driven+'.'+attr),cd=driver, v=1)
            elif 'SideWind' in compoundName:
                compoundName=compoundName.replace('SideWind','WindSide')
                compoundName=compoundName[:9]
                if compoundName in attr and driverAttrName in attr:
                    cmds.setDrivenKeyframe((driven+'.'+attr),cd=driver, v=1)
            else:
                cmds.setDrivenKeyframe((driven+'.'+attr),cd=driver, v=0)

    def connectSailCacheAttr(self, sailType, currentControl): # ToDo deep debug
        '''
        Desc:
        Set driven keys in a superfast way

        Parameter:
        sailType = sail type ex (SAIL_A, SAIL_B, SAIL_C...)
        currentControl = current wind control CTRL
        '''
        currentAttr=cmds.attributeQuery(sailType, node=currentControl, listEnum=True)
        print('DEBUG CURRENT ATTR: ', currentAttr)
        currentAttrBuffer=currentAttr[0].split(':',-1)
        for i in range(0,len(currentAttrBuffer)-1):
            cmds.setAttr(currentControl+'.'+sailType,i)
            self.createDrivenKeys(currentControl+'.'+sailType, 'cacheBSCtls_C_001_GRUP')

    def connectSailTwinAttr(self, sailType, currentControl): # ToDo deep debug
        '''
        Desc:
        Set driven keys in a superfast way

        Parameter:
        sailType = sail type ex (SAIL_A, SAIL_B, SAIL_C...)
        currentControl = current wind control CTRL
        '''
        currentAttr=cmds.attributeQuery(sailType, node=currentControl, listEnum=True)
        print('DEBUG CURRENT ATTR: ', currentAttr)
        currentAttrBuffer=currentAttr[0].split(':',-1)
        for i in range(0,len(currentAttrBuffer)-1):
            cmds.setAttr(currentControl+'.'+sailType,i)
            self.createDrivenKeys(currentControl+'.'+sailType, 'twinCacheBSCtls_C_001_GRUP')

    def addClothOffsetAttrib(self):
        '''
        Desc:
        Add cacheOffset for abc for sails
        '''
        boatGlobal='boatGlobal_C_001_CTRL'
        cmds.addAttr(boatGlobal, ln='abcCacheOffset', at='long', dv=0)
        cmds.setAttr(boatGlobal+'.abcCacheOffset', e=True, keyable=True)

    def addClothCacheAttrib(self):
        '''
        Desc:
        Add Attributes for sails
        '''
        selections = cmds.ls('*WIND*_*CTRL*')
        currentOptions=None
        for sel in selections:
            if cmds.nodeType(sel)=='transform':
                # Create different options for sails
                if 'WINDA_C_001' in sel:
                    # Add separator for SAILCACHE
                    cmds.addAttr(sel, ln='SAILCACHE', at='enum', en="___________:")
                    cmds.setAttr(sel+'.SAILCACHE', e=True, keyable=True)
                    cmds.setAttr(sel+'.SAILCACHE', lock=True, keyable=True)

                    sail_D1='Loose_VarA:Loose_VarB:Loose_VarC:Mid_VarA:Strong_VarA:Strong_VarB:SideWindLeft_VarA:SideWindRight_VarA'
                    cmds.addAttr(sel, ln='SAIL_D1', at='enum', en=sail_D1)
                    cmds.setAttr(sel+'.SAIL_D1', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_D1', 3)

                    sail_D2='Loose_VarA:Loose_VarB:Mid_VarA:Strong_VarA:Strong_VarB'
                    cmds.addAttr(sel, ln='SAIL_D2', at='enum', en=sail_D2)
                    cmds.setAttr(sel+'.SAIL_D2', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_D2', 2)

                    # Add separator for FLAGCACHE
                    cmds.addAttr(sel, ln='FLAGCACHE', at='enum', en="___________:")
                    cmds.setAttr(sel+'.FLAGCACHE', e=True, keyable=True)
                    cmds.setAttr(sel+'.FLAGCACHE', lock=True, keyable=True)

                    flag01='Loose:Mid:Strong'
                    cmds.addAttr(sel, ln='FLAG01', at='enum', en=flag01)
                    cmds.setAttr(sel+'.FLAG01', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.FLAG01', 1)

                elif 'WINDB_C_001' in sel or 'WINDC_C_001' in sel:
                    # Add separator for SAILCACHE
                    cmds.addAttr(sel, ln='SAILCACHE', at='enum', en="___________:")
                    cmds.setAttr(sel+'.SAILCACHE', e=True, keyable=True)
                    cmds.setAttr(sel+'.SAILCACHE', lock=True, keyable=True)

                    sail_A='Loose_VarA:Loose_VarB:Loose_VarC:Mid_VarA:Mid_VarB:Mid_VarC:Strong_VarA:Strong_VarB:Strong_VarC:SideWindLeft_VarA:SideWindRight_VarA'
                    cmds.addAttr(sel, ln='SAIL_A', at='enum', en=sail_A)
                    cmds.setAttr(sel+'.SAIL_A', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_A', 3)

                    sail_B='Loose_VarA:Loose_VarB:Loose_VarC:Mid_VarA:Mid_VarB:Mid_VarC:Strong_VarA:Strong_VarB:Strong_VarC:SideWindLeft_VarA:SideWindRight_VarA'
                    cmds.addAttr(sel, ln='SAIL_B', at='enum', en=sail_B)
                    cmds.setAttr(sel+'.SAIL_B', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_B', 3)

                    sail_C='Loose_VarA:Loose_VarB:Loose_VarC:Mid_VarA:Mid_VarB:Mid_VarC:Strong_VarA:Strong_VarB:Strong_VarC:SideWindLeft_VarA:SideWindRight_VarA'
                    cmds.addAttr(sel, ln='SAIL_C', at='enum', en=sail_C)
                    cmds.setAttr(sel+'.SAIL_C', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_C', 3)

                    # Add separator for FLAGCACHE
                    cmds.addAttr(sel, ln='FLAGCACHE', at='enum', en="___________:")
                    cmds.setAttr(sel+'.FLAGCACHE', e=True, keyable=True)
                    cmds.setAttr(sel+'.FLAGCACHE', lock=True, keyable=True)

                    if 'WINDB_C_001' in sel:
                        flag02='Mid:Strong'
                        cmds.addAttr(sel, ln='FLAG02', at='enum', en=flag02)
                        cmds.setAttr(sel+'.FLAG02', e=True, keyable=True)

                        # Set default value to MID
                        cmds.setAttr(sel+'.FLAG02', 0)

                    if 'WINDC_C_001' in sel:
                        flag03='Mid:Strong'
                        cmds.addAttr(sel, ln='FLAG03', at='enum', en=flag03)
                        cmds.setAttr(sel+'.FLAG03', e=True, keyable=True)

                        # Set default value to MID
                        cmds.setAttr(sel+'.FLAG03', 0)

                elif 'WINDD_C_001' in sel:
                    # Add separator for SAILCACHE
                    cmds.addAttr(sel, ln='SAILCACHE', at='enum', en="___________:")
                    cmds.setAttr(sel+'.SAILCACHE', e=True, keyable=True)
                    cmds.setAttr(sel+'.SAILCACHE', lock=True, keyable=True)

                    sail_E='Mid_VarA:Mid_VarB:Mid_VarC:Strong_VarA:Strong_VarB:Strong_VarC'
                    cmds.addAttr(sel, ln='SAIL_E', at='enum', en=sail_E)
                    cmds.setAttr(sel+'.SAIL_E', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_E', 0)

                    sail_D3='Loose_VarA:Loose_VarB:Mid_VarA:Strong_VarA:Strong_VarB:SideWindLeft_VarA:SideWindRight_VarA'
                    cmds.addAttr(sel, ln='SAIL_D3', at='enum', en=sail_D3)
                    cmds.setAttr(sel+'.SAIL_D3', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.SAIL_D3', 2)

                    # Add separator for FLAGCACHE
                    cmds.addAttr(sel, ln='FLAGCACHE', at='enum', en="___________:")
                    cmds.setAttr(sel+'.FLAGCACHE', e=True, keyable=True)
                    cmds.setAttr(sel+'.FLAGCACHE', lock=True, keyable=True)

                    flag04='Mid:Strong'
                    cmds.addAttr(sel, ln='FLAG04', at='enum', en=flag04)
                    cmds.setAttr(sel+'.FLAG04', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.FLAG04', 0)

                    flag05='Mid:Strong'
                    cmds.addAttr(sel, ln='FLAG05', at='enum', en=flag05)
                    cmds.setAttr(sel+'.FLAG05', e=True, keyable=True)

                    # Set default value to MID
                    cmds.setAttr(sel+'.FLAG05', 0)


    def connectBoatToWind(self, connectionType='flags'):
        '''
        Desc:
        Import dynCache from cloth for sails/flag

        Parameter:
        connectionType = type of connections 'flag', 'sail'
        '''

        # Check the windAsset
        windAsset=cmds.ls('WND_*_CTRL')
        windAsset=windAsset[0]

        # Check sails CTRLS
        boatSailCtrls=cmds.ls('*:*WIND*_CTRL')

        # Check flags CTRLS
        boatFlagCtrls=cmds.ls('*:*flagWind*_CTRL')

        # Check global CTRLS
        boatGlobalCtrls=cmds.ls('*:*boatGlobal*_CTRL')

        # List of objects
        outOfRot=[]

        for ctrl in boatGlobalCtrls:
            # Get the Position CTRL changing the name
            ctrlPos=ctrl.replace('boatGlobal','boatPosition')
            print('ctrlPos = ' + ctrlPos)
            #print('>>> HERE')
            #print('> CTRL: ', ctrl)

            # Store the current name
            currentName=ctrl.split(':',-1)[0]

            # Check if the boat is flooded or not
            rotX=cmds.getAttr(ctrl+'.rotateX')
            rotZ=cmds.getAttr(ctrl+'.rotateZ')

            #if rotX == 0 and rotZ == 0:
            # Make connections
            if connectionType=='flags':
                PMANode=cmds.createNode('plusMinusAverage', n=currentName+'FLAG'+'_PMAV')
                cmds.setAttr(PMANode+'.operation', 2)
                print('FLAGS PART: ')

                # Wind connection
                try:
                    cmds.connectAttr(windAsset+'.rotateY', PMANode+'.input3D[0].input3Dy', f=True)
                except:
                    self.debug('Connecton failed on: '+PMANode+'.input3D[0].input3Dy')

                try:
                    cmds.connectAttr(ctrl+'.rotateY', PMANode+'.input3D[1].input3Dy', f=True)
                except:
                    self.debug('Connecton failed on: '+PMANode+'.input3D[1].input3Dy')
                # Position control code
                try:
                    cmds.connectAttr(ctrlPos+'.rotateY', PMANode+'.input3D[2].input3Dy', f=True)
                    print('Succes!' + ctrlPos +'PMANode= '+PMANode)
                except:
                    self.debug('Connecton failed on: '+PMANode+'.input3D[2].input3Dy')

                for flag in boatFlagCtrls:
                    if currentName in flag:
                        # Remove connections if exists
                        kstMaya.deleteConnection('%s' %flag+'.rx;')
                        kstMaya.deleteConnection('%s' %flag+'.ry;')
                        kstMaya.deleteConnection('%s' %flag+'.rz;')
                        try:
                            cmds.connectAttr(windAsset+'.rotateX', flag+'.rotateX', f=True)
                        except:
                            self.debug('Connecton failed on: '+flag+'.rotateX')

                        try:
                            cmds.connectAttr(PMANode+'.output3Dy', flag+'.rotateY')
                        except:
                            self.debug('Connecton failed on: '+flag+'.rotateY')

                        try:
                            cmds.connectAttr(windAsset+'.rotateZ', flag+'.rotateZ', f=True)
                        except:
                            self.debug('Connecton failed on: '+flag+'.rotateZ')

            if connectionType=='sails':
                # create node
                PMANode=cmds.createNode('plusMinusAverage', n=currentName+'SAIL'+'_PMAV')
                cmds.setAttr(PMANode+'.operation', 2)
                print('SAILS PART: ')

                # Wind connection
                try:
                    cmds.connectAttr(windAsset+'.rotateY', PMANode+'.input3D[0].input3Dx', f=True)
                except:
                    self.debug('Connecton failed on WIND')

                # Boat rotation connection
                try:
                    cmds.connectAttr(ctrl+'.rotateY', PMANode+'.input3D[1].input3Dx', f=True)
                except:
                    self.debug('Connecton failed on BOAT ROTATION')
                # Position control code
                try:
                    cmds.connectAttr(ctrlPos+'.rotateY', PMANode+'.input3D[2].input3Dx', f=True)
                    print('Succes!' + ctrlPos +'PMANode= '+ PMANode)
                except:
                    self.debug('Connecton failed on: ', PMANode+'.input3D[2].input3Dx')
                for sail in boatSailCtrls:
                    if currentName in sail:
                        # Remove connection if exist
                        kstMaya.deleteConnection('%s' %sail+'.ry;')
                        try:
                            # Output connection
                            cmds.connectAttr(PMANode+'.output3Dx', sail+'.rotateY', f=True)
                        except:
                            self.debug('Connection failed on PMA out and '+sail+'.rotateY')

    def skinClosestGeometry(self, selections, skinObjects, distance=1.0):
        '''
        Desc:
        Create skin based on closest vertex

        Parameter:
        distance = distance threshold

        Return: NoneFLIN01_032:windb_C_002_GRUP
        '''
        vtxList=[]
        skinObjectsList=skinObjects
        vtxList=kstRig.getClosestVertex(selections[0], skinObjects[0], distance)
        self.debug(vtxList)