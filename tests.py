from structures import *
from parsers import *
from checker import *
from assesser import *
from random import *
from time import *
from copy import *


#inst= load_instance("b_2")
#sol= solution(inst.assignment,inst)
#inst.display_assignment()
#generate_assignment_file(inst.assignment,"test")
#inst.assignment.assignment_list[0]=1000
#inst.assignment.assignment_list= inst.assignment.assignment_list + [0]
#del(inst.assignment.assignment_list[0])
#for i in range(100):
#    inst.assignment.assignment_list[i]= 0
#ma= sol.assignment.get_machine_assignment(len(sol.instance.machines))
#sol.instance.processes[ma[2][0]].service= 12
#sol.instance.processes[ma[2][1]].service= 12
#inst.services[9].spread= 80
#inst.services[15].dependencies= inst.services[15].dependencies + [20000]
#print(assignment_checker(sol,True))
#services_bug()




def test_consistency_checker(inst,times):
    print("testing consistency checker")
    print()
    for time in range(times):
        inst_1= deepcopy(inst)
        inst_2= deepcopy(inst)
        sol_1= solution(inst_1.assignment,inst_1)
        sol_2= solution(inst_2.assignment,inst_2)
        machines_amount= len(inst.machines)
        processes_amount= len(inst.processes)

        rand_ass= randrange(machines_amount,machines_amount*2)
        rand_index= randrange(processes_amount)
        inst_1.assignment.assignment_list[rand_index]= rand_ass
        print("proc",rand_index,"mech",rand_ass)
        if consistency_checker(sol_1) == True:
            print("consistency check: no error showing up")
            return False

        rand_del= randrange(processes_amount)
        del(inst_2.assignment.assignment_list[rand_del])
        print("proc",rand_del)
        if consistency_checker(sol_2) == True:
            print("consistency check: no error showing up")
            return False
        print()

    return True



def test_capacity_constraints(inst,times):
    print("testing capacity constraints")
    print()
    for time in range(times):
        inst_1= deepcopy(inst)






def test_instance(instance_name):
    print("instance "+instance_name)
    start= time.time()
    inst= load_instance(instance_name)
    load_time= time.time() - start
    sol= solution(inst.assignment,inst)
    print("load time:",round(load_time,2))
    assignment_checker(sol,True)
    check_time= time.time() - (start + load_time)
    print("check time:",round(check_time,2))
    print()
    return load_time,check_time



def test_a():
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        test_instance(instance_name)



def test_b():
    for i in range(10):
        instance_name= "b_"+str(i+1)
        test_instance(instance_name)



def test_all():
    test_a()
    test_b()



def services_bug():
    for i in range(10):
        print("b"+str(i+1))
        inst= load_instance("b_"+str(i+1))
        true_serv=0
        empty_serv=0
        services_amount= len(inst.services)
        for serv_index in range(services_amount):
            serv= inst.services[serv_index]
            if serv.spread==0 and serv.dependencies==[]:
                empty_serv= empty_serv + 1
            else:
                true_serv= true_serv + 1
        print("total services:",services_amount)
        print("true services:",true_serv)
        print("empty services:",empty_serv)
        print()
