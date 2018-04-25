import itertools
from colorama import Fore

class QmcC_Simplifier:
    def __init__(self, operators, variables, rpn):
        '''
            Constructor
        '''
        self.operators = operators
        self.variables = variables
        self.rpn = rpn
    
    def __binary_possibilities(self,var_no):
        '''
            Returns all possible binary values with specified length (@var_no)
        '''
        return list(itertools.product([0,1], repeat=var_no))
    
    def __count_expression(self,val_dict):
        '''
            Evaluates expression
        '''
        stack = []
        for char in self.rpn:
            if char in [0,1]:
                stack.append(char)
            elif char in val_dict.keys():
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
        '''
            Returns dict of all possible expressions which gives True at the end
        '''
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
    
    def __merge_two_elems(self,el1,el2):
        '''
            Merging two elems -> ex. [0,1,1], [1,1,1] to ['-',1,1]
        '''
        i = 0
        result = []
        for k in range(len(el1)):
            if el1[k] == el2[k]:
                result.append(el1[k])
            else:
                i += 1
                result.append('-')
        if i == 1: return result
        else: return False

    def __reduce(self,positive_val_dict):
        '''
            Main loop of Quine Mcluskey -> reducing values
        '''
        dict1 = positive_val_dict.copy()
        result_dict = dict1.copy()
        flag = True
        used_keys = set()
        
        while(flag):
            dict2 = {}
            keys=list(dict1.keys())
            flag=False
            for i in range(0,len(keys)):
                for j in range(i+1,len(keys)):
                    key1=keys[i]; key2=keys[j]
                    val1=dict1[key1]; val2=dict1[key2]
                    merged = self.__merge_two_elems(val1,val2)
                    if merged:
                        if merged in dict2.values():
                            used_keys.add(key1); used_keys.add(key2)
                            continue
                        flag = True
                        if key1.__class__ == tuple:
                            new_key = key1 + key2
                        else:
                            new_key = key1, key2
                        result_dict[new_key] = merged
                        dict2[new_key] = merged
                        used_keys.add(key1); used_keys.add(key2)
            for key in used_keys: 
                del result_dict[key]
            used_keys = set()
            dict1 = dict2
        return result_dict  

    def __final_expression(self,reduced_dict):
        '''
            Returns final reduced expression
        '''
        final_exr = ""
        for val in reduced_dict.values():
            for i in range(len(self.variables)):
                if val[i] == 0: final_exr += "~{} & ".format(self.variables[i])
                elif val[i] == 1: final_exr += "{} & ".format(self.variables[i])
            final_exr = final_exr[:-3]
            final_exr += " | "
        final_exr = final_exr[:-3]
        return final_exr
    
    def __always_true(self,dictionary):
        for v in dictionary.values():
            i=0
            for el in v:
                if el == '-':
                    i+=1
            if i == len(v):
                return True
        else: return False

    def simplify(self):
        '''
            Simplifying expression
        '''
        all_possibilites = self.__binary_possibilities(len(self.variables))
        positive = self.__all_positive_exp(all_possibilites)
        #print(positive)
        #if (len(positive.items()) == len(self.variables)**2): return True
        if (len(positive.items())==0):
            print("False")
            return False
        if (len(positive) == 1 and 'f' in positive) or len(positive) == 0:
            print("False")
            return False
        elif len(positive) == 1 and 't' in positive:
            print ("True")
            return True

        reduced_dict = self.__reduce(positive)
        #print(reduced_dict)
        if self.__always_true(reduced_dict):
            print("True")
            return True

        a = ''
        for k, v in reduced_dict.items():
            a += "F{} = {}  ".format(k,v)
        print(a)
        f_expr = self.__final_expression(reduced_dict)
        print ("\nFinal Expression:     " + Fore.RED + f_expr + Fore.RESET)
        return f_expr
