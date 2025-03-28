import logging
import numpy as np
from spatialanalysis.CoordinateFrame import GOCF, CoordinateFrame
from spatialanalysis.utils import *

class Point(object):
    def __init__(self, coordinates, name, nativeCF=None):
        self.logger = logging.getLogger(name)
        self.name = name
        assert len(coordinates) == 3
        coordinates = np.array(coordinates, dtype='float')

        self.coordinatesNative = np.array(coordinates, dtype='float')

        if nativeCF is None:
            #Assume GOCF
            self.logger.warning("No native coordinate frame given; assuming GOCF")
            self.coordinates = self.coordinatesNative
        else:
            assert isinstance(nativeCF, CoordinateFrame)
            homogCoord = np.append(coordinates, 1.)
            self.coordinates = (nativeCF.tfMat @ homogCoord)[:3]

    def __repr__(self):
        return f"<Point '{self.name}' {self.coordinatesNative}>"

    def __str__(self):
        return f"<Point '{self.name}'>"

    def __eq__(self, other):
        if isinstance(other, Point):
            return np.allclose(self.coordinatesNative, other.coordinatesNative)
        elif isinstance(other, np.ndarray):
            assert len(other) == 3
            return np.allclose(self.coordinates, other)

    def transform(self, tx, ty, tz, rx, ry, rz, refFrame=None):
        if refFrame is None:
            refFrame = GOCF

        tf = makeTransform(tx, ty, tz, rx, ry, rz)
        homogCoord = np.append(self.coordinates, 1.)
        foo = refFrame.tfMat @ tf @ np.linalg.inv(refFrame.tfMat) @ homogCoord
        self.coordinates = foo[:3]
