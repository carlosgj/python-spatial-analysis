import numpy as np
import pint
import logging
from spatialanalysis.units import units, deg, rad

def makeRotation(rx, ry, rz):
    if not isinstance(rx, pint.Quantity):
        logging.warning("rx does not have units. Assuming radians.")
        rx = rx * rad
    if not isinstance(ry, pint.Quantity):
        logging.warning("rx does not have units. Assuming radians.")
        ry = ry * rad
    if not isinstance(rz, pint.Quantity):
        logging.warning("rx does not have units. Assuming radians.")
        rz = rz * rad

    sa = np.sin(rz).magnitude
    ca = np.cos(rz).magnitude

    sb = np.sin(ry).magnitude
    cb = np.cos(ry).magnitude

    sg = np.sin(rx).magnitude
    cg = np.cos(rx).magnitude

    mat = np.array([[ca*cb, ca*sb*sg-sa*cg, ca*sb*cg+sa*sg],
                    [sa*cb, sa*sb*sg+ca*cg, sa*sb*cg-ca*sg],
                    [-sb,   cb*sg,          cb*cg]])

    return mat

def makeTransform(tx, ty, tz, rx, ry, rz):
    rot = makeRotation(rx, ry, rz)
    t = np.array([[tx], [ty], [tz]], dtype='float')
    mat = np.append(rot, t, axis=1)
    homPad = np.array([[0, 0, 0, 1]], dtype='float')
    mat = np.append(mat, homPad, axis=0)
    return mat
