from structures import *



def get_machine_assignment(assignment,machines_amount):

    machine_assignment= []
    for i in range(machines_amount):
        machine_assignment= machine_assignment + [[]]

    assignment_size= len(assignment)
    for i in range(assignment_size):
        mech= assignment[i]
        machine_assignment[mech]= machine_assignment[mech] + [i]

    return machine_assignment



def find(list,goal):
    for i in range(len(list)):
        if list[i] == goal:
            return i
    return None



def find_neighborhoods_amount(instance):
    neighborhoods_amount= -1
    machines_amount= len(instance.machines)
    for mech_idex in range(machines_amount):
        mech_neighborhood= instance.machines[mech_idex].neighborhood
        if mech_neighborhood > neighborhoods_amount:
            neighborhoods_amount= mech_neighborhood
    return neighborhoods_amount + 1



def get_resource_usage_on_machine(res_index,mech_index,assignment,instance):
    machines_amount= len(instance.machines)
    machine_assignment= get_machine_assignment(assignment,machines_amount)
    machine_assignment_instance= get_machine_assignment(instance.assignment,machines_amount)

    resource_usage= 0
    transient_usage= 0
    for proc_index in machine_assignment[mech_index]:
        proc= instance.processes[proc_index]
        proc_requirement= proc.requirements[res_index]
        resource_usage= resource_usage + proc_requirement

    transient= instance.resources[res_index].transitivity
    if transient:
        for proc_index in machine_assignment_instance[mech_index]:
            if proc_index not in machine_assignment[mech_index]:
                proc= instance.processes[proc_index]
                proc_requirement= proc.requirements[res_index]
                transient_usage= transient_usage + proc_requirement

    total_usage= resource_usage + transient_usage
    return total_usage
