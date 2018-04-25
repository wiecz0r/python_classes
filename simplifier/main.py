from validate_convert import Infix_to_RPN
from McCluskey import QmcC_Simplifier

import sys
import string

if __name__ == "__main__":
    operators = {'|': 1, '&': 2, '^': 3, '~': 4, '>': 1, '=': 0}
    characters = "".join(string.ascii_letters) + '01'

    converter = Infix_to_RPN(characters,operators)
    converted = converter.convert("a>b")
    if not converted:
        print("Not converted. Mistakes in expression")
        exit()
    rpn, var = converted

    simplifier = QmcC_Simplifier(operators,var,rpn)
    print(simplifier.simplify())
