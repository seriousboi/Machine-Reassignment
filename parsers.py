from structures import *



def load_instance(instance_name):
    model_txt= get_txt("instances/model_"+instance_name+".txt")
    assignment_txt= get_txt("instances/assignment_"+instance_name+".txt")

    resources= get_resources(model_txt)
    resources_amount= len(resources)
    machines= get_machines(model_txt,resources_amount)
    services= get_services(model_txt)
    processes= get_processes(model_txt,resources_amount)
    objectives= get_objectives(model_txt)
    [process_move_cost,service_move_cost,machine_move_cost]= get_costs(model_txt)
    assignment= get_assignment(assignment_txt)

    instance= Instance(resources,machines,services,processes,objectives,process_move_cost,service_move_cost,machine_move_cost,assignment)
    return instance



def find_data_line(txt,data):
    return find_data_line_rec(txt,data,0)



def find_data_line_rec(txt,data,line):
    if data == 0:
        return line
    else:
        lines_between= int(txt[line].split()[0])+1
        return find_data_line_rec(txt,data-1,line+lines_between)



def get_resources(txt):
    resources_amount= int(txt[0].split()[0])

    resources= []
    for i in range(resources_amount):
        numbers= txt[1+i].split()

        if int(numbers[0]) == 0:
            transitivity= False
        else:
            transitivity= True
        load_cost= int(numbers[1])

        loaded_resource= resource(transitivity,load_cost)
        resources= resources + [loaded_resource]
    return resources



def get_machines(txt,resources_amount):
    machines_line= find_data_line(txt,1)
    machines_amount= int(txt[machines_line].split()[0])

    machines= []
    for i in range(machines_amount):
        numbers= txt[machines_line+i+1].split()

        neighborhood= int(numbers[0])

        location= int(numbers[1])

        capacities= []
        safety_capacities= []
        for i in range(resources_amount):
            capacity= int(numbers[2+i])
            capacities= capacities + [capacity]
            safety_capacity= int(numbers[2+i+resources_amount])
            safety_capacities= safety_capacities + [safety_capacity]

        move_costs= []
        for i in range(machines_amount):
            move_cost= int(numbers[2+i+2*resources_amount])
            move_costs= move_costs + [move_cost]

        loaded_machine= machine(neighborhood,location,capacities,safety_capacities,move_costs)
        machines= machines + [loaded_machine]
    return machines



def get_services(txt):
    services_line= find_data_line(txt,2)
    services_amount= int(txt[services_line].split()[0])

    services= []
    for i in range(services_amount):
        numbers= txt[services_line+i+1].split()

        spread= int(numbers[0])

        dependencies_amount= int(numbers[1])
        dependencies= []
        for i in range(dependencies_amount):
            dependency= int(numbers[2+i])
            dependencies= dependencies + [dependency]

        loaded_service= service(spread,dependencies)
        services= services + [loaded_service]
    return services



def get_processes(txt,resources_amount):
    processes_line= find_data_line(txt,3)
    processes_amount= int(txt[processes_line].split()[0])

    processes= []
    for i in range(processes_amount):
        numbers= txt[processes_line+i+1].split()

        service= int(numbers[0])

        requirements= []
        for i in range(resources_amount):
            requirement= int(numbers[1+i])
            requirements= requirements + [requirement]

        move_cost= int(numbers[1+resources_amount])

        loaded_process= process(service,requirements,move_cost)
        processes= processes + [loaded_process]
    return processes



def get_objectives(txt):
    objectives_line= find_data_line(txt,4)
    objectives_amount= int(txt[objectives_line].split()[0])

    objectives= []
    for i in range(objectives_amount):
        numbers= txt[objectives_line+i*2+1].split()

        resource_1= int(numbers[0])
        resource_2= int(numbers[1])
        target= int(numbers[2])
        balance= [resource_1,resource_2,target]

        balance_cost= int(txt[objectives_line+i*2+2].split()[0])

        loaded_objective= objective(balance,balance_cost)
        objectives= objectives + [loaded_objective]
    return objectives



def get_costs(txt):
    costs_line= len(txt)-1
    numbers= txt[costs_line].split()

    process_move_cost= int(numbers[0])
    service_move_cost= int(numbers[1])
    machine_move_cost= int(numbers[2])

    return [process_move_cost,service_move_cost,machine_move_cost]



def get_assignment(txt):
    numbers= txt[0].split()
    assignment= []
    for ass in numbers:
        assignment= assignment + [int(ass)]
    return assignment



def generate_assignment_file(assignment,file_name):
    file= open("solutions/"+file_name+".txt","w")
    for ass in assignment:
        file.write(str(ass)+" ")
    file.close()



def get_txt(file_name):
    file= open(file_name,"r")
    txt= file.readlines()
    file.close
    return txt
