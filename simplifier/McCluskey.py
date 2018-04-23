import itertools

class QmcC_Simplifier:
    def __init__(self, operators, variables, rpn):
        self.operators = operators
        self.variables = variables
        self.rpn = rpn
    
    def __binary_possibilities(self,var_no):
        return list(itertools.product([0,1], repeat=var_no))
    
    def __count_expression(self,val_dict):
        stack = []
        exp = self.rpn.copy()
        for char in exp:
            if char in val_dict.keys():
                exp[exp.index(char)] = val_dict[char]
                stack.append(val_dict[char])
            
            elif char == '~':
                x = stack.pop()
                stack.append(not x)
            
            elif char in self.operators:
                x = stack.pop()
                y = stack.pop()
                if char == '|':
                    stack.append(x or y)
                elif char == '^':
                    stack.append(x ^ y)
                elif char == '>':
                    stack.append((not y) or x)
                elif char == '&':
                    stack.append(x and y)
                elif char == '=':
                    stack.append(x == y)
        
        return stack.pop()

    def __all_positive_exp(self, possibilities = []):
        positive = {}
        if len(possibilities) == 0:
            result = self.__count_expression({})
            if result:
                return {'t': None}
            else: return {'f': None}
        
        else:      
            for elem in possibilities:
                vals = list(elem)
                dictionary = dict(zip(self.variables,vals))
                if self.__count_expression(dictionary):
                    i = possibilities.index(elem)
                    positive[i] = vals
            return positive
    
    def __no_of_ones(self,values):
        i = 0
        for el in values:
            if el == 1:
                i += 1
        return i

    def __connect_two(self,element,position):
        final = element.copy()
        final[position-1] = '-'
        return final

    def __diff_one_pos(self,el1,el2):
        pass
    
    #Main loop of Quine Mcluskey -> reducing values
    def __reduce(self,positive_val_dict):
        dict1 = positive_val_dict.copy()
        flag = 1
        while flag:
            keys_used = []
            dict2 = {}
            keys = list(dict1.keys())

            for i in range (0, len(keys)-1):
                for j in range(i+1,len(keys)):
                    val1 = dict1[keys[i]]
                    val2 = dict2[keys[j]]
                    position = self.__diff_one_pos(val1,val2)
                    if abs(self.__no_of_ones(val1)-self.__no_of_ones(val2))==1 and position:
                        if keys[i].__class__ == tuple:
                            new_key = keys[i]+keys[j]
                        else: new_key = keys[i], keys[j]
                        keys_used.append(keys[i]); keys_used.append(keys[j])
                        del dict1[keys[i]]; del dict1[keys[j]]
                        dict2[new_key] = self.__connect_two(val1,position)
                    else: flag = 0
            for key in dict1.keys():
                if key not in keys_used:
                    dict2[key] = dict1[key]
            dict1 = dict2

        return dict1   

    def __last_table(self,reduced_dict,positive_vals):
        pass        

    def __simplify(self):
        all_possibilites = self.__binary_possibilities(len(self.variables))
        positive = self.__all_positive_exp(all_possibilites)

        if (len(positive) == 1 and 'f' in positive) or len(positive) == 0:
            return "False"
        elif len(positive) == 1 and 't' in positive:
            return "True"

        reduced_dict = self.__reduce(positive)
        return self.__last_table(reduced_dict,positive)


