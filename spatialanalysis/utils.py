import numpy as np

def makeRotation(rx, ry, rz, units='degrees'):
    if units == 'degrees':
        rx = np.deg2rad(rx)
        ry = np.deg2rad(ry)
        rz = np.deg2rad(rz)

    sa = np.sin(rz)
    ca = np.cos(rz)

    sb = np.sin(ry)
    cb = np.cos(ry)

    sg = np.sin(rx)
    cg = np.cos(rx)


    mat = np.array([[ca*cb, ca*sb*sg-sa*cg, ca*sb*cg+sa*sg],
                    [sa*cb, sa*sb*sg+ca*cg, sa*sb*cg-ca*sg],
                    [-sb,   cb*sg,          cb*cg]])

    return mat

def makeTransform(tx, ty, tz, rx, ry, rz, units='degrees'):
    rot = makeRotation(rx, ry, rz, units=units)
    t = np.array([[tx], [ty], [tz]], dtype='float')
    mat = np.append(rot, t, axis=1)
    homPad = np.array([[0, 0, 0, 1]], dtype='float')
    mat = np.append(mat, homPad, axis=0)
    return mat
