"""Part 2: elementary data structures implemented from scratch.

- DynamicArray   : resizable array (insert, delete, access) with doubling
- Matrix         : 2-D array stored row-major in one flat DynamicArray-like list
- ArrayStack     : LIFO stack on an array
- ArrayQueue     : FIFO queue on a circular array
- LinkedList     : singly linked list (with tail pointer)
- LinkedStack / LinkedQueue : same ADTs built on linked nodes (for comparison)
- TreeNode       : rooted tree, left-child right-sibling representation

Only a fixed-size Python list is used as raw storage; resizing is done by hand.
"""


class DynamicArray:
    def __init__(self, capacity=4):
        self._data = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    def _resize(self, new_cap):
        new = [None] * new_cap
        for i in range(self._size):
            new[i] = self._data[i]
        self._data = new

    def __getitem__(self, i):  # O(1)
        if not 0 <= i < self._size:
            raise IndexError("index out of range")
        return self._data[i]

    def __setitem__(self, i, v):  # O(1)
        if not 0 <= i < self._size:
            raise IndexError("index out of range")
        self._data[i] = v

    def append(self, v):  # amortized O(1)
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        self._data[self._size] = v
        self._size += 1

    def insert(self, i, v):  # O(n): shift right
        if not 0 <= i <= self._size:
            raise IndexError("index out of range")
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        for j in range(self._size, i, -1):
            self._data[j] = self._data[j - 1]
        self._data[i] = v
        self._size += 1

    def delete(self, i):  # O(n): shift left
        if not 0 <= i < self._size:
            raise IndexError("index out of range")
        v = self._data[i]
        for j in range(i, self._size - 1):
            self._data[j] = self._data[j + 1]
        self._size -= 1
        self._data[self._size] = None
        if 0 < self._size <= len(self._data) // 4 and len(self._data) > 4:
            self._resize(len(self._data) // 2)
        return v

    def to_list(self):
        return [self._data[i] for i in range(self._size)]


class Matrix:
    """rows x cols matrix, row-major flat storage; access O(1)."""

    def __init__(self, rows, cols, fill=0):
        self.rows, self.cols = rows, cols
        self._data = [fill] * (rows * cols)

    def _idx(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise IndexError("index out of range")
        return r * self.cols + c

    def get(self, r, c):
        return self._data[self._idx(r, c)]

    def set(self, r, c, v):
        self._data[self._idx(r, c)] = v

    def insert_row(self, r, values):  # O(rows*cols): rebuild storage
        if not 0 <= r <= self.rows or len(values) != self.cols:
            raise ValueError("bad row")
        start = r * self.cols
        self._data = self._data[:start] + list(values) + self._data[start:]
        self.rows += 1

    def delete_row(self, r):  # O(rows*cols)
        if not 0 <= r < self.rows:
            raise IndexError("index out of range")
        start = r * self.cols
        self._data = self._data[:start] + self._data[start + self.cols:]
        self.rows -= 1

    def to_lists(self):
        return [self._data[r * self.cols:(r + 1) * self.cols] for r in range(self.rows)]


class ArrayStack:
    def __init__(self):
        self._a = DynamicArray()

    def push(self, v):  # amortized O(1)
        self._a.append(v)

    def pop(self):  # O(1) (amortized with shrinking)
        if not self._a:
            raise IndexError("pop from empty stack")
        return self._a.delete(len(self._a) - 1)

    def peek(self):  # O(1)
        if not self._a:
            raise IndexError("peek from empty stack")
        return self._a[len(self._a) - 1]

    def is_empty(self):
        return len(self._a) == 0

    def __len__(self):
        return len(self._a)


class ArrayQueue:
    """Circular-buffer queue: enqueue/dequeue amortized O(1)."""

    def __init__(self, capacity=4):
        self._data = [None] * capacity
        self._head = 0
        self._size = 0

    def __len__(self):
        return self._size

    def _grow(self):
        new = [None] * (2 * len(self._data))
        for i in range(self._size):
            new[i] = self._data[(self._head + i) % len(self._data)]
        self._data, self._head = new, 0

    def enqueue(self, v):
        if self._size == len(self._data):
            self._grow()
        self._data[(self._head + self._size) % len(self._data)] = v
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        v = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % len(self._data)
        self._size -= 1
        return v

    def front(self):
        if self._size == 0:
            raise IndexError("front of empty queue")
        return self._data[self._head]

    def is_empty(self):
        return self._size == 0


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, nxt=None):
        self.value, self.next = value, nxt


class LinkedList:
    """Singly linked list with head and tail pointers."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert_front(self, v):  # O(1)
        self.head = _Node(v, self.head)
        if self.tail is None:
            self.tail = self.head
        self._size += 1

    def insert_back(self, v):  # O(1) thanks to tail
        node = _Node(v)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def insert_at(self, i, v):  # O(i)
        if not 0 <= i <= self._size:
            raise IndexError("index out of range")
        if i == 0:
            return self.insert_front(v)
        if i == self._size:
            return self.insert_back(v)
        prev = self.head
        for _ in range(i - 1):
            prev = prev.next
        prev.next = _Node(v, prev.next)
        self._size += 1

    def delete_front(self):  # O(1)
        if self.head is None:
            raise IndexError("delete from empty list")
        v = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return v

    def delete_value(self, v):  # O(n); returns True if removed
        prev, cur = None, self.head
        while cur:
            if cur.value == v:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur is self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def search(self, v):  # O(n)
        cur = self.head
        while cur:
            if cur.value == v:
                return True
            cur = cur.next
        return False

    def __iter__(self):  # traversal O(n)
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def reverse(self):  # O(n)
        prev, cur = None, self.head
        self.tail = self.head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev


class LinkedStack:
    def __init__(self):
        self._l = LinkedList()

    def push(self, v):  # O(1) worst case
        self._l.insert_front(v)

    def pop(self):  # O(1) worst case
        if len(self._l) == 0:
            raise IndexError("pop from empty stack")
        return self._l.delete_front()

    def peek(self):
        if len(self._l) == 0:
            raise IndexError("peek from empty stack")
        return self._l.head.value

    def __len__(self):
        return len(self._l)


class LinkedQueue:
    def __init__(self):
        self._l = LinkedList()

    def enqueue(self, v):  # O(1) worst case
        self._l.insert_back(v)

    def dequeue(self):  # O(1) worst case
        if len(self._l) == 0:
            raise IndexError("dequeue from empty queue")
        return self._l.delete_front()

    def front(self):
        if len(self._l) == 0:
            raise IndexError("front of empty queue")
        return self._l.head.value

    def __len__(self):
        return len(self._l)


class TreeNode:
    """Rooted tree with unbounded children: left-child, right-sibling."""

    def __init__(self, value):
        self.value = value
        self.child = None    # leftmost child
        self.sibling = None  # next sibling

    def add_child(self, value):  # O(number of children)
        node = TreeNode(value)
        if self.child is None:
            self.child = node
        else:
            cur = self.child
            while cur.sibling:
                cur = cur.sibling
            cur.sibling = node
        return node

    def children(self):
        cur = self.child
        while cur:
            yield cur
            cur = cur.sibling

    def preorder(self):  # O(n)
        yield self.value
        for c in self.children():
            yield from c.preorder()
