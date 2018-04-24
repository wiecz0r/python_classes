class Infix_to_RPN:
    def __init__(self,characters,operators):
        self.characters = characters #list
        self.operators = operators #dict

    def convert(self,expression):
        output = []
        stack = []
        variables = []

        for char in expression:
            if char in self.characters:
                if char in ['0','1']:
                    output.append(int(char))
                else:
                    output.append(char)
                    if char not in variables:
                        variables.append(char)  
            
            elif char in self.operators.keys():
                while (len(stack)>0 and stack[len(stack)-1] != '(' and \
                    self.operators[stack[len(stack)-1]] >= self.operators[char]):
                    output.append(stack.pop())
                stack.append(char)
            
            elif char == '(':
                stack.append(char)
            
            elif char == ')':
                while stack[len(stack)-1] != '(':
                    output.append(stack.pop())
                stack.pop()
        
        while len(stack) > 0:
            output.append(stack.pop())
        
        return output, variables
            
class Validator:
    def __init__(self):
        pass          

            
