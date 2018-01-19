# Coordinated Spline Motion and Robot Control Project
# 
# Copyright (c) 2017 Olga Petrova <olga.petrova@cvut.cz>
# Advisor: Pavel Pisa <pisa@cmp.felk.cvut.cz>
# FEE CTU Prague, Czech Republic
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# In 2017, project funded by PiKRON s.r.o. http://www.pikron.com/

''' Module provides functions for points interpolation using p-splines '''

# based on Eilers and Marx, Flexible Smoothing with B-splines and Penalties, 1996

import numpy as np
from utils import param_correction

def b_spline(xs, xl, xr, ndx, bdeg):
    dx = (xr - xl)/ndx
    t = xl + dx*np.arange(-bdeg, ndx+1)
    Bs = np.empty((len(xs), t.shape[0]))
    r = np.arange(1, len(t))
    r = np.append(r, 0)
    T = (0*xs[0] + 1)*t
    for i, x in enumerate(xs):
        X = x*(0*t + 1)
        P = (X - T)/dx
        B = np.array((T <= X) & (X < (T + dx))).astype(float)
        if np.count_nonzero(B) > 1:
            B /= np.sum(B)
        for k in range(1, bdeg+1):
            B = (np.multiply(P, B) + np.multiply((k + 1 - P), B[r]))/k
        Bs[i,:] = B
    return Bs


def p_spline(x, xl, xr, ndx, bdeg, pord, lam, y):
    B = b_spline(x, xl, xr, ndx, bdeg)
    m, n = B.shape
    D = np.diff(np.eye(n), pord).T
    a = np.linalg.inv(B.T.dot(B) + lam*D.T.dot(D)).dot(B.T.dot(y))
    # yhat = B.dot(a)
    # Q = np.linalg.inv(B.T.dot(B) + lam*D.T.dot(D))
    # s = np.sum((y - yhat)**2)
    # t = np.sum(np.diag(Q.dot(B.T.dot(B))))
    # gcv = s/(m - t) ** 2
    return a


def M_trans(bdeg):
    if bdeg == 2:
        M = np.array([[0.5, -1.0, 0.5],[-1.0, 1.0, 0.0],[0.5, 0.5, 0.0]])

    if bdeg == 3:
        M = np.array([[-1.0/6.0, 0.5, -0.5, 1.0/6.0],[0.5, -1.0, 0.5, 0.0],
                      [-0.5, 0.0, 0.5, 0.0],[1.0/6.0, 2.0/3.0, 1.0/6.0, 0.0]])
    return M


def interpolate(points, num_segments, poly_deg, p_ord, lambda_):
    assert poly_deg == 2 or poly_deg == 3, 'Function supports only 2nd and 3rd order polynomials'
    assert poly_deg >= p_ord, 'Degree of polynomial must be greater than order of penalty'

    n, dim = points.shape
    t = np.arange(0, n)

    a = p_spline(t.T, 0.0, float(n-1), num_segments, poly_deg, p_ord, lambda_, points)
    Mn = M_trans(poly_deg)

    param = np.empty((0, dim*poly_deg))
    for i in range(num_segments):
        c = np.flipud(Mn.dot(a[i:i + poly_deg + 1])).T
        c = np.reshape(c[:,1:], (dim*poly_deg))
        param = np.append(param, [c], axis=0)

    param = param_correction(points[0], param, poly_deg)

    return param