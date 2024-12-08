"""CSC148 Lab 1

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module illustrates a simple unit test for our binary_search function.
"""
from search import binary_search


def test_search() -> None:
    """Simple test for binary_search."""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 5) == -1

#def test_single_item_list()->None:
   # assert binary_search([5], 5) == 0

if __name__ == '__main__':
    import pytest
    pytest.main(['test_search.py'])
