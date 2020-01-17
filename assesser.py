from structures import *



def total_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment

    load_cost= load_cost_assesser(sol)
    balance_cost= balance_cost_assesser(sol)
    process_move_cost= process_move_cost_assesser(sol)*instance.process_move_cost_weight
    service_move_cost= service_move_cost_assesser(sol)*instance.service_move_cost_weight
    machine_move_cost= machine_move_cost_assesser(sol)*instance.machine_move_cost_weight

    total_cost= load_cost+balance_cost+process_move_cost+service_move_cost+machine_move_cost
    return total_cost



def load_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment

    machines_amount= len(instance.machines)
    resources_amount= len(instance.resources)

    load_cost= 0
    for mech_index in range(machines_amount):
        load_cost= load_cost + machine_load_cost_assesser(sol,mech_index)

    return load_cost



def machine_load_cost_assesser(sol,mech_index):
    instance= sol.instance
    ass= sol.assignment

    machine_load_cost= 0
    resources_amount= len(instance.resources)
    for res_index in range(resources_amount):

        machine_resource_usage= sol.get_resource_usage_on_machine(res_index,mech_index)
        soft_cap= instance.machines[mech_index].safety_capacities[res_index]
        weight= instance.resources[res_index].load_cost
        machine_load_cost= machine_load_cost + max(0,machine_resource_usage-soft_cap)*weight

    return machine_load_cost



def balance_cost_assesser(sol):
    instance= sol.instance

    total_balance_cost= 0
    machines_amount= len(instance.machines)
    for mech_index in range(machines_amount):

        total_balance_cost= total_balance_cost + machine_balance_cost_assesser(sol,mech_index)

    return total_balance_cost



def machine_balance_cost_assesser(sol,mech_index):
    instance= sol.instance
    ass= sol.assignment

    machine_balance_cost= 0
    objectives_amount= len(instance.objectives)
    for obj_index in range(objectives_amount):

        res_index_1= instance.objectives[obj_index].balance[0]
        res_index_2= instance.objectives[obj_index].balance[1]
        target= instance.objectives[obj_index].balance[2]
        weight= instance.objectives[obj_index].weight

        res_usage_on_mech_1= sol.get_resource_usage_on_machine(res_index_1,mech_index)
        res_usage_on_mech_2= sol.get_resource_usage_on_machine(res_index_2,mech_index)
        hard_cap_1= instance.machines[mech_index].capacities[res_index_1]
        hard_cap_2= instance.machines[mech_index].capacities[res_index_2]
        unused_res_1= hard_cap_1 - res_usage_on_mech_1
        unused_res_2= hard_cap_2 - res_usage_on_mech_2

        machine_balance_cost= machine_balance_cost + max(0, target*unused_res_1 - unused_res_2)*weight

    return machine_balance_cost



def process_move_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment
    total_process_move_cost= 0

    processes_amount= len(instance.processes)
    for proc_index in range(processes_amount):

        if ass.assignment_list[proc_index] != instance.assignment.assignment_list[proc_index]:
            process_move_cost= instance.processes[proc_index].move_cost
            total_process_move_cost= total_process_move_cost + process_move_cost

    return total_process_move_cost



def service_move_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment
    total_service_move_cost= 0

    services_processes= instance.get_services_processes()
    services_amount= len(instance.services)
    for serv_index in range(services_amount):
        service_move_cost=0
        for proc_index in services_processes[serv_index]:

            if ass.assignment_list[proc_index] != instance.assignment.assignment_list[proc_index]:
                service_move_cost= service_move_cost + 1

        total_service_move_cost= max(total_service_move_cost,service_move_cost)
    return total_service_move_cost



def machine_move_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment
    total_machine_move_cost= 0

    processes_amount= len(instance.processes)
    for proc_index in range(processes_amount):

        mech_source_index= ass.assignment_list[proc_index]
        mech_destination_index= instance.assignment.assignment_list[proc_index]

        if mech_source_index != mech_destination_index:
            machine_move_cost= instance.machines[mech_source_index].move_costs[mech_destination_index]
            total_machine_move_cost= total_machine_move_cost + machine_move_cost

    return total_machine_move_cost



def movement_total_delta_assesser(sol,old_cost,proc_index,mech_index):

    load_delta= movement_load_delta_assesser(sol,old_cost,proc_index,mech_index)
    balance_delta= movement_balance_delta_assesser(sol,old_cost,proc_index,mech_index)
    process_move_delta= movement_process_delta_assesser(sol,old_cost,proc_index,mech_index)
    service_move_delta= movement_service_delta_assesser(sol,old_cost,proc_index,mech_index)
    machine_move_delta= movement_machine_delta_assesser(sol,old_cost,proc_index,mech_index)
    delta= load_delta + balance_delta + process_move_delta + process_move_delta + service_move_delta + machine_move_delta

    return delta



def movement_load_delta_assesser(sol,old_cost,proc_index,new_mech_index):
    instance= sol.instance
    ass= sol.assignment
    old_mech_index= ass.assignment_list[proc_index]

    old_mech_old_load_cost= machine_load_cost_assesser(sol,old_mech_index)
    new_mech_old_load_cost= machine_load_cost_assesser(sol,new_mech_index)

    ass.move_process(proc_index,new_mech_index)
    new_sol= solution(ass,instance)
    old_mech_new_load_cost= machine_load_cost_assesser(new_sol,old_mech_index)
    new_mech_new_load_cost= machine_load_cost_assesser(new_sol,new_mech_index)
    ass.move_process(proc_index,old_mech_index)

    mech_delta= old_mech_old_load_cost + new_mech_old_load_cost - old_mech_new_load_cost - new_mech_new_load_cost
    print(mech_delta)
    return mech_delta



def movement_balance_delta_assesser(sol,old_cost,proc_index,new_mech_index):
    instance= sol.instance
    ass= sol.assignment
    old_mech_index= ass.assignment_list[proc_index]

    old_mech_old_balance_cost= machine_balance_cost_assesser(sol,old_mech_index)
    new_mech_old_balance_cost= machine_balance_cost_assesser(sol,new_mech_index)

    ass.move_process(proc_index,new_mech_index)
    new_sol= solution(ass,instance)
    old_mech_new_balance_cost= machine_balance_cost_assesser(new_sol,old_mech_index)
    new_mech_new_balance_cost= machine_balance_cost_assesser(new_sol,new_mech_index)
    ass.move_process(proc_index,old_mech_index)

    mech_delta= old_mech_old_balance_cost + new_mech_old_balance_cost - old_mech_new_balance_cost - new_mech_new_balance_cost

    return mech_delta



def movement_process_delta_assesser(sol,old_cost,proc_index,new_mech_index):
    instance= sol.instance
    ass= sol.assignment

    old_mech_index= ass.assignment_list[proc_index]
    og_mech_index= instance.assignment.assignment_list[proc_index]

    mech_delta= 0
    if old_mech_index == og_mech_index:
        if new_mech_index != og_mech_index:
            mech_delta= +instance.processes[proc_index].move_cost
    else:
        if new_mech_index == og_mech_index:
            mech_delta= instance.processes[proc_index].move_cost

    return mech_delta*instance.process_move_cost_weight



def movement_service_delta_assesser(sol,old_cost,proc_index,new_mech_index):
    #instance.service_move_cost_weight
    return 0



def movement_machine_delta_assesser(sol,old_cost,proc_index,new_mech_index):
    instance= sol.instance
    ass= sol.assignment

    old_mech_index= ass.assignment_list[proc_index]
    og_mech_index= instance.assignment.assignment_list[proc_index]

    mech_delta= instance.machines[og_mech_index].move_costs[old_mech_index] - instance.machines[og_mech_index].move_costs[new_mech_index]

    return mech_delta*instance.machine_move_cost_weight
