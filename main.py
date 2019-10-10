from structures import *
from parsers import *
from checker import *
from assesser import *
from tests import *



#inst= load_instance("b_2")
#sol= solution(inst.assignment,inst)
#print(total_cost_assesser(sol))
#print(assignment_checker(sol,False))
#print(test_dependency_costraints_checker(inst,10))
test_all_checkers_inst(100)
