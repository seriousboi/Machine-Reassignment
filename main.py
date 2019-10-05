from structures import *
from parsers import *
from checker import *
from assesser import *
from benchmark import *
from misc import *



inst= load_instance("b_2")
sol= solution(inst.assignment,inst)
#inst.display_assignment()
#generate_assignment_file(inst.assignment,"test")
#inst.assignment.assignment_list[0]=1000
#inst.assignment.assignment_list= inst.assignment.assignment_list + [0]
#del(inst.assignment.assignment_list[0])
#for i in range(100):
#    inst.assignment.assignment_list[i]= 0
#inst.services[9].spread= 80
#inst.services[15].dependencies= inst.services[15].dependencies + [20000]
#print(assignment_checker(sol,True))
#services_bug()



print(total_cost_assesser(sol))
