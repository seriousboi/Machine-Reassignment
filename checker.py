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

        servs_on_mech= sol.get_services_on_machine(mech_index)
        servs_on_mech_amount= len(servs_on_mech)
        for serv_on_mech_index in range(servs_on_mech_amount):
            serv= servs_on_mech[serv_on_mech_index]

            if serv in servs_on_mech[0:serv_on_mech_index]:
                proc_index_1= machine_assignment[mech_index][find(servs_on_mech,serv)]
                proc_index_2= machine_assignment[mech_index][serv_on_mech_index]
                print("conflict, processes",proc_index_1,"and",proc_index_2,"from service",serv,"on machine",mech_index)
                return False

    return True



def spread_constraints(sol):
    instance= sol.instance
    ass= sol.assignment

    servs_loc= sol.get_services_locations()

    services_amount= len(instance.services)
    for serv_index in range(services_amount):
        spread_min= instance.services[serv_index].spread
        spreading= len(servs_loc[serv_index])
        if spreading < spread_min:
            print("service",serv_index,"not spread engouh,",spreading,"instead of",spread_min,"locations covered:",servs_loc[serv_index])
            return False

    return True



def dependency_constraints(sol):
    instance= sol.instance
    ass= sol.assignment

    nei_servs= sol.get_neighborhoods_services()

    neighborhoods_amount= instance.get_neighborhoods_amount()
    for neighborhood in range(neighborhoods_amount):
        for serv_index in nei_servs[neighborhood]:
            dependencies= instance.services[serv_index].dependencies
            for dependency in dependencies:
                if dependency not in nei_servs[neighborhood]:
                    print("dependency missing, service",dependency,"missing for service",serv_index,"in neighborhood",neighborhood)
                    return False
    return True



def find(list,goal):
    for i in range(len(list)):
        if list[i] == goal:
            return i
    return None
