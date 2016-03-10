# Kistie (K.eep, I.t, S.imple, T.ake, I.t, E.asy)
A simple framework for rigging in Maya, and soon other softwares.
Softwares that coming soon will be supported in Kistie are (Houdini, Modo, Blender)

I started last year to develop Kistie in my spare time because in the studios where i worked we used a lot of different software, and all time we rewrote same procedure and same classes that make exactly the same stuff but in different softwares.
So i added a level of API in that way:
instead:  Developer -> SW_API (different API for each SW)
          Developer -> Kistie (All API for each SW)
It's just an experiment, maybe a bit crazy, but for now at least for me, already semplified a lot my life, i hope that will also for you.
So, this first commit it's just for Maya also for see the interest about Kistie from CG community.

How to use:
download or clone Kistie repo for instance: C:/Work/DEV/Kistie

Inside Maya (all version that suppor Python):

ex.1 - Channels connections
- Create to cubes

run this script:
import maya.cmds as cmds

- Kistie, Python path, change if you need
sys.path.append('C:/Work/DEV/Kistie') # Your repo

from kcode.kcore.KstMaya import KstMaya
kmaya = KstMaya()

kmaya.node_op('pCube1.tx','>>','pCube2.ty')

ex.3 - Object creation
- Create two locators

run this script:
import maya.cmds as cmds

from kcode.krig.KstRig import KstRig
krig = KstRig()
krig.create_line_from_objects('curve', ['locator1', 'locator2'])

ex.2 - Object creation
- Create two locators

run this script:
import maya.cmds as cmds

from kcode.krig.KstRig import KstRig
krig = KstRig()
krig.create_line_from_objects('curve', ['locator1', 'locator2'])

ex.4 - Joint chain creation from scratch
from an empty Maya scene

run this script:
import maya.cmds as cmds

from kcode.krig.KstRig import KstRig
krig = KstRig()
krig.create_joint_chain('MyChain',[(0, 0, 0), (0,1,0), (0,2,0), (0,3,0)])

ex.5 - Joint chain creation from 3 locators
create 3 locators

run this script:
import maya.cmds as cmds

from kcode.krig.KstRig import KstRig
krig = KstRig()
pos = kmaya.get_position_list_from_objs(['locator1', 'locator2', 'locator3'])
krig.create_joint_chain('MyChain',pos)

Of course you can also build n locators
and make this:

selection = cmds.ls(sl=True)
pos = kmaya.get_position_list_from_objs(selection)
krig.create_joint_chain('MyChain',pos)

You will see that Kistie is quite flexible, and most important Open Source, so, change what you want or expand as you want and just...
KEEP IT SIMPLE TAKE IT EASY

Enjoy!

Leonardo Bruni
