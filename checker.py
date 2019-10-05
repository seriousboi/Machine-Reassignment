from structures import *



def assignment_checker(assignment,instance,check_consistency):

    if check_consistency:
        if consistency_checker(assignment,instance) == False:
            return False

    constraints= [capacity_constraints,
    conflict_constraints,
    spread_constraints,
    dependency_constraints]

    for constraint in constraints:
        if constraint(assignment,instance) == False:
            return False

    return True



def consistency_checker(assignment,instance):
    processes_amount= len(instance.processes)
    machines_amount= len(instance.machines)
    assignment_size= len(assignment)

    if assignment_size > processes_amount:
        print("too many processes,",assignment_size,"instead of",processes_amount)
        return False
    if assignment_size < processes_amount:
        print("too few processes,",assignment_size,"instead of",processes_amount)
        return False


    for i in range(assignment_size):
        if assignment[i] >= machines_amount:
            print("impossible assignment, process",i,"assigned to machine",str(assignment[i])+", only",machines_amount,"machines")
            return False

    return True



def capacity_constraints(assignment,instance):
    machines_amount= len(instance.machines)
    resources_amount= len(instance.resources)
    machine_assignment= get_machine_assignment(assignment,machines_amount)
    machine_assignment_instance= get_machine_assignment(instance.assignment,machines_amount)

    for mech_index in range(machines_amount):
        mech= instance.machines[mech_index]
        for res_index in range(resources_amount):

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
            capacity= mech.capacities[res_index]
            if total_usage > capacity:
                print("not enough capacity,","resource",res_index,"on machine",mech_index,"with",capacity,"capacity and",total_usage,"usage by processes:",machine_assignment[mech_index])
                return False

    return True



def conflict_constraints(assignment,instance):
    machines_amount= len(instance.machines)
    machine_assignment= get_machine_assignment(assignment,machines_amount)

    for mech_index in range(machines_amount):
        services_on_mech= []

        assigned_processes_ammount= len(machine_assignment[mech_index])
        for assigned_proc_index in range(assigned_processes_ammount):
            proc_index= machine_assignment[mech_index][assigned_proc_index]
            serv= instance.processes[proc_index].service

            if serv in services_on_mech:
                proc_index_2= machine_assignment[mech_index][find(services_on_mech,serv)]
                print("conflict, processes",proc_index,"and",proc_index_2,"from service",serv,"on machine",mech_index)
                return False
            services_on_mech= services_on_mech + [serv]

    return True



def spread_constraints(assignment,instance):
    services_locations= []
    services_amount= len(instance.services)
    for serv_index in range(services_amount):
        services_locations= services_locations + [[]]

    processes_amount= len(assignment)
    for proc_index in range(processes_amount):
        proc= instance.processes[proc_index]
        serv_index= proc.service
        mech_idex= assignment[proc_index]
        mech= instance.machines[mech_idex]
        location= mech.location

        if location not in services_locations[serv_index]:
            services_locations[serv_index]= services_locations[serv_index] + [location]

    for serv_index in range(services_amount):
        spread_min= instance.services[serv_index].spread
        spreading= len(services_locations[serv_index])
        if spreading < spread_min:
            print("service",serv_index,"not spread engouh,",spreading,"instead of",spread_min,"locations covered:",services_locations[serv_index])
            return False

    return True



def dependency_constraints(assignment,instance):
    neighborhoods_services= []
    neighborhoods_amount= find_neighborhoods_amount(instance)
    for neighborhood in range(neighborhoods_amount):
        neighborhoods_services= neighborhoods_services + [[]]

    processes_amount= len(assignment)
    for proc_index in range(processes_amount):
        proc= instance.processes[proc_index]
        serv_index= proc.service
        mech_idex= assignment[proc_index]
        mech= instance.machines[mech_idex]
        neighborhood= mech.neighborhood

        if serv_index not in neighborhoods_services[neighborhood]:
            neighborhoods_services[neighborhood]= neighborhoods_services[neighborhood] + [serv_index]

    for neighborhood in range(neighborhoods_amount):
        for serv_index in neighborhoods_services[neighborhood]:
            dependencies= instance.services[serv_index].dependencies
            for dependency in dependencies:
                if dependency not in neighborhoods_services[neighborhood]:
                    print("dependency missing, service",dependency,"missing for service",serv_index,"in neighborhood",neighborhood)
                    return False
    return True

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
