import itertools

class QmcC_Simplifier:
    def __init__(self, operators, variables, rpn):
        self.operators = operators
        self.variables = variables
        self.rpn = rpn
    
    def __binary_possibilities(self,var_no):
        return list(itertools.product([0,1], repeat=var_no))
    
    def count_expression(self,val_dict):
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
                    stack.append((not x) or y)
                elif char == '&':
                    stack.append(x and y)
                elif char == '=':
                    stack.append(x == y)
        
        return stack.pop()

    def __all_positive_exp(self, possibilities = []):
        positive = {}
        if len(possibilities) == 0:
            result = self.count_expression({})
            if result:
                return {'t': None}
            else: return {'f': None}
        
        else:      
            for elem in possibilities:
                vals = list(elem)
                dictionary = dict(zip(self.variables,vals))
                if self.count_expression(dictionary):
                    i = possibilities.index(elem)
                    positive[i] = vals
            return positive
    
    def __merge_two_elems(self,el1,el2):
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

    
    #Main loop of Quine Mcluskey -> reducing values
    def __reduce(self,positive_val_dict):
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
                    #if key1 in used_keys and key2 in used_keys: continue
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

    def __last_table(self,reduced_dict,positive_vals):
        pass        

    def simplify(self):
        all_possibilites = self.__binary_possibilities(len(self.variables))
        positive = self.__all_positive_exp(all_possibilites)

        if (len(positive.items()) == len(self.variables)**2): return True
        if (len(positive.items())==0): return False
        if (len(positive) == 1 and 'f' in positive) or len(positive) == 0:
            return False
        elif len(positive) == 1 and 't' in positive:
            return True

        return self.__reduce(positive)
        #return self.__last_table(reduced_dict,positive)


