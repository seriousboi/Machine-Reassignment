from structures import *



def total_cost_assesser(assignment,instance):

    load_cost= load_cost_assesser(assignment,instance)
    balance_cost= balance_cost_assesser()
    process_move_cost= process_move_cost_assesser()*instance.process_move_cost_weight
    service_move_cost= service_move_cost_assesser()*instance.service_move_cost_weight
    machine_move_cost= machine_move_cost_assesser()*instance.machine_move_cost_weight

    total_cost= load_cost+balance_cost+process_move_cost+service_move_cost+machine_move_cost
    return total_cost



def load_cost_assesser(assignment,instance):
    load_cost= 0

    resources_amount= len(instance.resources)
    for res_index in range(resources_amount):
        resource_load_cost= resource_load_cost_assesser(res_index,assignment,instance)
        load_cost= load_cost + resource_load_cost

    return load_cost



def resource_load_cost_assesser(res_index,assignment,instance):
    resource_load_cost= 0

    machines_amount= len(instance.machines)
    for mech_idex in range(machines_amount):
        resource_usage=0 #reprend ici
        soft_cap= instance.machines[mech_idex].safety_capacities[res_index]
        machine_resource_load_cost= max(0,)

    return 0



def balance_cost_assesser():
    return 0



def process_move_cost_assesser():
    return 0



def service_move_cost_assesser():
    return 0



def machine_move_cost_assesser():
    return 0
