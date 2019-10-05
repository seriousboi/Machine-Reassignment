from structures import *



def assignment_checker(sol,check_consistency):

    if check_consistency:
        if consistency_checker(sol) == False:
            return False

    constraints= [capacity_constraints,
    conflict_constraints,
    spread_constraints,
    dependency_constraints]

    for constraint in constraints:
        if constraint(sol) == False:
            return False

    return True



def consistency_checker(sol):
    instance= sol.instance
    ass= sol.assignment

    processes_amount= len(instance.processes)
    machines_amount= len(instance.machines)
    assignment_size= len(ass.assignment_list)

    if assignment_size > processes_amount:
        print("too many processes,",assignment_size,"instead of",processes_amount)
        return False
    if assignment_size < processes_amount:
        print("too few processes,",assignment_size,"instead of",processes_amount)
        return False


    for i in range(assignment_size):
        if ass.assignment_list[i] >= machines_amount:
            print("impossible assignment, process",i,"assigned to machine",str(ass.assignment_list[i])+", only",machines_amount,"machines")
            return False

    return True



def capacity_constraints(sol):
    instance= sol.instance
    ass= sol.assignment

    machines_amount= len(instance.machines)
    resources_amount= len(instance.resources)

    for mech_index in range(machines_amount):
        mech= instance.machines[mech_index]
        for res_index in range(resources_amount):

            total_usage= sol.get_resource_usage_on_machine(res_index,mech_index)
            hard_cap= mech.capacities[res_index]
            if total_usage > hard_cap:
                print("not enough capacity,","resource",res_index,"on machine",mech_index,"with",hard_cap,"capacity and",total_usage,"usage by processes:",sol.assignment.machine_assignment_list[mech_index])
                return False

    return True



def conflict_constraints(sol):
    instance= sol.instance
    ass= sol.assignment

    machines_amount= len(instance.machines)
    machine_assignment= ass.get_machine_assignment(machines_amount)

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



def spread_constraints(sol):
    instance= sol.instance
    ass= sol.assignment

    services_locations= []
    services_amount= len(instance.services)
    for serv_index in range(services_amount):
        services_locations= services_locations + [[]]

    processes_amount= ass.lenght
    for proc_index in range(processes_amount):
        proc= instance.processes[proc_index]
        serv_index= proc.service
        mech_idex= ass.assignment_list[proc_index]
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



def dependency_constraints(sol):
    instance= sol.instance
    ass= sol.assignment

    neighborhoods_services= []
    neighborhoods_amount= instance.get_neighborhoods_amount()
    for neighborhood in range(neighborhoods_amount):
        neighborhoods_services= neighborhoods_services + [[]]

    processes_amount= ass.lenght
    for proc_index in range(processes_amount):
        proc= instance.processes[proc_index]
        serv_index= proc.service
        mech_idex= ass.assignment_list[proc_index]
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



def find(list,goal):
    for i in range(len(list)):
        if list[i] == goal:
            return i
    return None
