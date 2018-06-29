from .exceptions import FormulaValidationError


class BaseValidator:
    """
    Base validator, defining the interface of common behaviours
    """

    def __init__(self):
        pass

    def __call__(self, value):
        raise NotImplementedError("Should be implemented in children classes")


class NotEmptyStringValidator(BaseValidator):
    """
    This validator looks for non-empty formulas.
     + A valid formula is not empty!
    """

    def __call__(self, value):
        if not (isinstance(value, str) and value.strip()):
            raise FormulaValidationError('Formula cannot be empty')


class StartsWithValidator(BaseValidator):
    """
    This validator checks for initial character of a formula.
     + A valid formula starts with either an alphabetic character or an opening bracket
    """

    def __call__(self, value):
        first_chr = value[0]
        if not (first_chr.isalpha() or first_chr == '('):
            raise FormulaValidationError('Formula should start with an alphabetic sign or (')


class CharCombinationValidator(BaseValidator):
    """
    This validator checks for all combinations of characters to be valid.
     + A valid formula should only contain alphanumeric characters + ( and )
     + A valid formula should have matching number of opening and closing brakcets

     Validation takes o(n) time, loops over all chars and simultaneously checks bracketing and char validity
    """

    BRACKETS = {
        '(': ')',
        '{': '}',
        '[': ']'
    }

    class SimpleBracketStack:
        """
        To validate correct bracketing, we define a stack.
        + When ( is encountered, it's pushed to the stack.
        + When ) is encountered, if the last element of stack is a (, it's popped, otherwise it's pushed to stack.
        Finally, an empty stack signifies a correct bracketed formula
        """

        def __init__(self):
            self.stack = []

        def push(self, value):
            if not self.is_empty() and CharCombinationValidator.open_close_pair(self.stack[-1], value):
                return self.stack.pop()
            self.stack.append(value)

        def is_empty(self):
            return self.stack == []

        def __str__(self):
            return "Stack Contents: %r" % self.stack

    def __call__(self, value):
        stack = self.SimpleBracketStack()

        for char in value:
            if char in (list(self.BRACKETS.keys()) + list(self.BRACKETS.values())):
                stack.push(char)
            elif not char.isalnum():
                raise FormulaValidationError('Formula should only contain brackets or alphanumeric characters')

        if not stack.is_empty():
            raise FormulaValidationError('Formula should have a matching set of opening and closing brackets')

    @staticmethod
    def open_close_pair(value1, value2):
        return CharCombinationValidator.BRACKETS.get(value1) == value2

# Probably other validations, but my assumptions are up to this point (Since I don't know much Chemistry anyways :D)
