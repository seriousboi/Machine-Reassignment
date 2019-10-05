from structures import *



def total_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment

    load_cost= load_cost_assesser(sol)
    balance_cost= balance_cost_assesser()
    process_move_cost= process_move_cost_assesser()*instance.process_move_cost_weight
    service_move_cost= service_move_cost_assesser()*instance.service_move_cost_weight
    machine_move_cost= machine_move_cost_assesser()*instance.machine_move_cost_weight

    total_cost= load_cost+balance_cost+process_move_cost+service_move_cost+machine_move_cost
    return total_cost



def load_cost_assesser(sol):
    instance= sol.instance
    ass= sol.assignment
    load_cost= 0

    machines_amount= len(instance.machines)
    resources_amount= len(instance.resources)
    for res_index in range(resources_amount):
        for mech_index in range(machines_amount):
            machine_resource_usage= sol.get_resource_usage_on_machine(res_index,mech_index)
            soft_cap= instance.machines[mech_index].safety_capacities[res_index]
            resource_load_cost= max(0,machine_resource_usage-soft_cap)
        weight= instance.resources[res_index].load_cost
        load_cost= load_cost + resource_load_cost*weight

    return load_cost



def balance_cost_assesser():
    return 0



def process_move_cost_assesser():
    return 0



def service_move_cost_assesser():
    return 0



def machine_move_cost_assesser():
    return 0
