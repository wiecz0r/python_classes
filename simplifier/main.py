from convert import Infix_to_RPN
from McCluskey import QmcC_Simplifier

import sys

operators = {'|': 2, '&': 2, '^': 3, '~': 4, '>': 1, '=': 0}
characters = "".join([chr(i) for i in range(97, 123)]) + "".join([chr(i) for i \
    in range(65, 91)]) + "".join(list(map(str, range(2))))

converter = Infix_to_RPN(characters,operators)
converter.convert("x|y&1|x|z&y|c")