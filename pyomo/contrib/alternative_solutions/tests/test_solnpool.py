from numpy.testing import assert_array_almost_equal
from collections import Counter

import pyomo.environ as pe
import pyomo.common.unittest as unittest

from pyomo.contrib.alternative_solutions import gurobi_generate_solutions
import pyomo.contrib.alternative_solutions.tests.test_cases as tc


@unittest.skipUnless(
        pe.SolverFactory("gurobi").available(), "Gurobi MIP solver not available"
)
@unittest.pytest.mark.solver("gurobi")
class TestSolnPoolUnit(unittest.TestCase):
    """
    Cases to cover:

        LP feasibility (for an LP just one solution should be returned since gurobi cannot enumerate over continuous vars)

        Pass at least one solver option to make sure that work, e.g. time limit

        We need a utility to check that a two sets of solutions are the same.
        Maybe this should be an AOS utility since it may be a thing we will want to do often.
    """

    def test_ip_feasibility(self):
        """
        Enumerate all solutions for an ip: triangle_ip.

        Check that the correct number of alternate solutions are found.
        """
        m = tc.get_triangle_ip()
        results = gurobi_generate_solutions(m, num_solutions=100)
        objectives = [round(result.objective[1], 2) for result in results]
        actual_solns_by_obj = m.num_ranked_solns
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, actual_solns_by_obj)

    def test_ip_num_solutions(self):
        """
        Enumerate 8 solutions for an ip: triangle_ip.

        Check that the correct number of alternate solutions are found.
        """
        m = tc.get_triangle_ip()
        results = gurobi_generate_solutions(m, num_solutions=8)
        assert len(results) == 8
        objectives = [round(result.objective[1], 2) for result in results]
        actual_solns_by_obj = [6, 2]
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, actual_solns_by_obj)

    def test_mip_feasibility(self):
        """
        Enumerate all solutions for a mip: indexed_pentagonal_pyramid_mip.

        Check that the correct number of alternate solutions are found.
        """
        m = tc.get_indexed_pentagonal_pyramid_mip()
        results = gurobi_generate_solutions(m, num_solutions=100)
        objectives = [round(result.objective[1], 2) for result in results]
        actual_solns_by_obj = m.num_ranked_solns
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, actual_solns_by_obj)

    def test_mip_rel_feasibility(self):
        """
        Enumerate solutions for a mip: indexed_pentagonal_pyramid_mip.

        Check that only solutions within a relative tolerance of 0.2 are
        found.
        """
        m = tc.get_pentagonal_pyramid_mip()
        results = gurobi_generate_solutions(m, num_solutions=100, rel_opt_gap=0.2)
        objectives = [round(result.objective[1], 2) for result in results]
        actual_solns_by_obj = m.num_ranked_solns[0:2]
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, actual_solns_by_obj)

    def test_mip_rel_feasibility_options(self):
        """
        Enumerate solutions for a mip: indexed_pentagonal_pyramid_mip.

        Check that only solutions within a relative tolerance of 0.2 are
        found.
        """
        m = tc.get_pentagonal_pyramid_mip()
        results = gurobi_generate_solutions(
            m, num_solutions=100, solver_options={"PoolGap": 0.2}
        )
        objectives = [round(result.objective[1], 2) for result in results]
        actual_solns_by_obj = m.num_ranked_solns[0:2]
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, actual_solns_by_obj)

    def test_mip_abs_feasibility(self):
        """
        Enumerate solutions for a mip: indexed_pentagonal_pyramid_mip.

        Check that only solutions within an absolute tolerance of 1.99 are
        found.
        """
        m = tc.get_pentagonal_pyramid_mip()
        results = gurobi_generate_solutions(m, num_solutions=100, abs_opt_gap=1.99)
        objectives = [round(result.objective[1], 2) for result in results]
        actual_solns_by_obj = m.num_ranked_solns[0:3]
        unique_solns_by_obj = [val for val in Counter(objectives).values()]
        assert_array_almost_equal(unique_solns_by_obj, actual_solns_by_obj)

    def test_mip_no_time(self):
        """
        Enumerate solutions for a mip: indexed_pentagonal_pyramid_mip.

        Check that no solutions are returned with a timelimit of 0.
        """
        m = tc.get_pentagonal_pyramid_mip()
        # Use quiet=False to test error message
        results = gurobi_generate_solutions(
            m, num_solutions=100, solver_options={"TimeLimit": 0.0}, quiet=False
        )
        assert len(results) == 0


if __name__ == "__main__":
    unittest.main()
