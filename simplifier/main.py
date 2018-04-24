from validate_convert import Infix_to_RPN
from McCluskey import QmcC_Simplifier

import sys

operators = {'|': 1, '&': 2, '^': 3, '~': 4, '>': 1, '=': 0}
characters = "".join([chr(i) for i in range(97, 123)]) + "".join([chr(i) for i \
    in range(65, 91)]) + "".join(list(map(str, range(2))))

converter = Infix_to_RPN(characters,operators)
rpn, var = converter.convert("(x|y&1)&1=1")
print(rpn)
simplifier = QmcC_Simplifier(operators,var,rpn)
dictionary = dict(zip(var,[0,0]))
aaa = simplifier.count_expression(dictionary)
print(aaa)
