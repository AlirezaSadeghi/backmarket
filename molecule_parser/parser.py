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
        """
        Loops over all provided validators, and passes formula to them
        In case any of the validators fail, is_valid returns false.

        :param raise_exception: If True, invalid input formula will
        result in an exception indicating the reason otherwise
        only a Boolean is returned

        :return: True in case all validators pass the input formula,
         False otherwise. [Also can raise exception]
        """
        for validator in self.validators:
            try:
                validator(self.formula)
            except FormulaValidationError as fve:
                if raise_exception:
                    raise fve
                return False
        return True

    def process_formula(self):
        """
        Public interface to start processing the string
        """
        self._process_formula(self.formula)

    def _process_formula(self, formula):
        """
        Recursively looks through the provided formula and checks for existence of three conditions

        1. If an opening bracket is found (e.g. [):
         A new context (meaning a new formula that should be recursively processed) has been found.
         It's initially added as an empty dictionary to our stack,
          and will be popped when the corresponding closing bracket
          is encountered. We continue with the rest of the formula,
          looking for atoms and closing brackets.

        2. If a closing bracket is found (e.g. ]):
         The context is fully processed and now we remove it from the top of the stack,
         and apply its values to the parent context.

        3. If an atom is found (e.g. Fe):
         We add the atom to the current context,
          either with multiplier of 1 (if no number was next to it)
         or the number next to it.
        """
        remainder = None

        atom = re.match(MoleculeParser.ATOM_RE, formula)
        opening = re.match(MoleculeParser.OPEN_BRACKET_RE, formula)
        closing = re.match(MoleculeParser.CLOSE_BRACKET_RE, formula)

        # An atom is matched (e,g, Fe, or Fe2)
        if atom:
            remainder = formula[len(atom.group()):]
            self._stack[-1][atom.group(1)] += int(atom.group(2) or 1)

        # An opening is matched (e.g. [Fe...)
        elif opening:
            remainder = formula[len(opening.group()):]
            self._stack.append(defaultdict(int))

        # A closing is matched (e.g. ...]2)
        elif closing:
            remainder = formula[len(closing.group()):]
            for (k, v) in self._stack.pop().items():
                self._stack[-1][k] += v * int(closing.group(1) or 1)

        if remainder:
            self._process_formula(remainder)

    def __repr__(self):
        """
        :return: representation of class object
        """
        return '%r' % dict(self._stack[0])

    def __str__(self):
        """
        :return: identifier string of class object
        """
        return 'Parser Module for Formula: %s' % self.formula
