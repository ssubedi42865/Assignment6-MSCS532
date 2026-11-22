"""Tests for Part 2. Run: python test_data_structures.py"""
import unittest

from data_structures import (ArrayQueue, ArrayStack, DynamicArray, LinkedList,
                             LinkedQueue, LinkedStack, Matrix, TreeNode)


class TestArrays(unittest.TestCase):
    def test_dynamic_array(self):
        a = DynamicArray()
        for i in range(10):
            a.append(i)
        a.insert(0, 99)
        a.insert(5, 55)
        self.assertEqual(a.to_list(), [99, 0, 1, 2, 3, 55, 4, 5, 6, 7, 8, 9])
        self.assertEqual(a.delete(0), 99)
        self.assertEqual(a[4], 55)
        a[0] = -1
        self.assertEqual(a[0], -1)
        for _ in range(len(a)):
            a.delete(0)
        self.assertEqual(len(a), 0)
        with self.assertRaises(IndexError):
            a[0]

    def test_matrix(self):
        m = Matrix(2, 3)
        m.set(1, 2, 7)
        self.assertEqual(m.get(1, 2), 7)
        m.insert_row(1, [1, 2, 3])
        self.assertEqual(m.to_lists(), [[0, 0, 0], [1, 2, 3], [0, 0, 7]])
        m.delete_row(0)
        self.assertEqual(m.rows, 2)
        with self.assertRaises(IndexError):
            m.get(5, 5)


class TestStacksQueues(unittest.TestCase):
    def test_stacks(self):
        for S in (ArrayStack, LinkedStack):
            s = S()
            for i in range(20):
                s.push(i)
            self.assertEqual(s.peek(), 19)
            self.assertEqual([s.pop() for _ in range(20)], list(range(19, -1, -1)))
            with self.assertRaises(IndexError):
                s.pop()

    def test_queues(self):
        for Q in (ArrayQueue, LinkedQueue):
            q = Q()
            for i in range(10):
                q.enqueue(i)
            self.assertEqual([q.dequeue() for _ in range(5)], [0, 1, 2, 3, 4])
            for i in range(10, 20):  # forces wrap-around / growth
                q.enqueue(i)
            self.assertEqual(q.front(), 5)
            self.assertEqual([q.dequeue() for _ in range(15)], list(range(5, 20)))
            with self.assertRaises(IndexError):
                q.dequeue()


class TestLinkedList(unittest.TestCase):
    def test_ops(self):
        l = LinkedList()
        l.insert_back(2)
        l.insert_front(1)
        l.insert_back(4)
        l.insert_at(2, 3)
        self.assertEqual(list(l), [1, 2, 3, 4])
        self.assertTrue(l.search(3))
        self.assertTrue(l.delete_value(4))
        self.assertEqual(l.tail.value, 3)
        self.assertFalse(l.delete_value(42))
        l.reverse()
        self.assertEqual(list(l), [3, 2, 1])
        self.assertEqual(l.delete_front(), 3)
        self.assertEqual(len(l), 2)


class TestTree(unittest.TestCase):
    def test_tree(self):
        r = TreeNode("r")
        a = r.add_child("a")
        r.add_child("b")
        a.add_child("c")
        self.assertEqual(list(r.preorder()), ["r", "a", "c", "b"])


if __name__ == "__main__":
    unittest.main()
