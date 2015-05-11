import maya.cmds as cmds
import sys

sys.path.append('C:/DEV/Kistie')

import Kistie as _KstCore_
import kcode.kcore.kmaya.kattrs.KstAttrs as _KstAttrs_
import kcode.krig.KstRig as _KstRig_
import kcode.kcore.KstDraw as _KstDraw_
import kcode.kcore.KstMaya as _KstMaya_
import kcode.krig.kstRigModules.RTS_Rig as _KstRigRts_
import kcode.krig.kstRigModules.Wing as _Wing_

reload(_KstCore_)
reload(_KstAttrs_)
reload(_KstRig_)
reload(_KstDraw_)
reload(_KstMaya_)
reload(_KstRigRts_)
reload(_Wing_)

KstCore = _KstCore_.KistieCore()
KstAttrs=_KstAttrs_.KstAttrs()
KstRig=_KstRig_.KstRig()
KstDraw=_KstDraw_.KstDraw()
KstMaya=_KstMaya_.KstMaya()
KstRigRts=_KstRigRts_.RTS_Rig()
Wing=_Wing_.Wing('Wing','L')

# Guide generation
user_guides = ['locator9','locator10','locator11','locator12']
guides = Wing.generate_guides(user_guides)

# Generate interpolation surface
follicle_list = Wing.generate_surface(guides[0], guides[1], from_node=False)

# Generate joints on surface 
Wing.generate_joints_on_surface(follicle_list, from_node=False, radius=1)

# Generate interpolated points
points = ['down_Wing_L_001_LOC','down_Wing_L_002_LOC','down_Wing_L_003_LOC','down_Wing_L_004_LOC']
Wing.create_interpolation_joints(points)

# Generate wing surfaces
Wing.generate_wing_surfaces(points, from_node=False, offset=0.15)