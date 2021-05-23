#!/usr/bin/env python
import heapq
import unittest
from itertools import islice, repeat, count

from main import (
    wheel2357,
    spin,
    insert_prime,
    QueueItem,
    next_composite,
    adjust,
    sieve_,
    sieve,
    primes,
)


class TestWheel2357(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(list(islice(wheel2357(), 5)), [2, 4, 2, 4, 6])

    def test_repeats(self):
        self.assertEqual(len(list(islice(wheel2357(), 1000))), 1000)


class TestSpin(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(list(islice(spin(repeat(2), 0), 5)), [0, 2, 4, 6, 8])

    def test_starting_integer(self):
        self.assertEqual(list(islice(spin(repeat(2), 1), 5)), [1, 3, 5, 7, 9])

    def test_irregular_wheel(self):
        self.assertEqual(list(islice(spin([2, 3, 2, 3], 0), 5)), [0, 2, 5, 7, 10])


class TestInsertPrime(unittest.TestCase):
    def test_basic(self):
        table = []
        insert_prime(2, [2, 3, 4], table)
        self.assertEqual(len(table), 1)
        self.assertIsInstance(table[0], QueueItem)
        self.assertEqual(table[0].number, 4)
        self.assertEqual(list(table[0].generator), [4, 6, 8])

    def test_in_order(self):
        table = []
        insert_prime(2, [], table)
        insert_prime(5, [], table)
        insert_prime(3, [], table)
        self.assertEqual(heapq.heappop(table).number, 2 * 2)
        self.assertEqual(heapq.heappop(table).number, 3 * 3)
        self.assertEqual(heapq.heappop(table).number, 5 * 5)

    def test_generator_start(self):
        table = []
        insert_prime(2, count(start=3), table)
        self.assertEqual(next(table[0].generator), 6)


class TestNextComposite(unittest.TestCase):
    def test_basic(self):
        table = [QueueItem(4, count()), QueueItem(9, count())]
        self.assertEqual(next_composite(table), 4)


class TestAdjust(unittest.TestCase):
    def test_basic(self):
        table = [
            QueueItem(4, count(start=6, step=2)),
            QueueItem(9, count(start=12, step=3)),
        ]
        heapq.heapify(table)
        adjust(3, table)
        self.assertEqual([i.number for i in table], [4, 9])
        adjust(4, table)
        self.assertEqual([i.number for i in table], [6, 9])
        adjust(6, table)
        self.assertEqual([i.number for i in table], [8, 9])
        adjust(8, table)
        self.assertEqual([i.number for i in table], [9, 10])


class TestSieve_(unittest.TestCase):
    def test_basic(self):
        table = [QueueItem(4, count(start=6, step=2))]
        self.assertEqual(
            list(islice(sieve_(count(start=3), table), 5)), [3, 5, 7, 11, 13]
        )


class TestSieve(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(list(islice(sieve(count(start=2)), 5)), [2, 3, 5, 7, 11])


class TestPrimes(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(list(islice(primes(), 5)), [2, 3, 5, 7, 11])
        self.assertEqual(
            list(islice(primes(), 100)),
            [
                2,
                3,
                5,
                7,
                11,
                13,
                17,
                19,
                23,
                29,
                31,
                37,
                41,
                43,
                47,
                53,
                59,
                61,
                67,
                71,
                73,
                79,
                83,
                89,
                97,
                101,
                103,
                107,
                109,
                113,
                127,
                131,
                137,
                139,
                149,
                151,
                157,
                163,
                167,
                173,
                179,
                181,
                191,
                193,
                197,
                199,
                211,
                223,
                227,
                229,
                233,
                239,
                241,
                251,
                257,
                263,
                269,
                271,
                277,
                281,
                283,
                293,
                307,
                311,
                313,
                317,
                331,
                337,
                347,
                349,
                353,
                359,
                367,
                373,
                379,
                383,
                389,
                397,
                401,
                409,
                419,
                421,
                431,
                433,
                439,
                443,
                449,
                457,
                461,
                463,
                467,
                479,
                487,
                491,
                499,
                503,
                509,
                521,
                523,
                541,
            ],
        )


if __name__ == "__main__":
    unittest.main()
