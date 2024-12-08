import course
import survey
import criterion
import grouper
import pytest
from course import Student, Course
from grouper import Grouping, Group, Grouper, AlphaGrouper, GreedyGrouper, SimulatedAnnealingGrouper
from survey import Question, MultipleChoiceQuestion, NumericQuestion, YesNoQuestion, CheckboxQuestion, Answer, Survey
from criterion import Criterion, HomogeneousCriterion, HeterogeneousCriterion, LonelyMemberCriterion
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
class TestStudent:
    def test_init(self) -> None:
        s = Student(101, "Joe")
        assert s.id == 101
        assert s.name == "Joe"
        assert s._answer == {}

    def test_str(self) -> None:
        s = Student(101, "Joe")
        assert s.str == "Joe"

    def test_Student_set_answer(self) -> None:
        s = Student(101, "Joe")
        q1 = Question(1, "what is 1+1?", ["1", "2", "3"], 1)
        a1 = Answer("2")
        s.set_answer(q1, a1)
        assert s._answer == {1: a1}
        a2 = Answer("1")
        s.set_answer(q1, a2)
        assert s._answer == {1: a2}

    def test_Student_has_answer(self) -> None:
        s = Student(101, "Joe")
        q1 = Question(1, "what is 1+1?", ["1", "2", "3"], 1)
        a1 = Answer("2")
        s.set_answer(q1, a1)
        assert s.has_answer == True
        a2 = Answer("1")
        s.set_answer(q1, a2)
        assert s.has_answer == False

    def test_Student_get_answer(self) -> None:
        s = Student(101, "Joe")
        q1 = Question(1, "what is 1+1?", ["1", "2", "3"], 1)
        a1 = Answer("2")
        s.set_answer(q1, a1)
        assert s.get_answer(q1) == a1
        q2 = Question(2, "", [], 2)
        assert s.get_answer(q2) is None


###############################################################################
# Task 3 Test cases
###############################################################################
class TestCourse:
    def test_Course_enroll_students(self) -> None:
        s1 = Student(1, "Joe")
        s2 = Student(2, "Bob")
        s3 = Student(3, "Ali")
        c = Course("CSC")
        c.enroll_student([s1, s2])
        assert s1 in c.students
        assert s2 in c.students
        c.enroll_student([s1, s3])
        assert s3 not in c.students
        c.enroll_student([s3])
        assert s3 in c.students

    def test_Course_get_students(self) -> None:
        s1 = Student(1, "Joe")
        s2 = Student(2, "Bob")
        s3 = Student(3, "Ali")
        c = Course("CSC")
        c.enroll_student([s1, s2, s3])
        students = c.get_students()
        assert len(students) == 3
        assert students[0] == s1
        assert students[1] == s2
        assert students[2] == s3


###############################################################################
# Task 4 Test cases
###############################################################################
class TestYesNoQuestion:
    def test_YesNoQuestion_get_similarity(self) -> None:
        q = YesNoQuestion(1, "what")
        a1 = Answer(True)
        a2 = Answer(False)
        assert q.get_similarity(a1, a1) == 1.0
        assert q.get_similarity(a1, a2) == 0.0

    def test_YesNoQuestion_validate_answer(self) -> None:
        q = YesNoQuestion(2, "how")
        assert q.validate_answer(Answer(True)) is True
        assert q.validate_answer(Answer(False)) is True
        assert q.validate_answer(Answer("yes")) is False


###############################################################################
# Task 5 Test cases
###############################################################################
class TestAnswer:
    def test_Answer_is_valid(self) -> None:
        q1 = Question("Your name", str)
        a1 = Answer("Joe")
        assert a1.is_valid(q1) is True
        q2 = Question("Your age", int)
        a2 = Answer("ten")
        assert a2.is_valid(q2) is False
        q3 = Question("Family members", list[str])
        a3 = Answer(["Dad", "Mom", "Sister"])
        assert a3.is_valid(q3) is True
        q4 = Question("Family members", list[str])
        a4 = Answer("Dad", "Mom", "Sister")
        assert a4.is_valid(q4) is False
        q5 = Question("You are boy", bool)
        a5 = Answer(True)
        assert a5.is_valid(q5) is True
        q6 = Question("You are boy", bool)
        a6 = Answer("yes")
        assert a6.is_valid(q6) is False


###############################################################################
# Task 6 Test cases
###############################################################################
class TestHomogeneousCriterion:
    def test_HomogeneousCriterion_score_answers(self, criteria,
                                                answers, question) -> None:
        q = Question("What is your favorite color?")
        criterion = HomogeneousCriterion()
        a1 = Answer("red")
        assert criterion.score_answers(question, [a1]) == 1.0
        a1 = Answer("red")
        a2 = Answer("red")
        assert criterion.score_answers(question, [a1, a2]) == 1.0
        a1 = Answer("red")
        a2 = Answer("blue")
        assert criterion.score_answers(question, [a1, a2]) == 0.0
        a1 = Answer("red")
        a2 = Answer("blue")
        a3 = Answer("black")
        assert criterion.score_answers(question, [a1, a2, a3]) == 0.33


###############################################################################
# Task 7 Test cases
###############################################################################
def test___len__():
    s1 = Student(123, 'A')
    s2 = Student(456, 'B')
    s3 = Student(789, 'C')
    g1 = Group([s1, s2, s3])
    assert len(g1) == 3

def test___contains__():
    s1 = Student(123, 'A')
    s2 = Student(456, 'B')
    s3 = Student(789, 'C')
    g1 = Group([s1, s2, s3])
    assert s1 in g1

def test_get_members():
    s1 = Student(123, 'A')
    s2 = Student(456, 'B')
    s3 = Student(789, 'C')
    g1 = Group([s1, s2, s3])
    assert len(g1.get_members()) == 3
###############################################################################
# Task 8 Test cases
###############################################################################
def test_add_group():
    s1 = Student(123, 'Alice')
    s2 = Student(456, 'bob')
    g1 = Group([s1, s2])
    g2 = Grouping()
    assert g2.add_group(g1) == True
    assert len(g2) == 1
###############################################################################
# Task 9 Test cases
###############################################################################
class TestSurvey:
    def test_Survey_get_questions(self) -> None:
        q1 = Question(1, "Your name")
        q2 = Question(2, "Your age")
        s = Survey([q1, q2])
        assert s.get_questions() == [q1, q2]
        q3 = Question(3, "Your gender")
        s.set_criterion(HomogeneousCriterion(), q3)
        s.set_weight(2, q3)
        assert s.get_questions() == [q1, q2, q3]

    def test_Survey_score_grouping(self, survey_, greedy_grouping) -> None:
        score = survey_.score_grouping(greedy_grouping)
        assert round(score, 2) == 2.29

    def test_Survey_score_students(self, survey_,
                                   students_with_answers) -> None:
        score = survey_.score_students(students_with_answers)
        assert round(score, 2) == 1.22

    def test_Survey_set_criterion(self) -> None:
        s = Survey()
        criterion = "E"
        assert s.set_criterion == criterion

    def test_Survey_set_weight(self, survey_, questions) -> None:
        survey_._weights = {}
        survey_.set_weight(999, questions[0])
        assert survey_._get_weight(questions[0]) == 999

###############################################################################
# Task 10 Test cases
###############################################################################
# TODO: Add your test cases below
