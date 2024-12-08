
def slice_list(lst: list[Any], n: int) -> list[list[Any]]:
    """Return a list containing slices of <lst> in order. Each slice is a
    list of size <n> containing the next <n> elements in <lst>.

    The last slice may contain fewer than <n> elements in order to make sure
    that the returned list contains all elements in <lst>.

    Note: Here is a less efficient implementation of this function:
        slices = []
        for i in range(0, len(lst), n):
            slices.append(lst[i:i + n])
        return slices

    Preconditions:
        - n <= len(lst)

    >>> slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    True
    >>> slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [False]]
    True
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


# Provided helper
def find_best_addition_to_group(survey: Survey, members: list[Student],
                                non_members: list[Student]) -> Student:
    """Find the best student in <non_members> to add to the group <members>,
    i.e., the student that increases the group's score the most (or decreases
    it the least).

    Preconditions:
        - len(non_members) > 0
    """
    best_score = float('-inf')
    best_student = None
    for student in non_members:
        score = survey.score_students(members + [student])
        if score > best_score:
            best_score = score
            best_student = student
    return best_student


# Provided helper
def random_swap(lst: list[list[Any]], seed: int = 0) -> None:
    """Swap two random elements from distinct sublists of <lst>.

    Uses a random seed <seed> to allow for repeatable results.
    Note: This function mutates <lst>

    Preconditions:
        - len(lst) >= 2
        - each sub list has length >= 1

    >>> l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> random_swap(l, seed=0)
    >>> l # The 4 and the 8 have swapped positions
    [[1, 2, 3], [8, 5, 6], [7, 4, 9]]
    >>> random_swap(l, seed=0)
    >>> # Now we use the same seed again, so the positions where swapping
    >>> # occurs are the same as before, and we end up with the original list.
    >>> l
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> for i in range(20):
    ...     random_swap(l, seed=i)
    >>> l # After many swaps the order will be random
    [[7, 2, 8], [1, 5, 4], [3, 9, 6]]
    """
    rnd = random.Random(seed)
    rng = range(len(lst))
    # find two distinct sub lists
    l_1, l_2 = rnd.sample(rng, 2)
    # find an element in each sub list
    i_1 = rnd.randint(0, len(lst[l_1]) - 1)
    i_2 = rnd.randint(0, len(lst[l_2]) - 1)
    # swap the elements
    lst[l_1][i_1], lst[l_2][i_2] = lst[l_2][i_2], lst[l_1][i_1]


# Provided helper
def total_score(survey: Survey, groups: list[list[Student]]) -> float:
    """Return the total score of the grouping of students in <groups> according
    to <survey>.

    Note: This function does the same thing as the following:
            g = Grouping()
            for group in groups:
                g.add_group(Group(group))
            return survey.score_grouping(g)

    Preconditions:
        - len(groups) > 0
    """
    return sum(survey.score_students(group) for group in groups) / len(groups)


# Provided helper
def accept(old_score: float, new_score: float, temperature: float, seed: int
           ) -> bool:
    """If <new_score> is at least as high as <old_score>, return True.
    Otherwise, return True with probability
        exp((<new_score> - <old_score>) / <temperature>)
    unless <temperature> is 0, in which case, return False.
    """
    diff = new_score - old_score

    if diff >= 0:
        return True
    elif temperature == 0:
        return False

    rnd = random.Random(seed)
    return rnd.random() < math.exp(diff / temperature)





    students = list(course.get_students())
    sliced_stu = slice_list(students, self.group_size)

    best_grouping = sliced_stu
    best_score = total_score(survey, best_grouping)
    cur_score = best_score
    cur_sliced = best_grouping

    cur_temp = self._initial_t
    sa = Grouping()

    for i in range(self._iteration):
        copy_sliced = copy.deepcopy(cur_sliced)
        random_swap(cur_sliced, seed=i)
        new_score = total_score(survey, cur_sliced)
        if accept(cur_score, new_score, cur_temp, seed=i):
            if new_score > total_score(survey, best_grouping):
                best_grouping = copy.deepcopy(cur_sliced)
            cur_score = new_score
        else:
            cur_sliced = copy_sliced
        cur_temp = self._initial_t * (1 - (i + 1 / (self._iteration - 1)))

    for group in best_grouping:
        temp_group = Group(group)
        sa.add_group(temp_group)

    return sa
