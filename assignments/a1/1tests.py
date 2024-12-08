# TODO: Add the test cases that you'll be submitting to this file!
#       Make sure your test cases are all named starting with
#       test_ and that they have unique names.

# You may need to import pytest in order to run your tests.
# You are free to import hypothesis and use hypothesis for testing.
# This file will not be graded for style with PythonTA
from __future__ import annotations
import math
import random
import copy
from typing import TYPE_CHECKING, Any
import pytest
import course
import survey
import criterion
import grouper
if TYPE_CHECKING:
    from survey import Survey
    from course import Course, Student
    from grouper import Group, Grouping


@pytest.fixture
def empty_course() -> course.Course:
    return course.Course('csc148')


@pytest.fixture
def students() -> list[course.Student]:
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette')]


@pytest.fixture
def alpha_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def greedy_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def sa_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[2],
                                      students_with_answers[0]]))
    grouping.add_group(grouper.Group([students_with_answers[3],
                                      students_with_answers[1]]))
    return grouping


@pytest.fixture
def questions() -> list[survey.Question]:
    return [survey.MultipleChoiceQuestion(1, 'why?', ['a', 'b']),
            survey.NumericQuestion(2, 'what?', -2, 4),
            survey.YesNoQuestion(3, 'really?'),
            survey.CheckboxQuestion(4, 'how?', ['a', 'b', 'c'])]


@pytest.fixture
def criteria(answers) -> list[criterion.Criterion]:
    return [criterion.HomogeneousCriterion(),
            criterion.HeterogeneousCriterion(),
            criterion.LonelyMemberCriterion(),
            criterion.HomogeneousCriterion()]


@pytest.fixture()
def weights() -> list[int]:
    return [2, 5, 7, 4]


@pytest.fixture
def answers() -> list[list[survey.Answer]]:
    return [[survey.Answer('a'), survey.Answer('b'),
             survey.Answer('a'), survey.Answer('b')],
            [survey.Answer(0), survey.Answer(4),
             survey.Answer(-1), survey.Answer(1)],
            [survey.Answer(True), survey.Answer(False),
             survey.Answer(True), survey.Answer(True)],
            [survey.Answer(['a', 'b']), survey.Answer(['a', 'b']),
             survey.Answer(['a']), survey.Answer(['b'])]]


@pytest.fixture
def students_with_answers(students, questions, answers) -> list[course.Student]:
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def course_with_students(empty_course, students) -> course.Course:
    empty_course.enroll_students(students)
    return empty_course


@pytest.fixture
def course_with_students_with_answers(empty_course,
                                      students_with_answers) -> course.Course:
    empty_course.enroll_students(students_with_answers)
    return empty_course


@pytest.fixture
def survey_(questions, criteria, weights) -> survey.Survey:
    s = survey.Survey(questions)
    for i, question in enumerate(questions):
        s.set_weight(weights[i], question)
        s.set_criterion(criteria[i], question)
    return s


@pytest.fixture
def group(students) -> grouper.Group:
    return grouper.Group(students)


def get_member_ids(grouping: grouper.Grouping) -> set[frozenset[int]]:
    member_ids = set()
    for group in grouping.get_groups():
        ids = []
        for member in group.get_members():
            ids.append(member.id)
        member_ids.add(frozenset(ids))
    return member_ids


def compare_groupings(grouping1: grouper.Grouping,
                      grouping2: grouper.Grouping) -> None:
    assert get_member_ids(grouping1) == get_member_ids(grouping2)


###############################################################################
# Task 2 Test cases
###############################################################################
# TODO: Add your test cases below


###############################################################################
# Task 3 Test cases
###############################################################################
# TODO: Add your test cases below


###############################################################################
# Task 4 Test cases
###############################################################################
# TODO: Add your test cases below


###############################################################################
# Task 5 Test cases
###############################################################################
# TODO: Add your test cases below


###############################################################################
# Task 6 Test cases
###############################################################################
# TODO: Add your test cases below


###############################################################################
# Task 7 Test cases
###############################################################################
class TestGroup:
    def test___len__(self, group) -> None:
        assert len(group) == 4

    def test___contains__(self, group, students) -> None:
        assert course.Student(1, '') in group

    def test_get_members(self, group, students) -> None:
        ids = set()
        for member in group.get_members():
            ids.add(member.id)
            assert member in group
        assert ids == {1, 2, 3, 4}
        assert students is not group.get_members()
###############################################################################
# Task 8 Test cases
###############################################################################
class TestGrouping:
    def test_add_group(self, group) -> None:
        grouping = grouper.Grouping()
        grouping.add_group(group)
        assert group in grouping._groups
###############################################################################
# Task 9 Test cases
###############################################################################
# TODO: Add your test cases below


###############################################################################
# Task 10 Test cases
###############################################################################
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

