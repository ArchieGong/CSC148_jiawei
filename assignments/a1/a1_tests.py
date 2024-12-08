"""CSC148 Assignment 1

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh, Jaisie Sin, Tom Ginsberg, Jonathan Calver, and Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Misha Schwartz, Mario Badr, Diane Horton, Sophia Huynh,
Jonathan Calver, and Jacqueline Smith
"""
import course
import survey
import criterion
import grouper
import pytest
from random import choice
from string import ascii_lowercase

GROUP_SIZE = 8
TOTAL_STUDENTS = 53


################################################################################
# PYTEST FIXTURES
# These are here create some sample datasets that we can use in our test cases.
# For more details, see https://docs.pytest.org/en/6.2.x/fixture.html
################################################################################
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
def questions_2() -> list[survey.Question]:
    return [survey.MultipleChoiceQuestion(5, 'why?', ['a', 'b']),
            survey.NumericQuestion(6, 'what?', -2, 4),
            survey.YesNoQuestion(7, 'really?'),
            survey.CheckboxQuestion(8, 'how?', ['a', 'b', 'c'])]


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
def wrong_answers() -> list[list[survey.Answer]]:
    return [[survey.Answer('m'), survey.Answer('q'),
             survey.Answer(4), survey.Answer(['a, b'])],
            [survey.Answer(-100), survey.Answer(9999),
             survey.Answer(['a, b']), survey.Answer(9999)],
            [survey.Answer(['a, b']), survey.Answer('False'),
             survey.Answer(-7), survey.Answer(123)],
            [survey.Answer(True), survey.Answer('a'),
             survey.Answer(['LOL']), survey.Answer(-4)]]


@pytest.fixture
def students_with_answers(students, questions, answers) -> list[course.Student]:
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def students_with_wrong_answers(students, questions, wrong_answers) -> list[course.Student]:
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, wrong_answers[j][i])
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
def course_with_students_with_wrong_answers(empty_course,
                                            students_with_wrong_answers) -> course.Course:
    empty_course.enroll_students(students_with_wrong_answers)
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


################################################################################
# PROVIDED TEST CASES
################################################################################
class TestCourse:
    def test_enroll_students(self, empty_course, students) -> None:
        empty_course.enroll_students(students)
        for student in students:
            assert student in empty_course.students

        temp = len(empty_course.students)
        empty_course.enroll_students([course.Student(99, ''),
                                      course.Student(5, 'Molly')])
        assert len(empty_course.students) == temp
        empty_course.enroll_students(students)
        assert len(empty_course.students) == temp
        empty_course.enroll_students([course.Student(5, 'Molly')])
        assert len(empty_course.students) == temp + 1

    def test_all_answered(self, course_with_students_with_answers,
                          survey_) -> None:
        assert course_with_students_with_answers.all_answered(survey_)

    def test_all_answered_2(self, course_with_students_with_wrong_answers,
                            survey_) -> None:
        assert not course_with_students_with_wrong_answers.all_answered(survey_)

    def test_get_students(self, course_with_students) -> None:
        students = course_with_students.get_students()
        for student in students:
            assert student in course_with_students.students


class TestStudent:
    def test_has_answer(self, students_with_answers,
                        questions, questions_2) -> None:
        for student in students_with_answers:
            for question in questions:
                assert student.has_answer(question)

        for student in students_with_answers:
            for question in questions_2:
                assert not student.has_answer(question)

    def test_has_answer_2(self, students, questions) -> None:
        for student in students:
            for question in questions:
                assert not student.has_answer(question)

    def test_has_answer_3(self, students_with_wrong_answers, questions) -> None:
        for student in students_with_wrong_answers:
            for question in questions:
                assert not student.has_answer(question)

    def test_set_answer(self, students, questions, answers) -> None:
        for i, student in enumerate(students):
            for j, question in enumerate(questions):
                answer = answers[j][i]
                student.set_answer(question, answer)
                assert student.get_answer(question) == answer

    def test_get_answer(self, students_with_answers,
                        questions, answers) -> None:
        for i, student in enumerate(students_with_answers):
            for j, question in enumerate(questions):
                assert student.get_answer(question) == answers[j][i]


class TestCriterion:



    def test_inheritance(self):
        classes = [criterion.HomogeneousCriterion,
                   criterion.HeterogeneousCriterion,
                   criterion.LonelyMemberCriterion]

        temp = 0
        for cls in classes:
            assert len(cls.mro()) > 2, "Wrong inheritance structure"
            if len(cls.mro()) > 3:
                temp += 1

        assert temp >= 1, "Wrong inheritance structure"


class TestHomogeneousCriterion:
    def test_score_answers(self, criteria, answers, questions) -> None:
        hom_criterion = criteria[0]
        score = hom_criterion.score_answers(questions[0], answers[0])
        assert round(score, 2) == 0.33


class TestHeterogeneousCriterion:
    def test_score_answers(self, criteria, answers, questions) -> None:
        het_criterion = criteria[1]
        score = het_criterion.score_answers(questions[1], answers[1])
        assert round(score, 2) == 0.44
        score = het_criterion.score_answers(questions[0], answers[0])
        assert round(score, 2) == 0.67
        score = het_criterion.score_answers(questions[2], answers[2])
        assert round(score, 2) == 0.5
        score = het_criterion.score_answers(questions[3], answers[3])
        assert round(score, 2) == 0.5

    def test_score_wrong_answers(self, criteria, wrong_answers, questions) -> None:
        het_criterion = criteria[1]
        with pytest.raises(criterion.InvalidAnswerError):
            het_criterion.score_answers(questions[1], wrong_answers[1])


class TestLonelyMemberCriterion:
    def test_score_answers(self, criteria, answers, questions) -> None:
        lon_criterion = criteria[2]
        assert lon_criterion.score_answers(questions[2], answers[2]) == 0.0
        assert lon_criterion.score_answers(questions[1], answers[1]) == 0.0
        assert lon_criterion.score_answers(questions[3], answers[3]) == 0.0
        assert lon_criterion.score_answers(questions[0], answers[0]) == 1.0

    def test_score_wrong_answers(self, criteria,
                                 wrong_answers, questions) -> None:
        lon_criterion = criteria[2]
        with pytest.raises(criterion.InvalidAnswerError):
            lon_criterion.score_answers(questions[1], wrong_answers[1])


class TestAlphaGrouper:
    def test_make_grouping(self, course_with_students_with_answers,
                           alpha_grouping,
                           survey_) -> None:
        grouper_ = grouper.AlphaGrouper(2)
        grouping = grouper_.make_grouping(course_with_students_with_answers,
                                          survey_)
        compare_groupings(grouping, alpha_grouping)

    def test_grouping(self, empty_course):
        grouper_ = grouper.AlphaGrouper(GROUP_SIZE)
        letters = ascii_lowercase
        names = [''.join(choice(letters) for i in range(4))
                 for _ in range(TOTAL_STUDENTS)]
        sorted_names = sorted(names)
        students = [course.Student(i, names[i])
                    for i, name in enumerate(names)]
        empty_course.enroll_students(students)
        survey_2 = survey.Survey([])

        groups = grouper_.make_grouping(empty_course,
                                        survey_2).get_groups()

        actual_names = []
        for i, group in enumerate(groups):
            if i != (len(groups) - 1):
                assert len(group) == GROUP_SIZE
            else:
                assert len(group) == TOTAL_STUDENTS % GROUP_SIZE

            actual_names.extend([s.name for s in group.get_members()])

        assert sorted_names == actual_names


class TestGreedyGrouper:
    def test_make_grouping(self, course_with_students_with_answers,
                           greedy_grouping,
                           survey_) -> None:
        grouper_ = grouper.GreedyGrouper(2)
        grouping = grouper_.make_grouping(course_with_students_with_answers,
                                          survey_)
        compare_groupings(grouping, greedy_grouping)

    def test_grouping_size(self, empty_course, questions, answers):
        grouper_ = grouper.GreedyGrouper(GROUP_SIZE)
        letters = ascii_lowercase
        names = [''.join(choice(letters) for i in range(4))
                 for _ in range(TOTAL_STUDENTS)]
        students = [course.Student(i, names[i])
                    for i, name in enumerate(names)]
        empty_course.enroll_students(students)
        s = survey.Survey(questions)
        for i, student in enumerate(students):
            for j, question in enumerate(questions):
                student.set_answer(question, answers[j][0])
        groups = grouper_.make_grouping(empty_course, s).get_groups()

        for i, group in enumerate(groups):
            if i != (len(groups) - 1):
                assert len(group) == GROUP_SIZE
            else:
                assert len(group) == TOTAL_STUDENTS % GROUP_SIZE

    def test_grouping(self, empty_course, questions, answers, criteria):
        grouper_ = grouper.GreedyGrouper(3)
        letters = ascii_lowercase
        names = [''.join(choice(letters) for i in range(4)) for _ in range(12)]
        students = [course.Student(i, names[i])
                    for i, name in enumerate(names)]

        questions = [survey.NumericQuestion(1, "Q1", 0, 100),
                    survey.YesNoQuestion(2, "Q2")]
        s = survey.Survey(questions)
        s.set_criterion(criteria[1], questions[1])
        empty_course.enroll_students(students)
        answers = [[survey.Answer(70), survey.Answer(True)],
                   [survey.Answer(101), survey.Answer(False)],
                   [survey.Answer(24), survey.Answer(True)],
                   [survey.Answer(53), survey.Answer(False)],
                   [survey.Answer(70), survey.Answer(True)],
                   [survey.Answer(44), survey.Answer(False)],
                   [survey.Answer(44), survey.Answer(True)],
                   [survey.Answer(20), survey.Answer(False)],
                   [survey.Answer(4), survey.Answer(True)],
                   [survey.Answer(98), survey.Answer(False)],
                   [survey.Answer(81), survey.Answer(True)],
                   [survey.Answer(105), survey.Answer(False)]]

        for i, student in enumerate(students):
            for j, question in enumerate(questions):
                student.set_answer(question, answers[i][j])
        grouping_ = grouper_.make_grouping(empty_course, s)

        res_grouping = grouper.Grouping()
        res_grouping.add_group(grouper.Group([students[0], students[3],
                                              students[4]]))
        res_grouping.add_group(grouper.Group([students[1], students[2],
                                              students[5]]))
        res_grouping.add_group(grouper.Group([students[6], students[7],
                                              students[8]]))
        res_grouping.add_group(grouper.Group([students[9], students[10],
                                              students[11]]))

        compare_groupings(grouping_, res_grouping)


class TestSimulatedAnnealingGrouper:
    def test_make_grouping(self, course_with_students_with_answers,
                           sa_grouping,
                           survey_) -> None:
        grouper_ = grouper.SimulatedAnnealingGrouper(2)
        grouping = grouper_.make_grouping(course_with_students_with_answers,
                                          survey_)
        compare_groupings(grouping, sa_grouping)

    def test_grouping(self, empty_course, questions, answers, criteria):
        grouper_ = grouper.SimulatedAnnealingGrouper(3)
        letters = ascii_lowercase
        names = [''.join(choice(letters) for i in range(4)) for _ in range(12)]
        students = [course.Student(i, names[i])
                    for i, name in enumerate(names)]

        questions = [survey.NumericQuestion(1, "Q1", 0, 100),
                    survey.YesNoQuestion(2, "Q2")]
        s = survey.Survey(questions)
        s.set_criterion(criteria[1], questions[1])
        empty_course.enroll_students(students)
        answers = [[survey.Answer(70), survey.Answer(True)],
                   [survey.Answer(101), survey.Answer(False)],
                   [survey.Answer(24), survey.Answer(True)],
                   [survey.Answer(53), survey.Answer(False)],
                   [survey.Answer(70), survey.Answer(True)],
                   [survey.Answer(44), survey.Answer(False)],
                   [survey.Answer(44), survey.Answer(True)],
                   [survey.Answer(20), survey.Answer(False)],
                   [survey.Answer(4), survey.Answer(True)],
                   [survey.Answer(98), survey.Answer(False)],
                   [survey.Answer(81), survey.Answer(True)],
                   [survey.Answer(105), survey.Answer(False)]]

        for i, student in enumerate(students):
            for j, question in enumerate(questions):
                student.set_answer(question, answers[i][j])
        grouping_ = grouper_.make_grouping(empty_course, s)

        res_grouping = grouper.Grouping()
        res_grouping.add_group(grouper.Group([students[0], students[9],
                                              students[4]]))
        res_grouping.add_group(grouper.Group([students[3], students[5],
                                              students[6]]))
        res_grouping.add_group(grouper.Group([students[8], students[2],
                                              students[7]]))
        res_grouping.add_group(grouper.Group([students[1], students[10],
                                              students[11]]))

        compare_groupings(grouping_, res_grouping)


class TestGroup:
    def test___len__(self, group) -> None:
        assert len(group) == 4

    def test___contains__(self, group, students) -> None:
        for student in students:
            assert student in group
        assert course.Student(3, 'Miguel') in group
        assert course.Student(7, 'Zoro') not in group

    def test_get_members(self, group, students) -> None:
        ids = set()
        for member in group.get_members():
            ids.add(member.id)
            assert member in group
        assert ids == {1, 2, 3, 4}
        assert students is not group.get_members()


class TestGrouping:
    def test___len__(self, greedy_grouping) -> None:
        assert len(greedy_grouping) == 2

    # Requested in handout.
    def test_add_group(self, group) -> None:
        grouping = grouper.Grouping()
        grouping.add_group(group)
        assert group in grouping._groups

    def test_get_groups(self, students) -> None:
        group = grouper.Group(students[:2])
        grouping = grouper.Grouping()
        grouping.add_group(group)
        assert get_member_ids(grouping) == {frozenset([1, 2])}


# Requested in handout
class TestSurvey:
    def test___len__(self, survey_) -> None:
        assert len(survey_) == 4

    def test___contains__(self, survey_, questions, questions_2) -> None:
        for question in questions:
            assert question in survey_
        for question in questions_2:
            assert question not in survey_

    def test_get_questions(self, survey_, questions) -> None:
        q_ids = set()
        for question in questions:
            q_ids.add(question.id)
        for question in survey_.get_questions():
            assert question.id in q_ids

    def test__get_criterion(self, survey_, questions, criteria) -> None:
        for i, question in enumerate(questions):
            assert isinstance(survey_._get_criterion(question),
                              type(criteria[i]))

    def test__get_weight(self, survey_, questions, weights) -> None:
        for i, question in enumerate(questions):
            assert isinstance(survey_._get_weight(question), type(weights[i]))

    def test_set_weight(self, survey_, questions) -> None:
        survey_._weights = {}
        survey_.set_weight(999, questions[0])
        assert survey_._get_weight(questions[0]) == 999

    def test_set_criterion(self, survey_, questions) -> None:
        survey_._criteria = {}
        criterion_ = criterion.HomogeneousCriterion()
        survey_.set_criterion(criterion_, questions[0])
        assert survey_._get_criterion(questions[0]) == criterion_

    def test_score_students(self, survey_, students_with_answers) -> None:
        score = survey_.score_students(students_with_answers)
        assert round(score, 2) == 1.22

    def test_score_grouping(self, survey_, greedy_grouping) -> None:
        score = survey_.score_grouping(greedy_grouping)
        assert round(score, 2) == 2.29


class TestAnswer:
    def test_is_valid(self, questions, answers) -> None:
        for i, question in enumerate(questions):
            assert answers[i][0].is_valid(question)

    def test_init_copy(self) -> None:
        l = ['a', 'b']
        answer = survey.Answer(l)
        l.append('c')
        assert answer.content == ['a', 'b']


class TestQuestions:

    def test_inheritance(self):
        classes = [survey.MultipleChoiceQuestion,
                   survey.NumericQuestion,
                   survey.YesNoQuestion,
                   survey.CheckboxQuestion]
        temp = 0
        for cls in classes:
            assert len(cls.mro()) > 2, "Wrong inheritance structure"
            if len(cls.mro()) > 3:
                temp += 1

        assert temp >= 1, "Wrong inheritance structure"


class TestMultipleChoiceQuestion:
    def test_validate_answer(self, questions, answers) -> None:
        mc = questions[0]
        assert mc.validate_answer(answers[0][0])
        assert not mc.validate_answer(answers[1][0])
        assert not mc.validate_answer(answers[2][0])
        assert not mc.validate_answer(answers[3][0])

    def test_get_similarity(self, questions, answers) -> None:
        mc = questions[0]
        assert mc.get_similarity(*answers[0][:2]) == 0.0
        assert mc.get_similarity(answers[0][0], answers[0][0]) == 1.0


class TestNumericQuestion:
    def test_validate_answer(self, questions, answers) -> None:
        num = questions[1]
        assert num.validate_answer(answers[1][0])
        assert not num.validate_answer(answers[0][0])
        assert not num.validate_answer(answers[3][0])

    def test_get_similarity(self, questions, answers) -> None:
        num = questions[1]
        similarity = num.get_similarity(*answers[1][:2])
        assert round(similarity, 2) == 0.33
        similarity = num.get_similarity(*answers[1][2:])
        assert round(similarity, 2) == 0.67
        similarity = num.get_similarity(survey.Answer(-2), survey.Answer(4))
        assert round(similarity, 2) == 0.0
        similarity = num.get_similarity(survey.Answer(0), survey.Answer(0))
        assert round(similarity, 2) == 1.0


class TestYesNoQuestion:
    def test_validate_answer(self, questions, answers) -> None:
        yn = questions[2]
        assert yn.validate_answer(answers[2][0])

    def test_get_similarity(self, questions, answers) -> None:
        yn = questions[2]
        similarity = yn.get_similarity(*answers[2][:2])
        assert round(similarity, 2) == 0.0


class TestCheckboxQuestion:
    def test_validate_answer(self, questions, answers) -> None:
        check = questions[3]
        assert check.validate_answer(answers[3][0])
        assert not check.validate_answer(answers[1][0])
        assert not check.validate_answer(answers[2][0])
        assert not check.validate_answer(answers[0][0])

    def test_get_similarity(self, questions, answers) -> None:
        check = questions[3]
        similarity = check.get_similarity(*answers[3][2:])
        assert round(similarity, 2) == 0.0
        similarity = check.get_similarity(*answers[3][:2])
        assert round(similarity, 2) == 1.0
        similarity = check.get_similarity(*answers[3][1:3])
        assert round(similarity, 2) == 0.5
        similarity = check.get_similarity(survey.Answer(['a', 'b', 'c', 'f']),
                                          survey.Answer(['a', 'c', 'b', 'd']))
        assert round(similarity, 2) == 0.6


if __name__ == '__main__':
    pytest.main(['a1_tests.py'])
