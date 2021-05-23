#!/usr/bin/env python

"""
Implementation of an infinite sieve of Eratosthenes.

Based on the paper "The Genuine Sieve of Eratosthenes" by Melissa E O'Neill.
Part of experiments for efficient prime generators.

Link to paper: https://www.cs.hmc.edu/~oneill/papers/Sieve-JFP.pdf

To prevent recursion overflow errors in Python, recursive functions have been converted to be non recursive instead.
"""

import heapq
from dataclasses import dataclass, field
from itertools import islice, tee, accumulate, repeat, chain
from typing import Generator, List, Iterator

__author__ = "Lucas Moeskops"
__copyright__ = "Copyright 2021"
__credits__ = ["Lucas Moeskops", "Melissa E O'Neill"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Lucas Moeskops"
__email__ = "lucasmoeskops@gmail.com"
__status__ = "Production"


@dataclass(order=True)
class QueueItem:
    number: int
    generator: Iterator[int] = field(compare=False)


PQ = List[QueueItem]
NumberGenerator = Generator[int, None, None]


def wheel2357() -> NumberGenerator:
    yield from chain.from_iterable(
        repeat(
            (
                2,
                4,
                2,
                4,
                6,
                2,
                6,
                4,
                2,
                4,
                6,
                6,
                2,
                6,
                4,
                2,
                6,
                4,
                6,
                8,
                4,
                2,
                4,
                2,
                4,
                8,
                6,
                4,
                6,
                2,
                4,
                6,
                2,
                6,
                6,
                4,
                2,
                4,
                6,
                2,
                6,
                4,
                2,
                4,
                2,
                10,
                2,
                10,
            )
        )
    )


def spin(wheel: Iterator[int], n: int) -> NumberGenerator:
    yield from accumulate(wheel, initial=n)


def insert_prime(p: int, xs: Iterator[int], table: PQ) -> None:
    heapq.heappush(table, QueueItem(p * p, (x * p for x in xs)))


def next_composite(table: PQ) -> int:
    return table[0].number


def adjust(x: int, table: PQ) -> None:
    n = table[0].number
    while n <= x:
        xs = table[0].generator
        n_ = next(xs)
        heapq.heappop(table)
        heapq.heappush(table, QueueItem(n_, xs))
        n = table[0].number


def sieve_(xs: Iterator[int], table: PQ) -> None:
    while True:
        x = next(xs)
        if next_composite(table) <= x:
            adjust(x, table)
        else:
            yield x
            xs_: Iterator[int]
            xs, xs_ = tee(xs, 2)
            insert_prime(x, xs_, table)


def sieve(xs: Iterator[int]) -> NumberGenerator:
    x = next(xs)
    xs: Iterator[int]
    xs_: Iterator[int]
    xs, xs_ = tee(xs, 2)
    yield x
    pq = []
    insert_prime(x, xs_, pq)
    yield from sieve_(xs, pq)


def primes() -> NumberGenerator:
    yield from (2, 3, 5, 7)
    yield from sieve(spin(wheel2357(), 11))


def print_first_1000_primes() -> None:
    print(list(islice(primes(), 1000)))


if __name__ == "__main__":
    print_first_1000_primes()
