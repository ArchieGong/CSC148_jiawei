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

=== Module Description ===

This file contains a class that describes a survey as well as classes that
describe different types of questions that can be asked on a survey.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union
from criterion import InvalidAnswerError, HomogeneousCriterion

if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """An abstract class representing a question used in a survey

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize this question with the text <text>."""
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        raise NotImplementedError

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion:
    """A question whose answers can be one of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    options_: a list of strings representing the possible answer options
    for this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    options_: list[str]

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.

        Preconditions:
            - No two elements in <options> are the same string
            - <options> contains at least two elements
        """
        self.id = id_
        self.text = text
        self.options_ = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question:' + self.text + '' + 'options:' + str(self.options_)

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for this
        question.
        """
        return answer.content in self.options_

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        return 0.0


class NumericQuestion:
    """A question whose answer can be an integer between some minimum and
    maximum value (inclusive).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    min_: the minimum possible answer
    max_: the maximum possible answer

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    min_: int
    max_: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        Preconditions:
            - min_ < max_
        """
        self.id = id_
        self.text = text
        self.max_ = max_
        self.min_ = min_

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question:' + self.text + '' + 'min:' + str(self.min_) \
            + '' + 'max:' + str(self.max_)

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        return isinstance(answer.content, int) and \
            self.min_ <= answer.content <= self.max_

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity is calculated as follows:
        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximum
           and minimum possible answers.
        3. subtract the value of step 2 from 1.0

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        diff = abs(answer1.content - answer2.content)
        max_diff = self.max_ - self.min_
        similarity = 1.0 - (diff / max_diff)
        return max(0.0, similarity)


class YesNoQuestion:
    """A question whose answer is either yes (represented by True) or
    no (represented by False).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize a question with the text <text> and id <id>.
        """
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """Return a string representation of this question including
        the text of the question.

        You can choose the precise format of this string.
        """
        return 'Question:' + self.text

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for
        this question.
        """
        return answer.content in [True, False]

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal
        and 0.0 otherwise.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class CheckboxQuestion:
    """A question whose answers can be one or more of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    options_: a list of strings representing the possible answer options
    for this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    options_: list[str]

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize this question with the text <text> and id <id> and
        possible answers given in <options>.
        """
        self.id = id_
        self.text = text
        self.options_ = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return 'Question:' + self.text + '' + \
            'possible answers:' + str(self.options_)

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid iff:
            * It is a non-empty list.
            * It has no duplicate entries.
            * Every item in it is one of the answer options for this question.
        """
        if answer.content != [] and \
                len(set(answer.content)) == len(answer.content) and \
                set(answer.content).issubset(set(self.options_)):
            return True
        else:
            return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content. If there are zero unique strings in common,
        return 1.0.

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer2>.content == ['c', 'b', 'd'], there are 2 strings common to
        both: 'c' and 'b'; and there are 4 unique strings that appear in both:
        'a', 'b', 'c', and 'd'. Therefore, the similarity between these two
        answers is 2/4 = 0.5.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        unique1 = set(answer1.content)
        unique2 = set(answer2.content)
        common = unique1.intersection(unique2)
        total = unique1.union(unique2)
        if len(total) == 0:
            return 1.0
        else:
            return len(common) / len(total)


class Answer:
    """An answer to a question used in a survey

    === Public Attributes ===
    content: an answer to a single question
    """
    content: Union[str, bool, int, list[str]]

    def __init__(self,
                 content: Union[str, bool, int, list[str]]) -> None:
        """Initialize this answer with content <content>"""
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff this answer is a valid answer to <question>"""
        return question.validate_answer(self)


class Survey:
    """A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    === Private Attributes ===
    _questions: a dictionary mapping a question's id to the question itself
    _criteria: a dictionary mapping a question's id to its associated criterion
    _weights: a dictionary mapping a question's id to a weight -- an integer
              representing the importance of this criteria.

    === Representation Invariants ===
    No two questions on this survey have the same id
    Each key in _questions equals the id attribute of its value
    The dictionaries _questions, _criteria, and _weights all have the same keys
    Each value in _weights is greater than 0

    NOTE: The weights associated with the questions in a survey do NOT have to
          sum up to any particular amount.
    """
    _questions: dict[int, Question]
    _criteria: dict[int, Criterion]
    _weights: dict[int, int]

    def __init__(self, questions: list[Question]) -> None:
        """Initialize a new survey that contains every question in <questions>.

        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        self._questions = {q.id: q for q in questions}
        self._criteria = {q.id: HomogeneousCriterion() for q in questions}
        self._weights = {q.id: 1 for q in questions}

    def __len__(self) -> int:
        """Return the number of questions in this survey """
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """Return True iff there is a question in this survey with the same
        id as <question>.
        """
        return question.id in self._questions

    def __str__(self) -> str:
        """Return a string containing the string representation of all
        questions in this survey.

        You can choose the precise format of this string.
        """
        return '\n'.join(str(q) for q in self._questions.values())

    def get_questions(self) -> list[Question]:
        """Return a list of all questions in this survey """
        return list(self._questions.values())

    def _get_criterion(self, question: Question) -> Criterion:
        """Return the criterion associated with <question> in this survey.

        Preconditions:
            - <question>.id occurs in this survey
        """
        return self._criteria.get(question.id)

    def _get_weight(self, question: Question) -> int:
        """Return the weight associated with <question> in this survey.

        Preconditions:
            - <question>.id occurs in this survey
        """
        return self._weights.get(question.id)

    def set_weight(self, weight: int, question: Question) -> bool:
        """Set the weight associated with <question> to <weight> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if not self.__contains__(question):
            return False
        self._weights[question.id] = weight
        return True

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """Set the criterion associated with <question> to <criterion> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if not self.__contains__(question):
            return False
        self._criteria[question.id] = criterion
        return True

    def score_students(self, students: list[Student]) -> float:
        """Return a quality score for <students> calculated based on their
        answers to the questions in this survey, and the associated criterion
        and weight for each question.

        The score is determined using the following algorithm:
        1. For each question in this survey, find the question's associated
           criterion (do we want homogeneous answers, for instance), weight,
           and <students> answers to the question. Use the score_answers method
           for its criterion to calculate how well the <students> answers
           satisfy the criterion. Multiply this quality score by the question's
           weight.
        2. Find the average of all quality scores from step 1.

        This method should NOT throw an InvalidAnswerError. If one occurs
        during the execution of this method or if there are no questions in
        <self>, return zero.

        Preconditions:
            - All students in <students> have an answer to all questions in this
            survey
            - len(students) > 0
        """
        if len(self._questions) == 0:
            return 0.0
        try:
            scores = []
            weights = []
            for question in self._questions.values():
                criterion = self._get_criterion(question)
                w = self._get_weight(question)
                weights.append(w)
                answer = []
                for student in students:
                    answer.append(student.get_answer(question))
                weight_score = criterion.score_answers(question, answer)
                scores.append(weight_score * w)
            return sum(scores) / len(scores)
        except InvalidAnswerError:
            return 0.0

    def score_grouping(self, grouping: Grouping) -> float:
        """Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> return 0.0. Otherwise, the score
        is determined using the following algorithm:
        1. For each group in <grouping>, calculate the score for the members of
           this based on their answers to the questions in this survey.
        2. Return the average of all the scores calculated in step 1.

        Preconditions:
            - All students in the groups in <grouping> have an answer to
              all questions in this survey
        """
        if grouping.get_groups() is None:
            return 0.0
        scores = []
        for group in grouping.get_groups():
            scores.append(self.score_students(group.get_members()))
        return sum(scores) / len(scores)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper'],
                                'disable': ['E9992']})
