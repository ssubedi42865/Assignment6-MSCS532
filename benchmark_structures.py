"""Part 2 empirical comparison: array vs linked stacks and queues.

Run: python benchmark_structures.py
"""
import time

from data_structures import (ArrayQueue, ArrayStack, DynamicArray, LinkedList,
                             LinkedQueue, LinkedStack)

N = 200_000


def t(fn):
    start = time.perf_counter()
    fn()
    return (time.perf_counter() - start) * 1000


def stack_run(S):
    def f():
        s = S()
        for i in range(N):
            s.push(i)
        for _ in range(N):
            s.pop()
    return f


def queue_run(Q):
    def f():
        q = Q()
        for i in range(N):
            q.enqueue(i)
        for _ in range(N):
            q.dequeue()
    return f


def front_insert_array(n=20_000):
    def f():
        a = DynamicArray()
        for i in range(n):
            a.insert(0, i)
    return f


def front_insert_list(n=20_000):
    def f():
        l = LinkedList()
        for i in range(n):
            l.insert_front(i)
    return f


def middle_access_array(n=20_000):
    a = DynamicArray()
    for i in range(n):
        a.append(i)
    return lambda: [a[n // 2] for _ in range(1000)]


def middle_access_list(n=20_000):
    l = LinkedList()
    for i in range(n):
        l.insert_back(i)

    def f():
        for _ in range(1000):
            for j, _v in enumerate(l):
                if j == n // 2:
                    break
    return f


if __name__ == "__main__":
    print(f"{N} push/enqueue + {N} pop/dequeue (ms)")
    print(f"  ArrayStack   {t(stack_run(ArrayStack)):8.1f}")
    print(f"  LinkedStack  {t(stack_run(LinkedStack)):8.1f}")
    print(f"  ArrayQueue   {t(queue_run(ArrayQueue)):8.1f}")
    print(f"  LinkedQueue  {t(queue_run(LinkedQueue)):8.1f}")
    print("20,000 front insertions (ms)")
    print(f"  DynamicArray {t(front_insert_array()):8.1f}")
    print(f"  LinkedList   {t(front_insert_list()):8.1f}")
    print("1,000 accesses to middle element of 20,000 items (ms)")
    print(f"  DynamicArray {t(middle_access_array()):8.1f}")
    print(f"  LinkedList   {t(middle_access_list()):8.1f}")
