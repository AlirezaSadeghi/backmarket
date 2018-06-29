import re

import unittest
from unittest.mock import patch

from collections import defaultdict

from molecule_parser.exceptions import FormulaValidationError
from molecule_parser.parser import MoleculeParser


class TestMoleculeParser(unittest.TestCase):
    def setUp(self):
        self.formula = 'Mg(OH)2'
        self.complex_formula = '(GFe)2{SO4(DC4)8}4'
        self.invalid_formula = 'Mg(OH)2]'

    def test_instantiation(self):
        """
        Tests to check if instantiation sets formula and _stack correctly or not
        """
        parser = MoleculeParser(self.formula)

        self.assertEqual(self.formula, parser.formula)
        self.assertIsInstance(parser._stack, list)
        self.assertEqual(len(parser._stack), 1)
        self.assertIsInstance(parser._stack[0], defaultdict)

    def test_is_valid_ok(self):
        """
        Parser's is_valid method should pass in case a valid formula was supported
        __call__ functions of respective validators should also be called with the value of formula
        """
        for validator_obj in MoleculeParser.validators:
            with patch.object(validator_obj.__class__, '__call__') as mock_method:
                parser = MoleculeParser(self.formula)
                self.assertTrue(parser.is_valid())

                mock_method.assert_called_once_with(self.formula)

    def test_is_valid_invalid_formula(self):
        """
        Parser's is_valid method should fail in case an invalid formula was supported.
         1. Fail silently if raise_exception=False
         2. Fail verbosely otherwise
        """
        parser = MoleculeParser(self.invalid_formula)

        self.assertFalse(parser.is_valid(raise_exception=False))
        with self.assertRaises(FormulaValidationError):
            parser.is_valid()

    def test_parser_with_no_validators_should_always_pass(self):
        """
        If no validator classes were instantiated for the parser, all formulas should be accepted
        """
        MoleculeParser.validators = []
        self.assertTrue(MoleculeParser(self.invalid_formula).is_valid())

    def test_parser_should_have_correct_regexes(self):
        """
        Tests whether the opening, closing and atom matching regexes are correct.
        """
        for bracket_type in ['(', '{', '[']:
            self.assertTrue(re.match(MoleculeParser.OPEN_BRACKET_RE, bracket_type))
            self.assertIsNone(re.match(MoleculeParser.CLOSE_BRACKET_RE, bracket_type))
            self.assertIsNone(re.match(MoleculeParser.ATOM_RE, bracket_type))

        for bracket_type in [')', '}', ']']:
            self.assertTrue(re.match(MoleculeParser.CLOSE_BRACKET_RE, bracket_type))
            self.assertIsNone(re.match(MoleculeParser.OPEN_BRACKET_RE, bracket_type))
            self.assertIsNone(re.match(MoleculeParser.ATOM_RE, bracket_type))

        for atom in ['Fe2', 'O2', 'H']:
            self.assertTrue(re.match(MoleculeParser.ATOM_RE, atom))
            self.assertIsNone(re.match(MoleculeParser.OPEN_BRACKET_RE, atom))
            self.assertIsNone(re.match(MoleculeParser.CLOSE_BRACKET_RE, atom))

    def test_process_formula_private_call(self):
        """
        Test whether the private _process_formula method is called when the public
         process_formula is invoked, receiving the whole formula as parameter
        """
        with patch.object(MoleculeParser, '_process_formula') as mock_method:
            MoleculeParser(self.formula).process_formula()
            mock_method.assert_called_once_with(self.formula)

    def test_private_process_formula(self):
        """
        Tests whether recursive processing of the formulas are done right.

        Notice: This is more of an end-to-end test not a unit one, _process_formula works
        recursively and it's defined as a class method, having side-effects on a class attribute (e.g. _stack)
        So it's not easily unit-testable and it's considered bad practice, and should be fixed.
        [I had a limited time of nearly 7 hours to work on this so this remains for future versions]

        """
        parser = MoleculeParser(self.formula)
        parser.process_formula()
        self.assertDictEqual({
            'Mg': 1, 'H': 2, 'O': 2
        }, dict(parser._stack[0]))

        parser = MoleculeParser(self.complex_formula)
        parser.process_formula()

        self.assertDictEqual({
            'G': 2, 'Fe': 2, 'S': 4, 'O': 16, 'D': 32, 'C': 128
        }, dict(parser._stack[0]))


if __name__ == '__main__':
    unittest.main()
