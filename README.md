# Assignment 6: Order Statistics and Elementary Data Structures

## Files
- `selection.py`: median-of-medians (worst-case O(n)) and Randomized Quickselect (expected O(n))
- `benchmark.py`: timing comparison across sizes and input distributions
- `data_structures.py`: dynamic array, matrix, array and linked stacks/queues, singly linked list, rooted tree
- `benchmark_structures.py`: array vs linked-list timing comparison
- `test_selection.py`, `test_data_structures.py`: unit tests
- `Report_Part1_Selection.docx`, `Report_Part2_Data_Structures.docx`: reports

## How to run
Requires Python 3.8+ and no third-party packages. Run from the folder containing the code:

```
python3 -m unittest test_selection test_data_structures
python3 benchmark.py
python3 benchmark_structures.py
```

## Summary of findings
- Both selection algorithms scale linearly. Randomized Quickselect was about 2 to 2.5 times faster than median of medians, which has the better worst-case guarantee but a larger constant.
- Three-way partitioning handles duplicate-heavy input efficiently, and random pivots avoid slowdowns on sorted and reverse-sorted input.
- Arrays win on indexed access and memory use. Linked lists win on front insertion (20,000 front inserts: about 5,201 ms for the array versus 3.7 ms for the list). Stack and queue throughput was similar for both in Python.
