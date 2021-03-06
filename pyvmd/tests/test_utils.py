"""
Tests for utilities.
"""
import VMD

from .utils import PyvmdTestCase


class TestPyvmdTestCase(PyvmdTestCase):
    """
    Test `PyvmdTestCase` class.
    """
    def test_teardown_deletes_molecules(self):
        VMD.molecule.new('foo')
        VMD.molecule.new('bar')

        class Foo(PyvmdTestCase):
            def runTest(self):
                pass

        Foo().tearDown()
        self.assertEqual(VMD.molecule.num(), 0)

    def test_assert_almost_equal_seqs(self):
        self.assertAlmostEqualSeqs([], [])
        self.assertAlmostEqualSeqs((), [])
        self.assertAlmostEqualSeqs(set(), [])
        self.assertAlmostEqualSeqs([1.0], [1.0])
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [1.0], [])
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [], [1.0])

        self.assertAlmostEqualSeqs([1.00000001], [1.0])
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [1.0000001], [1.0])

        self.assertAlmostEqualSeqs([1.0], [1.1], places=0)
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [1.0], [1.1], places=1)

        self.assertAlmostEqualSeqs([1.0], [1.0], delta=0.5)
        self.assertAlmostEqualSeqs([1.0], [1.1], delta=0.5)
        self.assertAlmostEqualSeqs([1.1], [1.0], delta=0.5)
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [1.0], [1.1], delta=0.05)

        self.assertRaises(TypeError, self.assertAlmostEqualSeqs, [1.0], [1.1], places=2, delta=0.5)

        self.assertAlmostEqualSeqs([1.0, -10, 42], [1.0, -10, 42])
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [1.0, -10, 42], [1.0, -10, 41])

        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, None, [])
        self.assertRaises(self.failureException, self.assertAlmostEqualSeqs, [], None)
