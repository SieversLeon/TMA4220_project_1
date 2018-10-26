#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements solver for 2D Helmholtz problem
"""
import numpy as np
import scipy.integrate as integrate

from project_1.infrastructure.p1_reference_element import P1ReferenceElement
from project_1.infrastructure.affine_transformation import AffineTransformation
from project_1.utils.integration import gauss_legendre_reference
from project_1.solvers.matrix_generation import generate_mass_matrix, generate_stiffness_matrix


def solve_helmholtz(mesh, f_function, quadpack=False, accuracy=1.49e-05):
    """
    Solves the Helmholtz problem under fixed BC.
    :param mesh: The mesh to operate on
    :param f_function: The inhomogenous right hand side
    :param quadpack: Should the Fortran quadpack package be used to integrate numerically
    :param accuracy: The accuracy for quadpack
    """

    vertices = mesh.vertices
    triangles = mesh.triangles
    varnr = mesh.supportsy * mesh.supportsx
    atraf = AffineTransformation()
    p1_ref = P1ReferenceElement()
    supports = 7

    # Mass matrix
    print("[Info] Calculating mass matrix")
    M = generate_mass_matrix(accuracy, atraf, mesh, p1_ref, quadpack, triangles, varnr, vertices)

    # Stiffness Matrix
    print("[Info] Calculating stiffness matrix")
    K = generate_stiffness_matrix(accuracy, atraf, mesh, p1_ref, quadpack, triangles, varnr, vertices)

    # b
    print("[Info] Calculating linear form")
    b = generate_linear_form(accuracy, atraf, f_function, mesh, p1_ref, quadpack, supports, triangles, varnr, vertices)

    A = K + M

    # BC Dirichlet
    nr = np.shape(vertices)[1]
    for i in range(nr):
        if vertices[1, i] == 0 or vertices[1, i] == 1:
            A[i, :] = np.zeros((1, nr))
            A[i, i] = 1
            b[i] = 0

    # Solve system
    u = np.linalg.inv(A).dot(b)
    return vertices, u


def generate_linear_form(accuracy, atraf, f_function, mesh, p1_ref, quadpack, supports, triangles, varnr, vertices):
    b = np.zeros((varnr, 1))
    for n in range(len(mesh.triangles)):
        tr_current = mesh.triangles[n]
        v0_coord = (vertices[0, triangles[n].v0], vertices[1, triangles[n].v0])
        v1_coord = (vertices[0, triangles[n].v1], vertices[1, triangles[n].v1])
        v2_coord = (vertices[0, triangles[n].v2], vertices[1, triangles[n].v2])
        atraf.set_target_cell(v0_coord, v1_coord, v2_coord)

        x_min = np.min([v0_coord[0], v1_coord[0], v2_coord[0]])
        x_max = np.max([v0_coord[0], v1_coord[0], v2_coord[0]])
        y_min = np.min([v0_coord[1], v1_coord[1], v2_coord[1]])
        y_max = np.max([v0_coord[1], v1_coord[1], v2_coord[1]])
        jinvt = atraf.get_inverse_jacobian().T
        j = atraf.get_jacobian()
        det = atraf.get_determinant()
        for i in range(3):
            if quadpack:
                ans, err = integrate.dblquad(b_integrant, x_min, x_max, lambda x: y_min, lambda x: y_max,
                                             epsabs=accuracy, epsrel=accuracy,
                                             args=(p1_ref, i, f_function, jinvt, v0_coord))
            else:
                ans, err = gauss_legendre_reference(b_integrant_reference,
                                                    args=(p1_ref, i, f_function, j, v0_coord, det), supports=supports)
            b[tr_current.v[i]] += ans
    return b


def mass_matrix_integrant(y, x, p1_ref, i, j):
    co = (x, y)
    return p1_ref.value(co)[i] * p1_ref.value(co)[j]


def stiffness_matrix_integrant_fast(y, x, p1_ref, i, j, jinvt, result):
    if (x + y > 1):
        result = 0
    return result


def stiffness_matrix_integrant(y, x, p1_ref, i, j, jinvt):
    co = (x, y)
    return jinvt.dot(p1_ref.gradients(co)[:, i]).T.dot(jinvt.dot(p1_ref.gradients(co)[:, j]))


def b_integrant(y, x, p1_ref, i, f_function, jinvt, v0_coord):
    co = (x, y)
    xp = np.array([x - v0_coord[0], y - v0_coord[1]])
    x_tr = (jinvt.dot(xp)[0], jinvt.dot(xp)[1])
    val = p1_ref.value(x_tr)[i]
    return val * f_function.value(co)


def b_integrant_reference(y, x, p1_ref, i, f_function, j, v0_coord, det):
    co = (x, y)
    xc = np.array([[x], [y]])
    x0 = np.array([[v0_coord[0]], [v0_coord[1]]])
    x_new = j.dot(xc) + x0
    return np.asscalar(p1_ref.value(co)[i] * f_function.value((x_new[0], x_new[1]))) * np.abs(det)
