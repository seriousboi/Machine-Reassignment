from structures import *
from parsers import *
from checker import *
from assesser import *
from time import *
from copy import *



def sliding_optimization_1(time_limit,instance_name):
    start= time()
    print("loading instance "+instance_name)
    print()
    inst= load_instance(instance_name)
    print("finished loading")
    print()
    ass= assignment(deepcopy(inst.assignment.assignment_list))
    sol= solution(ass,inst)
    best_cost= total_cost_assesser(sol)
    initial_cost= best_cost

    processes_amount= len(inst.processes)
    machines_amount= len(inst.machines)
    print(processes_amount,"processes and",machines_amount,"machines")
    print()

    print("optimising")
    print()
    all_singular_moves_tested= False
    while  not all_singular_moves_tested:

        improvement_found=  False
        for proc_index in range(processes_amount):
            for mech_index in range(machines_amount):

                if time_limit != None:
                    duration= time() - start
                    if duration >= time_limit:
                        print("time is up")
                        print("instance:",instance_name,"cost:",best_cost,"instead of",initial_cost,"time:",round(duration))
                        print("percentage of initial solution: "+str(round(100*best_cost/initial_cost,1))+"%")
                        print()
                        generate_assignment_file(ass,"sliding_1 "+instance_name+" C"+str(best_cost)+" T"+str(round(duration))+" ")
                        return ass

                old_mech_index= ass.assignment_list[proc_index]
                ass.move_process(proc_index,mech_index)
                sol= solution(ass,inst)

                if assignment_checker(sol,False,False):
                    new_cost= total_cost_assesser(sol)
                    if new_cost < best_cost:
                        print("improvement found: proc",proc_index,"to mech",mech_index)
                        print("new cost:",new_cost,"old cost:",best_cost)
                        print("percentage of initial solution: "+str(round(100*best_cost/initial_cost,1))+"%")
                        print()
                        best_cost= new_cost
                        improvement_found=  True
                        break

                ass.move_process(proc_index,old_mech_index)

                if (proc_index == processes_amount-1) and (mech_index == machines_amount-1):
                    all_singular_moves_tested= True

            if improvement_found:
                break

    duration= time() - start
    print("found local optimum before time limit")
    print("instance:",instance_name,"cost:",best_cost,"instead of",initial_cost,"time:",round(duration))
    print("percentage of initial solution: "+str(round(100*best_cost/initial_cost,1))+"%")
    print()
    generate_assignment_file(ass,"sliding_1 "+instance_name+" C"+str(best_cost)+" T"+str(round(duration))+" optimum ")
    return ass



def sliding_optimization_2(time_limit,instance_name):
    start= time()
    print("loading instance "+instance_name)
    print()
    inst= load_instance(instance_name)
    print("finished loading")
    print()
    ass= assignment(deepcopy(inst.assignment.assignment_list))
    sol= solution(ass,inst)
    best_cost= total_cost_assesser(sol)
    initial_cost= best_cost

    processes_amount= len(inst.processes)
    machines_amount= len(inst.machines)
    print(processes_amount,"processes and",machines_amount,"machines")
    print()

    print("optimising")
    print()
    all_singular_moves_tested= False
    while  not all_singular_moves_tested:

        for proc_index in range(processes_amount):
            best_move= None
            for mech_index in range(machines_amount):

                if time_limit != None:
                    duration= time() - start
                    if duration >= time_limit:
                        print("time is up")
                        print("instance:",instance_name,"cost:",best_cost,"instead of",initial_cost,"time:",round(duration))
                        print("percentage of initial solution: "+str(round(100*best_cost/initial_cost,1))+"%")
                        print()
                        generate_assignment_file(ass,"sliding_2 "+instance_name+" C"+str(best_cost)+" T"+str(round(duration))+" ")
                        return ass

                old_mech_index= ass.assignment_list[proc_index]
                ass.move_process(proc_index,mech_index)
                sol= solution(ass,inst)

                if assignment_checker(sol,False,False):
                    new_cost= total_cost_assesser(sol)
                    if new_cost < best_cost:
                        print("improvement found: proc",proc_index,"to mech",mech_index)
                        print("new cost:",new_cost,"old cost:",best_cost)
                        print("percentage of initial solution: "+str(round(100*best_cost/initial_cost,1))+"%")
                        print()
                        best_cost= new_cost
                        best_move= mech_index

                ass.move_process(proc_index,old_mech_index)

            if best_move != None:
                ass.move_process(proc_index,best_move)
                print("improvement applied")
                print()
                break
            elif proc_index == processes_amount - 1:
                all_singular_moves_tested= True



    duration= time() - start
    print("found local optimum before time limit")
    print("instance:",instance_name,"cost:",best_cost,"instead of",initial_cost,"time:",round(duration))
    print("percentage of initial solution: "+str(round(100*best_cost/initial_cost,1))+"%")
    print()
    generate_assignment_file(ass,"sliding_2 "+instance_name+" C"+str(best_cost)+" T"+str(round(duration))+" optimum ")
    return ass
