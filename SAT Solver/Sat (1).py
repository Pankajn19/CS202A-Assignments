from ast import Continue
from pysat.formula import CNF

 
# unit propogation removes all the clauses which containe only one literal and removes the negation of that literal from other clauses


def unit_propogation(f, variable_list):
    for l in f:
        if (len(l) == 1):
            f = [x for x in f if x != l]
            variable_list[abs(l[0]) - 1] = 1 if l[0] > 0 else -1
            f = [x for x in f if l[0] not in x]
            for k in f:
                if -l[0] in k:
                    k.remove(-l[0])
    return f, variable_list


# this function assigns values to pure literals(whose neagations are not present in the formula) and removes them from clauses
def pure_lit_e(f, var_no, variable_list):
    for i in range(1, var_no + 1):
        if any(i in c for c in f) and not any(-i in c for c in f):
            f = [x for x in f if i not in x]
            variable_list[i-1] = 1
        elif any(-i in c for c in f) and not any(i in c for c in f):
            f = [x for x in f if -i not in x]
            variable_list[i-1] = -1

    return f, variable_list

# this is just a function to randomly pick a variable from the formula after simplifications to assign it the value true or false
# it can be changed to optimize the code by picking a variable which occurs the most with same polarity through out the formula

def get_variable(f, variable_list):
    for i in range(0, len(variable_list)):
        if(variable_list[i] == 0):
            return i+1
    return 0

# this is the solver function
def solve(f, var_no, variable_list):
    f, variable_list = unit_propogation(f, variable_list)
    f,variable_list = pure_lit_e(f, var_no, variable_list)
    if len(f) == 0: 
        return f, variable_list

    for x in f:
        if len(x) == 0:
            return [x], variable_list
    
    if not any(len(x)-1 for x in f): return f, variable_list
    temp = [x for x in f]
    temp_variable_list = [x for x in variable_list]
    x = get_variable(f, variable_list)
    if(x == 0):
        return [], variable_list
    temp.append([x])
    temp_variable_list[x-1] = 1
    temp, temp_variable_list = solve(temp, var_no, temp_variable_list)
    if(len(temp) != 0): 
         return temp, temp_variable_list
    else:
        f.append([-x])
        variable_list[x-1] = -1
        f, variable_list = solve(f, var_no, variable_list)
        return f, variable_list



# variable_list is used to keep track of variables which are assigned a value
# variable_list[i] = 0 means (i+1)th variable is not assigned a value yet
# variable_list[i] = 1 means (i+1)th variable is assigned the value of "true"
# variable_list[i] = -1 means (i+1)th variable is assigned the value of "false"

cnf = CNF(from_file="test5.cnf")


f = [x for x in cnf.clauses]

variable_list = []
for i in range(1, cnf.nv+1):
     variable_list.append(0)
f, variable_list = solve(f, cnf.nv, variable_list)
if(f == [[]]):
    print("unsatisfiable")
else:
    print("satisfiable")
    print("a model is - ")
    for i, value in enumerate(variable_list):
        variable_list[i] = (i+1)*value
    variable_list = [x for x in variable_list if x != 0]
    print(variable_list)


# below is some garbage code which was used during the development to debug and test-run individual functions or code-snippets 

# cnf = CNF(from_file="test.cnf")
# print(cnf.clauses)
# variable_list = []
# for i in range(1, cnf.nv+1):
#     variable_list.append(0)
# temp, variable_list = unit_propogation(cnf.clauses, variable_list)
# print(temp)
# temp, variable_list = pure_lit_e(temp, cnf.nv, variable_list)
# print(temp)




