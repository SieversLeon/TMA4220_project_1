#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for the code"""

import unittest
import numpy as np

from f_function import FFunction
from u_tilde_function import UTildeFunction


class TestCode(unittest.TestCase):
    """
    Useful test cases
    Todo:Add more test cases
    """

    def setUp(self):
        pass

    def test_f_function(self):
        """
        Tests the implemented f function
        :return:
        """
        f_test_instance = FFunction()
        self.assertAlmostEqual(f_test_instance.value((0.5,0.3)),0)
        self.assertAlmostEqual(f_test_instance.value((0.0, 0.0)), 0)
        self.assertAlmostEqual(f_test_instance.value((0.0, 1.0)), 0)
        self.assertAlmostEqual(f_test_instance.value((1.0, 0.0)), 0)
        self.assertAlmostEqual(f_test_instance.value((1.0, 1.0)), 0)

    def test_u_tile_function(self):
        """
        Tests the implemented u_tilde function
        :return:
        """

        def evaluate_lhs(x,u_tilde_test_instance):
            """
            Evaluates the left hand side of the PDE at a given position
            :param x: Coordinate to evaluate on
            :param u_tilde_test_instance: The solution to the PDE
            :return: The value of the LHS
            """
            v = u_tilde_test_instance.value(x)-u_tilde_test_instance.laplacian(x)
            return v

        u_tilde_test_instance = UTildeFunction()
        f_test_instance = FFunction()

        #Evaluate consistency with given solution
        x = (0,0.5)
        self.assertAlmostEqual(u_tilde_test_instance.value(x),1)

        #Evaluate correctness of solution regarding f
        x = (0.3,0.2)
        self.assertAlmostEqual(evaluate_lhs(x,u_tilde_test_instance)-f_test_instance.value(x), 0)

        #Evaluate compliance with boundary conditions

        #Dirichlet
        x = (0.5,0)
        self.assertAlmostEqual(u_tilde_test_instance.value(x),0)
        x = (0.5,1)
        self.assertAlmostEqual(u_tilde_test_instance.value(x),0)

        #Neumann
        x = (0,0.5)
        n = np.array([[-1,0]]).T
        self.assertAlmostEqual(np.asscalar(u_tilde_test_instance.gradient(x).T.dot(n)), 0)

        x = (1,0.2)
        n = np.array([[1,0]]).T
        self.assertAlmostEqual(np.asscalar(u_tilde_test_instance.gradient(x).T.dot(n)), 0)






if __name__ == '__main__':
    print("Starting unittest...")
    unittest.main()