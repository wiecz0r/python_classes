#!/usr/bin/env python3

from validate_convert import Infix_to_RPN
from McCluskey import QmcC_Simplifier

import sys
import string

from colorama import Fore

def main(argv):
    '''
    Main program
    '''
    print("\nOriginal Expression:  "+Fore.YELLOW+"{}\n".format(argv) + Fore.RESET)
    operators = {'|': 1, '&': 2, '^': 3, '~': 4, '>': 1, '=': 0}
    characters = "".join(string.ascii_letters) + '01'

    converter = Infix_to_RPN(characters,operators)
    converted = converter.convert(argv)
    if not converted:
        print("Not converted. Mistakes in expression")
        exit()
    rpn, var = converted

    simplifier = QmcC_Simplifier(operators,var,rpn)
    aa = simplifier.simplify()
    return aa

if __name__ == "__main__":
    if len(sys.argv) < 2: print("Please write expression")
    else:    
        main(sys.argv[1])