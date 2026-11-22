"""Part 1 empirical analysis: compare selection algorithms on several inputs.

Run: python benchmark.py
Prints a table of median-of-3-runs times (ms) for finding the median (k = n/2),
and compares against sorting as a baseline.
"""
import random
import time

from selection import median_of_medians_select, randomized_select

SIZES = [1_000, 10_000, 100_000, 500_000]
DISTRIBUTIONS = {
    "random": lambda n: [random.randint(0, 10 * n) for _ in range(n)],
    "sorted": lambda n: list(range(n)),
    "reverse": lambda n: list(range(n, 0, -1)),
    "duplicates": lambda n: [random.randint(0, 9) for _ in range(n)],
}
ALGOS = {
    "median-of-medians": median_of_medians_select,
    "randomized": randomized_select,
    "sort baseline": lambda a, k: sorted(a)[k - 1],
}


def timeit(fn, arr, k, repeats=3):
    times = []
    for _ in range(repeats):
        t = time.perf_counter()
        fn(arr, k)
        times.append(time.perf_counter() - t)
    return sorted(times)[len(times) // 2] * 1000


def main():
    random.seed(42)
    print(f"{'distribution':<12}{'n':>9}" + "".join(f"{name:>20}" for name in ALGOS))
    for dist, gen in DISTRIBUTIONS.items():
        for n in SIZES:
            arr = gen(n)
            k = n // 2
            expected = sorted(arr)[k - 1]
            row = f"{dist:<12}{n:>9}"
            for name, fn in ALGOS.items():
                assert fn(arr, k) == expected, (name, dist, n)
                row += f"{timeit(fn, arr, k):>17.2f} ms"
            print(row)


if __name__ == "__main__":
    main()
