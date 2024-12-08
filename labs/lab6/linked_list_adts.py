"""Lab 6: Linked Lists and ADTs

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node, and ADT implementations using the linked list.

All of the code from lecture is here, as well as some exercises to work on.
"""
from __future__ import annotations
from typing import Any, Optional


################################################################################
# Below is code for a LinkedList
# You may replace this with code you've written in Lab 5 or add additional
# methods and augmentations as you deem necessary.
################################################################################
class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: Optional[_Node]

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, items: Optional[list] = None) -> None:
        """Initialize a new empty linked list containing the given items.
        """
        if not items:  # No items and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            curr = self._first
            for item in items[1:]:
                curr.next = _Node(item)
                curr = curr.next

    # ------------------------------------------------------------------------
    # Methods from lecture/readings
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        # >>> LinkedList([]).is_empty()
        # True
        # >>> LinkedList([1, 2, 3]).is_empty()
        # False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        # >>> str(LinkedList([1, 2, 3]))
        # '[1 -> 2 -> 3]'
        # >>> str(LinkedList([]))
        # '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __getitem__(self, index: int) -> Any:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.
        """
        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        assert curr is None or curr_index == index

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def insert(self, index: int, item: Any) -> None:
        """Insert a the given item at the given index in this list.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of the list is okay.

        # >>> lst = LinkedList([1, 2, 10, 200])
        # >>> lst.insert(2, 300)
        # >>> str(lst)
        # '[1 -> 2 -> 300 -> 10 -> 200]'
        # >>> lst.insert(5, -1)
        # >>> str(lst)
        # '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        # >>> lst.insert(100, 2)
        # Traceback (most recent call last):
        # IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next

    def append(self, item: Any) -> None:
        """Add the given item to the end of this linked list."""
        curr = self._first
        if curr is None:
            new_node = _Node(item)
            self._first = new_node
        else:
            while curr.next is not None:
                curr = curr.next

            # After the loop, curr is the last node in the LinkedList.
            # assert curr is not None and curr.next is None
            new_node = _Node(item)
            curr.next = new_node

    def pop(self, index: int) -> Any:
        """Remove and return the item at position <index>.
        Raise IndexError if index >= len(self) or index < 0.
        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.pop(1)
        2
        >>> lst.pop(2)
        200
        >>> lst.pop(148)
        Traceback (most recent call last):
        IndexError
        >>> lst.pop(0)
        1
        """
        # TODO: Implement this method. You may use the code from lecture,
        #       but we recommend trying it yourself!
        #       We've started this for you, covering the case where the index
        #       is less than 0 or if our LinkedList is empty.
        if index < 0 or self.is_empty():
            raise IndexError
        else:
            temp = self._first
            location = 0
            if index == 0:
                result2 = self._first.item
                self._first = temp.next
                return result2
            else:
                while temp.next is not None and location < index-1:
                    temp = temp.next
                    location += 1

                if temp.next == None:
                    raise IndexError
                else:
                    result=temp.next.item
                    temp.next = temp.next.next
                    return result




################################################################################

class LinkedListStack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.

    This implementation of a Stack uses a Linked List for its items.
    """

    # === Private Attributes ===
    # _items:
    #     The items currently in this Stack.

    def __init__(self) -> None:
        """Initialize a new empty LinkedListStack."""
        self._items = LinkedList()

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = LinkedListStack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        # TODO: Implement this method
        return self._items._first is None

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        # TODO: Implement this method
        if self.is_empty() is True:
            self._items._first = item
        else:
            self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an IndexError if this stack is empty.

        >>> s = LinkedListStack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        # TODO: Implement this method
        if self._items._first is None:
            raise IndexError
        else:
            temp = self._items._first
            if temp.next == None:
                self._items._first = None
            else:
                while temp.next.next is not None:
                    temp = temp.next
                result = temp.next.item
                temp.next = None
                return result

#self._items.pop()

class LinkedListQueue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.

    This implementation of a Queue uses a Linked List for its items.
    """

    # === Private Attributes ===
    # _items:
    #     The items currently in this Queue.

    def __init__(self) -> None:
        """Initialize a new empty LinkedListQueue."""
        self._items = LinkedList()

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = LinkedListQueue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        # TODO: Implement this method

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        # TODO: Implement this method

    def dequeue(self) -> Any:
        """Remove and return the item at the front of this queue.

        Raise an IndexError if this Queue is empty.

        >>> q = LinkedListQueue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        # TODO: Implement this method


if __name__ == '__main__':
    import doctest

    doctest.testmod()
