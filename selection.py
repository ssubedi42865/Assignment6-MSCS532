"""Selection algorithms for finding the kth smallest value in an array."""

import random


def randomized_quickselect(values, k):
    """Return the kth smallest value, counting duplicates separately.

    k starts at 1. The original input is preserved.
    Raises ValueError if k is outside the range 1 through len(values).
    """
    if not 1 <= k <= len(values):
        raise ValueError("k must be between 1 and the number of values")

    items = list(values)
    target = k - 1
    left, right = 0, len(items) - 1

    while left < right:
        pivot = items[random.randint(left, right)]

        # Split the active range into values below, equal to, and above pivot.
        lower, current, upper = left, left, right
        while current <= upper:
            if items[current] < pivot:
                items[lower], items[current] = items[current], items[lower]
                lower += 1
                current += 1
            elif items[current] > pivot:
                items[current], items[upper] = items[upper], items[current]
                upper -= 1
                # The value swapped in from the right still needs inspection.
            else:
                current += 1

        if target < lower:
            right = lower - 1
        elif target > upper:
            left = upper + 1
        else:
            return pivot

    return items[left]


if __name__ == "__main__":
    numbers = [9, 2, 7, 2, 5]
    for rank in range(1, len(numbers) + 1):
        print(f"Rank {rank}: {randomized_quickselect(numbers, rank)}")