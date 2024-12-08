def remove_first_double(self) -> None:
    #return if there are less than 2 nodes
    if self._first is None or self._first.next is None:
        return None
    #Else, try to find the first double.
    temp = self._first
    while (temp.next is None) and (temp.next.item != temp.item):
        temp = temp.next
    # 1) temp.next is None -- Reach the end, no double fuond
    # 2) temp.next.item == temp.item, found double
    if temp.next is not None:
        temp.next = temp.next.next


def swap(self, i: int, j: int) -> None:
    node_i = self._first
    for _ in range(i):
        if node_i is None:
            raise IndexError
        else node_i = node_i.next

    node_j = self._first
    for _ in range(j):
        if node_j is None:
            raise IndexError
        else node_j = node_j.next

    if node_i is None or node_j is None:
        raise IndexError

    node_i.item, node_j.item = node_j.item, node_i.item

def insert_new_items(self, new_item : list[Any]) -> list[Any]:
    temp = self._first
    i=0
    while (temp is not None) and (i < len(new_item)):
        #add the node
        new_node = _Node(new_item[i])
        new_node.next = temp.next
        temp.next = new_node

        #move to the next
        temp = temp.next.next
        i = i+1

    return new_items[i:]


