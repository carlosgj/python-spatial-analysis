import unittest
import logging
import numpy as np
import spatialanalysis as sa
from spatialanalysis.units import units, deg, rad

class TestPointBasics(unittest.TestCase):
    def test_ident(self):
        #Check that two points in the GOCF are equal
        pt1 = sa.Point([0, 0, 0], 'Pt1')
        pt2 = sa.Point([0, 0, 0], 'Pt2', nativeCF=sa.GOCF)
        self.assertEqual(pt1, pt2)

    def test_shiftInGOCF(self):
        pt1 = sa.Point([0, 0, 0], 'Pt1', nativeCF=sa.GOCF)
        pt1.transform(1.5, 0, 0, 0*deg, 0*deg, 0*deg)
        self.assertEqual(pt1, np.array([1.5, 0, 0]))

    def test_rotateInGOCF(self):
        pt1 = sa.Point([0, 0, 0], 'Pt1', nativeCF=sa.GOCF)
        pt1.transform(1, 0, 0, 0*deg, 0*deg, 0*deg)
        pt1.transform(0, 0, 0, 0*deg, 0*deg, 45*deg)
        self.assertEqual(pt1, np.array([0.70710678, 0.70710678, 0]))

    def test_rotateInOtherCF(self):
        refCF = sa.CoordinateFrame("PlusX", tfMat=sa.makeTransform(1.5, 0, 0, 0*rad, 0*rad, 0*rad))
        pt1 = sa.Point([0, 0, 0], 'Pt1', nativeCF=sa.GOCF)
        pt1.transform(0, 0, 0, 0*deg, 180*deg, 0*deg, refFrame=refCF)
        self.assertEqual(pt1, np.array([3, 0, 0]))

class TestCoordinateFrameBasics(unittest.TestCase):
    def setUp(self):
        self.plus1Z = sa.CoordinateFrame("+1Z", tfMat=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]]))
        self.threeAxShift = sa.CoordinateFrame("ShiftXYZ", tfMat=np.array([[1, 0, 0, 1.2], [0, 1, 0, 3.4], [0, 0, 1, 5.6], [0, 0, 0, 1]]))
        self.Xrot = sa.CoordinateFrame("Xrot", tfMat=sa.makeTransform(0, 0, 0, 30*deg, 0*deg, 0*deg))

    def test_GOCF(self):
        self.assertTrue(isinstance(sa.GOCF, sa.CoordinateFrame))

    def test_ident(self):
        #Check that two CFs are equal
        cf1 = sa.CoordinateFrame("CF1")
        self.assertEqual(sa.GOCF, cf1)

    def test_oneAxOffset1(self):
        pt = sa.Point([0, 0, 0], 'Pt1', nativeCF=self.plus1Z)
        self.assertEqual(pt, np.array([0, 0, 1]))

    def test_oneAxOffset2(self):
        pt = sa.Point([0, 0, 1.5], 'Pt1', nativeCF=self.plus1Z)
        self.assertEqual(pt, np.array([0, 0, 2.5]))

    def test_oneAxOffset3(self):
        pt = sa.Point([1.2, 3.4, 5.6], 'Pt1', nativeCF=self.plus1Z)
        self.assertEqual(pt, np.array([1.2, 3.4, 6.6]))

    def test_3AxOffset(self):
        pt = sa.Point([1., 2., -3.], 'Pt1', nativeCF=self.threeAxShift)
        self.assertEqual(pt, np.array([2.2, 5.4, 2.6]))

    def test_rotate(self):
        pt = sa.Point([1, 1, 1], 'Pt1', nativeCF=self.Xrot)
        self.assertEqual(pt, np.array([1, 0.3660254, 1.3660254]))

    def test_copy(self):
        cf1 = self.threeAxShift.copy('CF1')
        self.assertEqual(self.threeAxShift, cf1)

    def test_shiftAfterCreation(self):
        cf1 = sa.CoordinateFrame("CF1")
        cf1.transform(1.2, 3.4, 5.6, 0*rad, 0*rad, 0*rad)
        self.assertEqual(self.threeAxShift, cf1)

    def test_rotateAfterCreation(self):
        cf1 = sa.CoordinateFrame("CF1")
        cf1.transform(0, 0, 0, 30*deg, 0*deg, 0*deg)
        self.assertEqual(self.Xrot, cf1)

    def test_rotateInOtherFrame(self):
        refCF = sa.CoordinateFrame("RefCF")
        refCF.transform(1.5, 0, 0, 0*deg, 0*deg, 0*deg)

        testCF1 = sa.CoordinateFrame("TestCF1")
        testCF1.transform(0, 0, 0, 0*deg, 180*deg, 0*deg)
        testCF1.transform(3, 0, 0, 0*deg, 0*deg, 0*deg)

        testCF2 = sa.CoordinateFrame("TestCF2")
        testCF2.transform(0, 0, 0, 0*deg, 180*deg, 0*deg, refFrame=refCF)

        self.assertEqual(testCF1, testCF2)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    #Make sure things print okay(
    print(sa.GOCF)
    print(repr(sa.GOCF))
    pt = sa.Point([0, 0, 0], 'Pt')
    print(pt)
    print(repr(pt))

    unittest.main()
