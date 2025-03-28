import unittest
import logging
import numpy as np
import spatialanalysis as sa
print(sa.GOCF)

class TestPointBasics(unittest.TestCase):
    def test_ident(self):
        #Check that two points in the GOCF are equal
        pt1 = sa.Point([0, 0, 0], 'Pt1')
        pt2 = sa.Point([0, 0, 0], 'Pt2', nativeCF=sa.GOCF)
        self.assertEqual(pt1, pt2)

class TestCoordinateFrameBasics(unittest.TestCase):
    def setUp(self):
        self.plus1Z = sa.CoordinateFrame("+1Z", tfMat=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]]))
        self.threeAxShift = sa.CoordinateFrame("+1Z", tfMat=np.array([[1, 0, 0, 1.2], [0, 1, 0, 3.4], [0, 0, 1, 5.6], [0, 0, 0, 1]]))
        self.Xrot = sa.CoordinateFrame("+1Z", tfMat=sa.makeTransform(0, 0, 0, 45, 0, 0))

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
        self.assertEqual(pt, np.array([1, 0, 1.41421356]))

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    unittest.main()
