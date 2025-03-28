import logging
import numpy as np
from spatialanalysis.utils import *

class CoordinateFrame(object):
    def __init__(self, shortName, tfMat=None, longName=None):
        self.logger = logging.getLogger(shortName)
        self.shortName = shortName

        if tfMat is None:
            self.logger.info(f"Creating {shortName} equal to GOCF")
            self.tfMat = np.identity(4, dtype='float')
        else:
            assert np.array_equal(tfMat.shape, np.array([4, 4]))
            self.tfMat = np.array(tfMat, dtype='float')

        if longName is None:
            self.longName = shortName
        else:
            self.longName = str(longName)

    def origin(self):
        return self.tfMat[:3, 3]

    def copy(self, newShortName, newLongName=None):
        return CoordinateFrame(newShortName, tfMat=self.tfMat, longName=newLongName)

    def __repr__(self):
        return f"<CoordinateFrame '{self.shortName}' ({self.longName})>"

    def __str__(self):
        return f"<CF '{self.shortName}'>"

    def __eq__(self, other):
        if isinstance(other, CoordinateFrame):
            return np.allclose(self.tfMat, other.tfMat)
        return False

    def transform(self, tx, ty, tz, rx, ry, rz, units='degrees', refFrame=None):
        if refFrame is None:
            refFrame = GOCF

        tf = makeTransform(tx, ty, tz, rx, ry, rz, units=units)

        foo = refFrame.tfMat @ tf @ np.linalg.inv(refFrame.tfMat) @ self.tfMat
        self.tfMat = foo

    def asJSON(self):
        pass

GOCF = CoordinateFrame('GOCF', longName="Global Optical Coordinate Frame")
