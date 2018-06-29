import re

from collections import defaultdict

from molecule_parser.exceptions import FormulaValidationError
from molecule_parser.validators import (
    NotEmptyStringValidator, StartsWithValidator, CharCombinationValidator
)


class MoleculeParser:
    validators = (
        NotEmptyStringValidator(), StartsWithValidator(), CharCombinationValidator(),
    )

    OPEN_BRACKET_RE = r'[\(\[\{]'
    CLOSE_BRACKET_RE = r'[\)\]\}](\d+)?'
    ATOM_RE = r'([A-Z][a-z]?)(\d+)?'

    def __init__(self, formula):
        self.formula = formula
        self._stack = [defaultdict(int)]

    def is_valid(self, raise_exception=True):
        for validator in self.validators:
            try:
                validator(self.formula)
            except FormulaValidationError as fve:
                if raise_exception:
                    raise fve
                return False
        return True

    def process_formula(self):
        self._process_formula(self.formula)

    def _process_formula(self, formula):
        remainder = None

        atom = re.match(MoleculeParser.ATOM_RE, formula)
        opening = re.match(MoleculeParser.OPEN_BRACKET_RE, formula)
        closing = re.match(MoleculeParser.CLOSE_BRACKET_RE, formula)

        if atom:
            remainder = formula[len(atom.group()):]
            self._stack[-1][atom.group(1)] += int(atom.group(2) or 1)

        elif opening:
            remainder = formula[len(opening.group()):]
            self._stack.append(defaultdict(int))

        elif closing:
            remainder = formula[len(closing.group()):]
            for (k, v) in self._stack.pop().items():
                self._stack[-1][k] += v * int(closing.group(1) or 1)

        if remainder:
            self._process_formula(remainder)

    def __repr__(self):
        return '%r' % dict(self._stack[0])

    def __str__(self):
        return 'Parser Module for Formula: %s' % self.formula
