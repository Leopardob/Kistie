'''
K.I.S.T.I.E (Keep, It, Simple, Take, It, Easy)
Created on 1 Jan 2013
@author: Leonardo Bruni, leo.b2003@gmail.com
Kistie Math Library
This Kistie implementation i's part of project 'Kistie_Autorig' by Leonardo Bruni, leo.b2003@gmail.com
'''

import maya.OpenMaya as om
import math

# Import KstOut
import kcode.kcore.KstOut as _KstOut_
reload(_KstOut_)
KstOut = _KstOut_.KstOut()

# Define math mag function, actually is not used but can be usefull in future
mag = lambda x: math.sqrt(sum(i ** 2 for i in x))

class KstMath(object):
    # Debug module name variable
    _debug = 'KstMath'

    def __init__(self):
        # KstOut.debug(KstMath._debug, 'kstMath module loaded...')
        pass
    # From a point get a MVector
    def vec_from_point(self, pt):
        '''
        Desc:
        Method return a Vec from a point or list

        Parameter:
        pt = point in this format pt=[0,0,0]

        Return:
        a MVector
        '''
        if isinstance(pt, (list, tuple)):
            vec = om.MVector(pt[0], pt[1], pt[2])
            return vec
        else:
            KstOut.debug(KstMath._debug, '%s wrong type, you need or a list or a tuple' % pt)

    # From 2 point get the result MVector
    def vec_from_2_points(self, pt_a, pt_b):
        '''
        Desc:
        Method returns a Vec from 2 points

        Parameter:
        pt_a = first point
        pr_b = second point

        Return:
        a MVector
        '''
        tmp_a = om.MPoint(pt_a)
        tmp_b = om.MPoint(pt_b)
        vec = om.MVector(pt_a - pt_b)
        return vec

    def vec_middle_point(self, pt_a, pt_b):
        '''
        Desc:
        Method returns a middle point between 2 points

        Parameter:
        pt_a = first point
        pr_b = second point

        Return:
        a MPoint
        '''
        tmp_a = self.vec_from_point(pt_a)
        tmp_b = self.vec_from_point(pt_b)
        pt_mid = om.MVector(tmp_a + tmp_b) * .5
        return pt_mid

    def get_44_matrix_from_1_vec(self, normal, point):
        '''
        Desc:
        Method retunrs a MMatrix from 1 vectors and 1 point (startpoint)

        Parameter:
        normal = First Vector
        point = origin

        Return:
        a MMatrix
        '''
        # Convert all input in MVector for work with MVector and MMatrix API methods
        self.normal = self.vec_from_point(normal)
        self.point = self.vec_from_point(point)

        # Add arbitrary axis as binormal
        temp_binormal = self.vec_from_point([1,0,0])

        # Find up vector orhto to the normal
        self.upvec = self.cross(normal, temp_binormal, normalize=True)

        # Cross again for make binormal ortho
        self.binormal = self.cross(normal, temp_binormal, normalize=True)

        # Make orthog
        # Define m_utils for float utils
        m_utils = om.MScriptUtil()

        # Define a matrix MMatrix
        mat = om.MMatrix()

        # Building the matrix 4x4
        # 1 row
        m_utils.setDoubleArray(mat[0], 0, self.binormal.x)
        m_utils.setDoubleArray(mat[0], 1, self.binormal.y)
        m_utils.setDoubleArray(mat[0], 2, self.binormal.z)
        m_utils.setDoubleArray(mat[0], 3, 0)

        # 2 row
        m_utils.setDoubleArray(mat[1], 0, self.normal.x)
        m_utils.setDoubleArray(mat[1], 1, self.normal.y)
        m_utils.setDoubleArray(mat[1], 2, self.normal.z)
        m_utils.setDoubleArray(mat[1], 3, 0)

        # 3 row
        m_utils.setDoubleArray(mat[2], 0, self.upvec.x)
        m_utils.setDoubleArray(mat[2], 1, self.upvec.y)
        m_utils.setDoubleArray(mat[2], 2, self.upvec.z)
        m_utils.setDoubleArray(mat[2], 3, 0)

        # 4 row
        m_utils.setDoubleArray(mat[3], 0, self.point.x)
        m_utils.setDoubleArray(mat[3], 1, self.point.y)
        m_utils.setDoubleArray(mat[3], 2, self.point.z)
        m_utils.setDoubleArray(mat[3], 3, 0)

        return mat

    def get_44_matrix_from_2_vec(self, normal, binormal, point):
        '''
        Desc:
        Method retunrs a MMatrix from 2 vectors and 1 point (startpoint)

        Parameter:
        normal = First Vector
        binormal = Second Vector
        point = origin

        Return:
        a MMatrix
        '''
        # Convert all input in MVector for work with MVector and MMatrix API methods
        self.normal = self.vec_from_point(normal)
        self.point = self.vec_from_point(point)

        # Find up vector orhto to the normal
        self.upvec = self.cross(normal, binormal, normalize=True)

        # Cross again for make binormal ortho
        self.binormal = self.cross(normal, self.upvec, normalize=True)

        # Make orthog
        # Define m_utils for float utils
        m_utils = om.MScriptUtil()

        # Define a matrix MMatrix
        mat = om.MMatrix()

        # Building the matrix 4x4
        # 1 row
        m_utils.setDoubleArray(mat[0], 0, self.binormal.x)
        m_utils.setDoubleArray(mat[0], 1, self.binormal.y)
        m_utils.setDoubleArray(mat[0], 2, self.binormal.z)
        m_utils.setDoubleArray(mat[0], 3, 0)

        # 2 row
        m_utils.setDoubleArray(mat[1], 0, self.normal.x)
        m_utils.setDoubleArray(mat[1], 1, self.normal.y)
        m_utils.setDoubleArray(mat[1], 2, self.normal.z)
        m_utils.setDoubleArray(mat[1], 3, 0)

        # 3 row
        m_utils.setDoubleArray(mat[2], 0, self.upvec.x)
        m_utils.setDoubleArray(mat[2], 1, self.upvec.y)
        m_utils.setDoubleArray(mat[2], 2, self.upvec.z)
        m_utils.setDoubleArray(mat[2], 3, 0)

        # 4 row
        m_utils.setDoubleArray(mat[3], 0, self.point.x)
        m_utils.setDoubleArray(mat[3], 1, self.point.y)
        m_utils.setDoubleArray(mat[3], 2, self.point.z)
        m_utils.setDoubleArray(mat[3], 3, 0)

        return mat

    # From normal and up vector get a transformation matrix
    def get_44_matrix_from_3_vec(self, normal, binormal, upvec, point):
        '''
        Desc:
        Method retunrs a MMatrix from 3 vectors and 1 point (startpoint)

        Parameter:
        normal = First Vector
        binormal = Second Vector
        upvec = Third Vector
        point = origin

        Return:
        a MMatrix
        '''
        # Convert all input in MVector for work with MVector and MMatrix API methods
        self.normal = self.vec_from_point(normal)
        self.binormal = self.vec_from_point(binormal)
        self.upvec = self.vec_from_point(upvec)
        self.point = self.vec_from_point(point)

        # Define m_utils for float utils
        m_utils = om.MScriptUtil()

        # Define a matrix MMatrix
        mat = om.MMatrix()

        # Building the matrix 4x4
        # 1 row
        m_utils.setDoubleArray(mat[0], 0, self.binormal.x)
        m_utils.setDoubleArray(mat[0], 1, self.binormal.y)
        m_utils.setDoubleArray(mat[0], 2, self.binormal.z)
        m_utils.setDoubleArray(mat[0], 3, 0)

        # 2 row
        m_utils.setDoubleArray(mat[1], 0, self.normal.x)
        m_utils.setDoubleArray(mat[1], 1, self.normal.y)
        m_utils.setDoubleArray(mat[1], 2, self.normal.z)
        m_utils.setDoubleArray(mat[1], 3, 0)

        # 3 row
        m_utils.setDoubleArray(mat[2], 0, self.upvec.x)
        m_utils.setDoubleArray(mat[2], 1, self.upvec.y)
        m_utils.setDoubleArray(mat[2], 2, self.upvec.z)
        m_utils.setDoubleArray(mat[2], 3, 0)

        # 4 row
        m_utils.setDoubleArray(mat[3], 0, self.point.x)
        m_utils.setDoubleArray(mat[3], 1, self.point.y)
        m_utils.setDoubleArray(mat[3], 2, self.point.z)
        m_utils.setDoubleArray(mat[3], 3, 0)

        return mat

    # Extract transformations from matrix
    def get_transformations(self, inputmatrix, translate=True, rotate=True, scale=True):
        '''
        Desc:
        Method retunrs a list of float that contains transfomations

        Parameter:
        inputmatrix = MMatrix from extract transformations
        translate = bool
        rotate = bool
        scale = bool

        Return:
        a list of float that contains transformation defined by bool
        '''
        # Define m_utils for float utils
        m_utils = om.MScriptUtil()

        # Define spaces for transformations
        world_space = om.MSpace.kWorld
        object_space = om.MSpace.kObject

        # TRANSLATE
        # Define MTransformMatrix, for get method on transform
        trs_matrix = om.MTransformationMatrix(inputmatrix)

        # Get translation from MTransformationMatrix
        tr = trs_matrix.getTranslation(world_space)

        # ROTATE
        # Define MEulerRotation for extract rotation
        rot_euler = om.MEulerRotation()

        # Define rotation order to ZYX
        rot_order = om.MTransformationMatrix().kZYX

        # Tranform rotation in quaternion
        rot_quaternion = trs_matrix.rotation()

        # Convert quaternion in euler angles
        ro = rot_quaternion.asEulerRotation()
        ro.reorderIt(rot_order)

        # SCALE
        m_utils.createFromList([0, 0, 0], 3)
        scale_vec = m_utils.asDoublePtr()
        trs_matrix.getScale(scale_vec, object_space)
        sc = [m_utils.getDoubleArrayItem(scale_vec, i) for i in range(0, 3)]

        # Convert MVector in floatList
        t = [tr.x, tr.y, tr.z]
        r = [ro.x, ro.y, ro.z]
        s = sc

        # Make an empty list
        trs = []

        # OUTPUT
        # for user flag export trs list
        if translate:
            trs.append(t)

        if rotate:
            trs.append(r)

        if scale:
            trs.append(s)

        return trs

    # Define a method for a crossProduct
    def cross(self, vec_a, vec_b, normalize=True):
        '''
        Desc:
        Method retunrs cross product from 2 vectors

        Parameter:
        vec_a = First Vector
        vec_b = Second Vector
        normalize = bool that return the normalized vector if is True

        Return:
        a MVector that is the result of the cross product between vec_a and vec_b
        '''
        # Convert input vector in MVector
        result_vec = self.vec_from_point((
            vec_a[1] * vec_b[2] - vec_a[2] * vec_b[1], vec_a[2] * vec_b[0] - vec_a[0] * vec_b[2],
            vec_a[0] * vec_b[1] - vec_a[1] * vec_b[0]))

        if normalize:
            result_vec.normalize()
        return result_vec

    # Define a method for a dotProduct
    def dot(self, vec_a, vec_b):
        '''
        Desc:
        vec_a = First Vector
        vec_b = Second Vector
        normalize = bool that return the normalized vector if is True

        Return:
        a MVector that is the result of the dot product between vec_a and vec_b
        '''
        # Convert input vectors in MVector
        self.vec_a = self.vec_from_point(vec_a)
        self.vec_b = self.vec_from_point(vec_b)
        result = self.vec_a * self.vec_b
        return result

    # Define a method for len
    def get_mag(self, vec_a):
        '''
        vec_a = First Vector
        '''

        # Convert input vector in MVector
        mag = vec_a.length()
        return mag