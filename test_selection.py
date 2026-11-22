"""Correctness tests for Part 1. Run: python test_selection.py"""
import random
import unittest

from selection import median_of_medians_select, randomized_select

ALGOS = [median_of_medians_select, randomized_select]


class TestSelection(unittest.TestCase):
    def test_random_arrays_every_k(self):
        random.seed(1)
        for fn in ALGOS:
            for n in [1, 2, 3, 5, 6, 11, 50]:
                arr = [random.randint(-20, 20) for _ in range(n)]
                s = sorted(arr)
                for k in range(1, n + 1):
                    self.assertEqual(fn(arr, k), s[k - 1])

    def test_duplicates_and_constant(self):
        for fn in ALGOS:
            self.assertEqual(fn([7] * 1000, 500), 7)
            arr = [1, 1, 2, 2, 2, 3, 3, 3, 3]
            for k in range(1, 10):
                self.assertEqual(fn(arr, k), sorted(arr)[k - 1])

    def test_sorted_and_reverse(self):
        for fn in ALGOS:
            self.assertEqual(fn(list(range(1000)), 250), 249)
            self.assertEqual(fn(list(range(1000, 0, -1)), 250), 250)

    def test_input_not_modified(self):
        for fn in ALGOS:
            arr = [5, 3, 9, 1]
            fn(arr, 2)
            self.assertEqual(arr, [5, 3, 9, 1])

    def test_invalid(self):
        for fn in ALGOS:
            with self.assertRaises(ValueError):
                fn([], 1)
            with self.assertRaises(ValueError):
                fn([1, 2, 3], 0)
            with self.assertRaises(ValueError):
                fn([1, 2, 3], 4)


if __name__ == "__main__":
    unittest.main()
