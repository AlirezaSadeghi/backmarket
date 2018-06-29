import sys
from os import path

import logging
from logging.config import dictConfig


def __fix_path__():
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


if __name__ == '__main__':
    __fix_path__()

    from molecule_parser.exceptions import FormulaValidationError
    from molecule_parser.parser import MoleculeParser
    from molecule_parser.config import logging_config

    dictConfig(logging_config)
    logger = logging.getLogger('parser')

    inputs = [
        'H2O',
        'Mg(OH)2',
        'CH3(CH2)6CH3',
        '(GFe)2{SO4(DC4)8}4',
        'K4[ON(SO3)2]2'
    ]

    for formula in inputs:
        parser = MoleculeParser(formula)
        try:
            parser.is_valid()
            parser.process_formula()
            logger.info('%s is valid -> %r' % (formula, repr(parser)))
        except FormulaValidationError as fve:
            logger.error("Invalid Formula! %r" % fve)
