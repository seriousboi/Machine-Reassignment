from structures import *
from parsers import *
from checker import *
from assesser import *
from benchmark import *
from misc import *



inst= load_instance("b_4")
#inst.display_processes()
#generate_assignment_file(inst.assignment,"test")
#inst.assignment[0]=1000
#inst.assignment= inst.assignment + [0]
#del(inst.assignment[0])
#for i in range(100):
#    inst.assignment[i]= 0
#inst.services[9].spread= 80
#inst.services[15].dependencies= inst.services[15].dependencies + [20000]
#print(assignment_checker(inst.assignment,inst,True))
#services_bug()



print(total_cost_assesser(inst.assignment,inst))
