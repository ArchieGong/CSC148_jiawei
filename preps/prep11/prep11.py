"""Prep 11 Synthesize: Recursive Sorting Algorithms

=== CSC148 Summer 2021 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu and Diane Horton

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu and Diane Horton

=== Module Description ===
This file includes the recursive sorting algorithms from this week's prep
readings, and two short programming exercises to extend your learning about
these algorithms in different ways.
"""
from typing import Any


################################################################################
# Mergesort and Quicksort
################################################################################
def mergesort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of mergesort; it does not mutate the
    input list.

    >>> mergesort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Divide the list into two parts, and sort them recursively.
        mid = len(lst) // 2
        left_sorted = mergesort(lst[:mid])
        right_sorted = mergesort(lst[mid:])

        # Merge the two sorted halves. Need a helper here!
        return _merge(left_sorted, right_sorted)


def _merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Precondition: <lst1> and <lst2> are sorted.
    """
    index1 = 0
    index2 = 0
    merged = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1

    # Now either index1 == len(lst1) or index2 == len(lst2).

    # The remaining elements of the other list
    # can all be added to the end of <merged>.
    # Note that at most ONE of lst1[index1:] and lst2[index2:]
    # is non-empty, but to keep the code simple, we include both.
    return merged + lst1[index1:] + lst2[index2:]


def quicksort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of quicksort; it does not mutate the
    input list.

    >>> quicksort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Pick pivot to be first element.
        # Could make lots of other choices here (e.g., last, random)
        pivot = lst[0]

        # Partition rest of list into two halves
        smaller, bigger = _partition(lst[1:], pivot)

        # Recurse on each partition
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)

        # Return! Notice the simple combining step
        return smaller_sorted + [pivot] + bigger_sorted


def _partition(lst: list, pivot: Any) -> tuple[list, list]:
    """Return a partition of <lst> with the chosen pivot.

    Return two lists, where the first contains the items in <lst>
    that are <= pivot, and the second is the items in <lst> that are > pivot.
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger


################################################################################
# Synthesize exercises
################################################################################
def mergesort3(lst: list) -> list:
    """Return a sorted version of <lst> using three-way mergesort.

    Three-way mergesort is similar to mergesort, except:
        - it divides the input list into *three* lists of (almost) equal length
        - the main helper merge3 takes in *three* sorted lists, and returns
          a sorted list that contains elements from all of its inputs.

    HINT: depending on your impementation, you might need another base case
    when len(lst) == 2 to avoid an infinite recursion error.

    >>> mergesort3([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    elif len(lst) == 2:
        return [min(lst), max(lst)]
    else:
        n = len(lst)
        first_part = lst[:n // 3]
        second_part = lst[n // 3: 2 * n // 3]
        third_part = lst[2 * n // 3:]

        first_sort = mergesort3(first_part)
        second_sort = mergesort3(second_part)
        third_sort = mergesort3(third_part)

        return merge3(first_sort, second_sort, third_sort)


def merge3(lst1: list, lst2: list, lst3: list) -> list:
    """Return a sorted list with the elements in the given input lists.

    Precondition: <lst1>, <lst2>, and <lst3> are all sorted.

    This *must* be implemented using the same approach as _merge; in particular,
    it should use indexes to keep track of where you are in each list.
    This will keep your implementation efficient, which we will be checking for.

    Since this involves some detailed work with indexes, we recommend splitting
    up your code into one or more helpers to divide up (and test!) each part
    separately.
    """

    # Note that we've made it public because we'll be testing it directly.
    # You may call _merge in this function, but you should only call it ONCE
    # at most.
    # i.e. merge the three lists together and use _merge as needed when
    # there's only two lists left to merge.
    merged1 = _merge(lst1, lst2)
    merged2 = _merge(merged1, lst3)
    return merged2


def kth_smallest(lst: list, k: int) -> Any:
    """Return the <k>-th smallest element in <lst>.

    Raise IndexError if k < 0 or k >= len(lst).
    Note: for convenience, k counts from 0, so kth_smallest(lst, 0) == min(lst).

    Precondition: <lst> does not contain duplicates.

    >>> kth_smallest([10, 20, -4, 3], 0)
    -4
    >>> kth_smallest([10, 20, -4, 3], 2)
    10
    """
    # You may *not* sort the list here (this is easy but not very efficient).
    # Instead, use the following approach, based on quicksort:
    #   1. partition the list based on a chosen pivot:
    #       smaller, bigger = partition(...)
    #   2. Compare len(smaller) against k, and use the result to decide which
    #      list to recurse on (if any). As in your BST prep, you should only
    #      make one recursive call into either <smaller> or <bigger>, not both!
    if k < 0 or k >= len(lst):
        raise IndexError
    pivot = lst[0]
    small, big = _partition(lst[1:], pivot)
    if len(small) == k:
        return pivot
    elif len(small) > k:
        return kth_smallest(small, k)
    else:
        return kth_smallest(big, k - len(small) - 1)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={'disable': ['E1136']})
