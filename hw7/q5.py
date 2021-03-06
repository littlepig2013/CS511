# please use the same format as in the sample lists, and make sure the working directory has the readin file
# to run: python3 q5.py


import ast
from z3 import *
opt = Optimize() # find min

variable_d = {}
neg_var_d = {}


# input_list = [
#             [ [1,[[0,1]]], [1,[[0,2]]] ] ,
#             [ [1,[[0,1],[1,2]]], [2,[[0,2]]], [-3,[[0,1]]], [-1,[]] ] ,
#             [ [-1,[[0,1],[1,2]]], [-2,[[0,2]]], [3,[[0,1]]], [1,[]] ]
#         ]

# input_list = [
#             [ [1, [[0,1]]] ] ,
#             [ [1, [[0,1]]] ] ,
#             [ [-1,[[0,1]]] ]
#         ]

input_list = [
            [ [1, [[0,1]]] ] ,
            [ [1, [[0,1],[0,1]]], [-1,[[0,1]] ]]  ,
            [ [-1,[[0,1],[0,1]]], [1, [[0,1]] ]]  
        ]

try:
    filename = input("type the filename or use default input: ")
    with open("./"+filename, 'r') as f:
        input_list = ast.literal_eval(f.read())
except Exception as e:
    print(e)
    print("go with default")

print(input_list)
for i in range(len(input_list)):
    # init vars
    if i == 0:
        for term in input_list[i]:
            for var in term[1]:
                # prepare the x and its negation vars
                variable_d[var[1]] = Int("x"+str(var[1]))
                neg_var_d[var[1]] = Int("x_"+str(var[1]))
                opt.add(Or(variable_d[var[1]] == 0, variable_d[var[1]] == 1))
                opt.add(Or(neg_var_d[var[1]] == 0, neg_var_d[var[1]] == 1))
                opt.add(Not(neg_var_d[var[1]] == variable_d[var[1]]))
    # init minimization
    if i == 0:
        to_minimize = 0
        for term in input_list[i]:
            term_to_minimize = 1
            for var in term[1]:
                if var[0] == 0:
                    term_to_minimize = term_to_minimize * variable_d[var[1]]
                if var[0] == 1:
                    to_minimize = term_to_minimize * neg_var_d[var[1]]
            term_to_minimize = term[0] * term_to_minimize
            to_minimize = to_minimize + term_to_minimize
        opt.minimize(to_minimize)
    else:
        new_constraint = 0
        for term in input_list[i]:
            term_new_constraint = 1
            for var in term[1]:
                if var[0] == 0:
                    term_new_constraint = term_new_constraint * variable_d[var[1]]
                if var[0] == 1:
                    term_new_constraint = term_new_constraint * neg_var_d[var[1]]
            term_new_constraint = term[0] * term_new_constraint
            new_constraint = new_constraint + term_new_constraint
        opt.add(new_constraint <= 0)
            
print(opt.check())
print(opt.model())
print(opt.check()==sat)
