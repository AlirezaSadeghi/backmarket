import re
import unittest

from string import punctuation

from molecule_parser.exceptions import FormulaValidationError
from molecule_parser.validators import (
    BaseValidator, NotEmptyStringValidator, StartsWithValidator, CharCombinationValidator
)


class TestBaseValidator(unittest.TestCase):
    def test_should_not_be_callable(self):
        """
        Base validator should not be allowed to be used
        """
        with self.assertRaises(NotImplementedError):
            BaseValidator()("any-value")


class TestNotEmptyStringValidator(unittest.TestCase):
    def setUp(self):
        self.empty_formula = ''
        self.not_empty_formula = 'non-empty'

    def test_accept_non_empty_formulas(self):
        """
        Tests whether non-empty formulas are accepted
        """
        validator = NotEmptyStringValidator()

        self.assertIsNone(validator(self.not_empty_formula))

    def test_should_raise_in_case_of_empty_formula(self):
        """
        Tests whether non-empty formulas are rejected
        """
        validator = NotEmptyStringValidator()

        with self.assertRaises(FormulaValidationError):
            validator(self.empty_formula)


class TestStartsWithValidator(unittest.TestCase):
    def setUp(self):
        self.correct_formulas = [
            '(therest', 'some-formula'
        ]
        self.wrong_formulas = [
            '3therest', ')done(', '_formula'
        ]

    def test_should_accept_alphabetic_opening_parenthesis(self):
        """
        Tests whether formulas starting with an alphabetic start, or with an opening parenthesis
        are accepted
        """
        validator = StartsWithValidator()

        for formula in self.correct_formulas:
            self.assertIsNone(validator(formula))

    def test_should_raise_in_case_of_wrong_initials(self):
        """
        Tests whether all other initial characters are rejected
        """
        validator = StartsWithValidator()

        for formula in self.wrong_formulas:
            with self.assertRaises(FormulaValidationError):
                validator(formula)


class TestCharCombinationValidator(unittest.TestCase):
    def setUp(self):
        self.correct_formulas = [
            'H2O',
            'Mg(OH)2',
            'CH3(CH2)6CH3',
            '(GFe)2{SO4(DC4)8}4',
            'K4[ON(SO3)2]2'
        ]
        self.wrong_opening_closing_parenthesis = ')()('
        self.wrong_opening_closing_types = '(something][FE}'

    def test_should_accept_alphanumeric_formulas(self):
        """
        Tests whether formulas only containing alphanumeric, (, ) characters are accepted
        """
        validator = CharCombinationValidator()

        for formula in self.correct_formulas:
            self.assertIsNone(validator(formula))

    def test_should_raise_in_case_of_wrong_characters(self):
        """
        Tests whether formulas containing _, -, +, -, =, and other invalid character types are rejected
        Checks all punctuation characters, except those accepted.
        """
        validator = CharCombinationValidator()

        regex = re.compile(r'[\(\[\{]\)\]\}')
        forbidden_chars = regex.sub('', punctuation)
        for char in forbidden_chars:
            with self.assertRaises(FormulaValidationError):
                validator('Fe(O)2%s' % char)

    def test_should_raise_in_case_of_wrong_parenthesising(self):
        """
        Tests whether opening and closing parenthesis in a formula match, not just by count,
        but also by position.

        TODO -> Mock SimpleStack and check that also
        """
        validator = CharCombinationValidator()

        with self.assertRaises(FormulaValidationError):
            validator(self.wrong_opening_closing_parenthesis)

    def test_should_raise_in_case_of_wrong_opening_closing_types(self):
        """
        Tests whether opening and closing parenthesis match in type
        """
        validator = CharCombinationValidator()

        with self.assertRaises(FormulaValidationError):
            validator(self.wrong_opening_closing_types)


if __name__ == '__main__':
    unittest.main()
