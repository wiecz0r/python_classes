class Infix_to_RPN:
    def __init__(self,characters,operators):
        self.characters = characters #list
        self.operators = operators #dict

    def validate(self,expr):
        ops = "".join(self.operators.keys())
        brackets_count = 0
        state = True
        for s in expr:
            if s == ' ': continue
            if s == '(':
                brackets_count+=1
            elif s == ')':
                brackets_count-=1
            if brackets_count < 0: return False
            if state:
                if s in self.characters:
                    state = False
                elif s in ops.replace('~',')'): return False
                elif s in '~': pass
            else:
                if s in ops.replace('~',''): state = True
                elif s in self.characters + '(~': return False
        if brackets_count !=0: return False
        return not state

    
    def convert(self,expression):
        if not self.validate(expression):
            return False
        output = []
        stack = []
        variables = []

        for char in expression:
            if char == ' ': continue
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
            
