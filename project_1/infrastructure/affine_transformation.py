#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements the affine transformation from the reference element
"""

import numpy as np


class AffineTransformation:
    """
    Defines the affine transformation
    """

    def set_target_cell(self, v0, v1, v2):
        """
        Sets the target cell
        :param v0: Tuple (x,y) of the location of vertex v0
        :param v1: Tuple (x,y) of the location of vertex v1
        :param v2: Tuple (x,y) of the location of vertex v1
        """

        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def get_jacobian(self, v0=None, v1=None, v2=None):
        """
        Gives the current jacobian
        :param v0: If coordinate of vertex is given, these will be used instead of previously set
        :param v1: If coordinate of vertex is given, these will be used instead of previously set
        :param v2: If coordinate of vertex is given, these will be used instead of previously set
        :return: The jacobian
        """

        if v0 == None:
            # Grab vertices from storage
            v0 = self.v0
            v1 = self.v1
            v2 = self.v2

        J = np.array([[v1[0] - v0[0], v2[0] - v0[0]], [v1[1] - v0[1], v2[1] - v0[1]]])
        return J

    def get_inverse_jacobian(self, v0=None, v1=None, v2=None):
        """
        Gives the inverse of the current jacobian
        :param v0: If coordinate of vertex is given, these will be used instead of previously set
        :param v1: If coordinate of vertex is given, these will be used instead of previously set
        :param v2: If coordinate of vertex is given, these will be used instead of previously set
        :return: The inverse jacobian
        """

        if v0 == None:
            # Grab vertices from storage
            v0 = self.v0
            v1 = self.v1
            v2 = self.v2

        J = np.array([[v1[0] - v0[0], v2[0] - v0[0]], [v1[1] - v0[1], v2[1] - v0[1]]])

        # Check regularity
        detJ = np.linalg.det(J)
        if np.isclose(detJ, 0):
            print(J)
            raise ValueError('J is singular and can therfore not be inverted.')

        return np.linalg.inv(J)

    def get_determinant(self, v0=None, v1=None, v2=None):
        """
        Gives the determinant of the current jacobian
        :param v0: If coordinate of vertex is given, these will be used instead of previously set
        :param v1: If coordinate of vertex is given, these will be used instead of previously set
        :param v2: If coordinate of vertex is given, these will be used instead of previously set
        :return: The determinant
        """
        if v0 == None:
            # Grab vertices from storage
            v0 = self.v0
            v1 = self.v1
            v2 = self.v2

        J = np.array([[v1[0] - v0[0], v2[0] - v0[0]], [v1[1] - v0[1], v2[1] - v0[1]]])

        return np.linalg.det(J)
