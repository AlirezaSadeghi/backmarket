class BlackMarketBaseException(Exception):
    pass


class FormulaValidationError(BlackMarketBaseException):

    def __init__(self, message, *args, **kwargs):
        self.message = 'Molecule Formula Exception - %s' % message
        super(FormulaValidationError, self).__init__(message, *args, **kwargs)
