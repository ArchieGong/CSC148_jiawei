from typing import List
def insert_after(lst: List[int], n1: int, n2: int) -> None:
    """After each occurrence of <n1> in <lst>, insert <n2>.
    >>> lst = [5, 1, 2, 1, 6]
    >>> insert_after(lst, 1, 99)
    >>> lst
    [5, 1, 99, 2, 1, 99, 6]
    """
    i = 0
    while i < len(lst):
        if lst[i] == n1:
            lst.insert(i+1, n2)
        i += 1
if __name__ == '__main__':
    import doctest
    doctest.testmod()

