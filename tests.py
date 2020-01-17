from structures import *
from parsers import *
from checker import *
from assesser import *
from sliding import *
from random import *
from time import *
from copy import *
from glob import *



initial_costs= {
"a1_1":49528750,"a1_2":1061649570,"a1_3":583662270,"a1_4":632499600,"a1_5":782189690,
"a2_1":391189190,"a2_2":1876768120,"a2_3":2272487840,"a2_4":3223516130,"a2_5":787355300,
"b_1":7644173180,"b_2":5181493830,"b_3":6336834660,"b_4":9209576380,"b_5":12426813010,
"b_6":12749861240,"b_7":37946901700,"b_8":14068207250,"b_9":23234641520,"b_10":42220868760
}



def test_all_checkers_inst(times):
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        print("loading for test instance "+instance_name)
        print()
        inst= load_instance(instance_name)
        if test_all_checkers(inst,times) == False:
            return False
    for i in range(10):
        instance_name= "b_"+str(i+1)
        print("loading for test instance "+instance_name)
        print()
        inst= load_instance(instance_name)
        if test_all_checkers(inst,times) == False:
            ("error on instance "+instance_name)
            return False
    return True




def test_all_checkers(inst,times):

    tests= [test_consistency_checker,
    test_capacity_constraints_checker,
    test_conflict_constraints_checker,
    test_spread_constraints_checker,
    test_dependency_costraints_checker]

    for test in tests:
        if test(inst,times) == False:
            return False
    return True



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
        print("proc:",rand_index,"mech:",rand_ass)
        if consistency_checker(sol_1) == True:
            print("consistency check: no error showing up")
            return False

        rand_del= randrange(processes_amount)
        del(inst_2.assignment.assignment_list[rand_del])
        print("proc:",rand_del)
        if consistency_checker(sol_2) == True:
            print("consistency check: no error showing up")
            return False
        print()

    return True



def test_capacity_constraints_checker(inst,times):
    print("testing capacity constraints checker")
    print()
    for time in range(times):
        inst_1= deepcopy(inst)
        sol_1= solution(inst_1.assignment,inst_1)

        machines_amount= len(inst_1.machines)
        resources_amount= len(inst_1.resources)
        mech_index= randrange(machines_amount)
        res_index= randrange(resources_amount)
        mech_ass= inst_1.assignment.get_machine_assignment(machines_amount)

        processes_amount= len(mech_ass[mech_index])
        if processes_amount>0:
            proc_index= mech_ass[mech_index][randrange(processes_amount)]

            hard_cap= inst_1.machines[mech_index].capacities[res_index]
            inst_1.processes[proc_index].requirements[res_index]= hard_cap + 1
            print("mech:",mech_index,"res:",res_index,"proc:",proc_index,"cap:",hard_cap)
            if capacity_constraints(sol_1) == True:
                print("capacity constraints check: no error showing up")
                return False
        print()
    return True



def test_conflict_constraints_checker(inst,times):
    print("testing conflict constraints checker")
    print()
    for time in range(times):
        inst_1= deepcopy(inst)
        sol_1= solution(inst_1.assignment,inst_1)

        machines_amount= len(inst_1.machines)
        services_amount= len(inst_1.services)
        mech_index= randrange(machines_amount)
        serv_index= randrange(services_amount)

        mech_ass= inst_1.assignment.get_machine_assignment(machines_amount)
        processes_amount= len(mech_ass[mech_index])
        if processes_amount>=2:
            proc_index_1= mech_ass[mech_index][randrange(processes_amount)]
            proc_index_2= mech_ass[mech_index][randrange(processes_amount)]
            while proc_index_1 == proc_index_2:
                proc_index_2= mech_ass[mech_index][randrange(processes_amount)]

            inst_1.processes[proc_index_1].service= serv_index
            inst_1.processes[proc_index_2].service= serv_index

            print("mech:",mech_index,"serv:",serv_index,"proc_1:",proc_index_1,"proc_2:",proc_index_2)
            if conflict_constraints(sol_1) == True:
                print("conflict constraints constraints check: no error showing up")
                return False
        print()
    return True



def test_spread_constraints_checker(inst,times):
    print("testing spread constraints checker")
    print()
    for time in range(times):
        inst_1= deepcopy(inst)
        sol_1= solution(inst_1.assignment,inst_1)

        services_amount= len(inst_1.services)
        serv_index= randrange(services_amount)
        spread_min= inst_1.services[serv_index].spread
        add_spread= randrange(0,spread_min+1) + 1
        spread= len(sol_1.get_services_locations()[serv_index])

        total_spread= inst_1.services[serv_index].spread + spread + add_spread
        inst_1.services[serv_index].spread= total_spread

        print("serv:",serv_index,"spread_min:",spread_min,"spread:",spread,"add_spread:",add_spread,"total spread:",total_spread)
        if spread_constraints(sol_1) == True:
            print("spread constraints constraints check: no error showing up")
            return False
        print()
    return True



def test_dependency_costraints_checker(inst,times):
    print("testing dependency constraints checker")
    print()
    for time in range(times):
        inst_1= deepcopy(inst)
        sol_1= solution(inst_1.assignment,inst_1)

        neighborhoods_amount= inst_1.get_neighborhoods_amount()
        neighborhood= randrange(neighborhoods_amount)
        nei_servs= sol_1.get_neighborhoods_services()
        neighborhood_services_amount= len(nei_servs[neighborhood])
        serv_index= nei_servs[neighborhood][randrange(neighborhood_services_amount)]
        services_amount= len(inst_1.services)

        new_dep_index= randrange(services_amount+1)
        while new_dep_index in nei_servs[neighborhood]:
            new_dep_index= randrange(services_amount+1)

        inst_1.services[serv_index].dependencies.append(new_dep_index)
        print("neighborhood:",neighborhood,"service:",serv_index,"dependency:",new_dep_index)
        if dependency_constraints(sol_1) == True:
            print("dependency constraints constraints check: no error showing up")
            return False
        print()

    return True



def test_instance_speed(instance_name):
    print("instance "+instance_name+":")
    start= time()
    inst= load_instance(instance_name)
    load_time= time() - start
    sol= solution(inst.assignment,inst)
    print("load time:",round(load_time,2))
    assignment_checker(sol,True,True)
    check_time= time() - (start + load_time)
    print("check time:",round(check_time,2))
    print("initial_cost:",total_cost_assesser(sol))
    assessment_time= time() - (start + load_time + check_time)
    print("assessment time:",round(assessment_time,2))
    print()
    return load_time,check_time



def test_all_speed():
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        test_instance_speed(instance_name)
    for i in range(10):
        instance_name= "b_"+str(i+1)
        test_instance_speed(instance_name)



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



def location_neighborhood_study():
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        location_neighborhood_study_instance(instance_name)

    for i in range(10):
        instance_name= "b_"+str(i+1)
        location_neighborhood_study_instance(instance_name)



def location_neighborhood_study_instance(instance_name):
    print(instance_name+":")
    inst= load_instance(instance_name)
    inclusion= {}

    machines_amount= len(inst.machines)
    for mech_index in range(machines_amount):

        nei= inst.machines[mech_index].neighborhood
        loc= inst.machines[mech_index].location

        if loc in inclusion:
            inclusion[loc]= inclusion[loc] + [nei]
        else:
            inclusion[loc]= [nei]

    print(inclusion)
    print()
    return



def test_optimization_a(algorithm,time_limit):
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        algorithm(time_limit,instance_name)



def test_optimization_b(algorithm,time_limit):
    for i in range(10):
        instance_name= "b_"+str(i+1)
        algorithm(time_limit,instance_name)



def test_optimization(algorithm,time_limit):
    test_optimization_a(algorithm,time_limit)
    test_optimization_b(algorithm,time_limit)



def compare_optimization_instance(path,algo_name_1,algo_name_2,instance_name):
    global initial_costs
    path_length= len(path)
    solution_data_1= glob(path+algo_name_1+" "+instance_name+"*")[0]
    solution_data_1= solution_data_1[path_length-1:]
    solution_data_2= glob(path+algo_name_2+" "+instance_name+"*")[0]
    solution_data_2= solution_data_2[path_length-1:]

    initial_cost= initial_costs[instance_name]
    cost_1= int(find_word(solution_data_1,2)[1:])
    cost_2= int(find_word(solution_data_2,2)[1:])
    time_1= int(find_word(solution_data_1,3)[1:])
    time_2= int(find_word(solution_data_2,3)[1:])

    print("instance "+instance_name+":")
    print("initial cost:",initial_cost,algo_name_1+": "+str(round(100*cost_1/initial_cost))+"%",algo_name_2+": "+str(round(100*cost_2/initial_cost))+"%")
    print("time: "+algo_name_1+":",time_1,algo_name_2+":",time_2)
    if find_word(solution_data_1,4) == "optimum":
        if find_word(solution_data_2,4) == "optimum":
            print("both found a local optimum")
        else:
            print(algo_name_1+" found a local optimum")
    else:
        if find_word(solution_data_2,4) == "optimum":
            print(algo_name_2+" found a local optimum")
        else:
            print("both cut before local optimum")
    print()

    return



def find_word(sentence,n):
    return find_word_rec(sentence,0,len(sentence),n)



def find_word_rec(sentence,start,stop,n):
    if n == 0:
        return sentence[start:find_end_of_word(sentence,start,stop)+1]
    else:
        return find_word_rec(sentence,find_end_of_word(sentence,start,stop)+2,stop,n-1)



def find_end_of_word(sentence,start,stop):
    for index in range(start,stop):
        if sentence[index] == ' ':
            return index - 1
    return stop -1



def compare_optimization_a(path,algo_name_1,algo_name_2):
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        compare_optimization_instance(path,algo_name_1,algo_name_2,instance_name)



def compare_optimization_b(algorithm,time_limit):
    for i in range(10):
        instance_name= "b_"+str(i+1)
        compare_optimization_instance(path,algo_name_1,algo_name_2,instance_name)



def compare_optimization(algorithm,time_limit):
    compare_optimization_a(algorithm,time_limit)
    compare_optimization_b(algorithm,time_limit)



def test_movement_total_delta_assesser(instance_name,times):
    print(instance_name+":")
    print()
    inst= load_instance(instance_name)
    ass= assignment(deepcopy(inst.assignment.assignment_list))
    sol= solution(ass,inst)
    initial_cost= total_cost_assesser(sol)
    processes_amount= len(inst.processes)
    machines_amount= len(inst.machines)

    for time in range(times):
        proc_index= randrange(processes_amount)
        mech_index= randrange(machines_amount)
        old_mech_index= ass.assignment_list[proc_index]
        print("proc:",proc_index,"mech:",mech_index)
        delta= movement_total_delta_assesser(sol,initial_cost,proc_index,mech_index)
        print("delta:",delta)
        sol.assignment.move_process(proc_index,mech_index)
        real_delta= initial_cost - total_cost_assesser(sol)
        ass.move_process(proc_index,old_mech_index)
        print("real delta:",real_delta)
        print()
