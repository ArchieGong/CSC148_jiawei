class TestAlphaGrouper:
    def test_make_grouping(self, course_with_students_with_answers,
                           alpha_grouping,
                           survey_) -> None:
        grouper_ = grouper.AlphaGrouper(2)
        grouping = grouper_.make_grouping(course_with_students_with_answers,
                                          survey_)
        compare_groupings(grouping, alpha_grouping)


class TestGreedyGrouper:
    def test_make_grouping(self, course_with_students_with_answers,
                           greedy_grouping,
                           survey_) -> None:
        grouper_ = grouper.GreedyGrouper(2)
        grouping = grouper_.make_grouping(course_with_students_with_answers,
                                          survey_)
        compare_groupings(grouping, greedy_grouping)


class TestGroup:
    def test___len__(self, group) -> None:
        assert len(group) == 4

    def test___contains__(self, group, students) -> None:
        for student in students:
            assert student in group

    def test_get_members(self, group) -> None:
        ids = set()
        for member in group.get_members():
            ids.add(member.id)
        assert ids == {1, 2, 3, 4}


class TestGrouping:
    def test___len__(self, greedy_grouping) -> None:
        assert len(greedy_grouping) == 2

    def test_add_group(self, group) -> None:
        grouping = grouper.Grouping()
        grouping.add_group(group)
        assert group in grouping._groups

    def test_get_groups(self, students) -> None:
        group = grouper.Group(students[:2])
        grouping = grouper.Grouping()
        grouping.add_group(group)
        assert get_member_ids(grouping) == {frozenset([1, 2])}



