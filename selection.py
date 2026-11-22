"""Part 1: selection algorithms (k-th smallest element).

- median_of_medians_select: deterministic, worst-case O(n)
- randomized_select: Randomized Quickselect, expected O(n)

Both use 3-way partitioning, so arrays with many duplicates are handled
correctly and efficiently. k is 1-based (k=1 is the minimum).
Neither function modifies the input list.
"""
import random


def _check(arr, k):
    if not arr:
        raise ValueError("array is empty")
    if not 1 <= k <= len(arr):
        raise ValueError("k must satisfy 1 <= k <= len(arr)")


def _partition3(a, pivot):
    """Split a into (less, equal, greater) relative to pivot."""
    less, equal, greater = [], [], []
    for x in a:
        if x < pivot:
            less.append(x)
        elif x > pivot:
            greater.append(x)
        else:
            equal.append(x)
    return less, equal, greater


# ---------------------------------------------------------------- deterministic
def _median_of_five(group):
    group = sorted(group)  # constant-size sort: O(1)
    return group[(len(group) - 1) // 2]


def _mom_select(a, k):
    """Return k-th smallest (1-based) of list a using median of medians."""
    while True:
        n = len(a)
        if n <= 5:
            return sorted(a)[k - 1]
        # 1. split into groups of 5 and take each group's median
        medians = [_median_of_five(a[i:i + 5]) for i in range(0, n, 5)]
        # 2. recursively find the median of the medians (the pivot)
        pivot = _mom_select(medians, (len(medians) + 1) // 2)
        # 3. partition around the pivot
        less, equal, greater = _partition3(a, pivot)
        if k <= len(less):
            a = less
        elif k <= len(less) + len(equal):
            return pivot
        else:
            k -= len(less) + len(equal)
            a = greater


def median_of_medians_select(arr, k):
    """Deterministic selection in worst-case O(n) time."""
    _check(arr, k)
    return _mom_select(list(arr), k)


# ------------------------------------------------------------------- randomized
def randomized_select(arr, k, rng=random):
    """Randomized Quickselect: expected O(n) time."""
    _check(arr, k)
    a = list(arr)
    while True:
        if len(a) == 1:
            return a[0]
        pivot = a[rng.randrange(len(a))]
        less, equal, greater = _partition3(a, pivot)
        if k <= len(less):
            a = less
        elif k <= len(less) + len(equal):
            return pivot
        else:
            k -= len(less) + len(equal)
            a = greater
