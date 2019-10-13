


class Instance():
    def __init__(self,resources,machines,services,processes,objectives,process_move_cost,service_move_cost,machine_move_cost,assignment):
        self.resources= resources #list of resources
        self.machines= machines #list of machines
        self.services= services #list of services
        self.processes= processes #list of processes
        self.objectives= objectives #list of objectives
        self.process_move_cost_weight= process_move_cost #integer
        self.service_move_cost_weight= service_move_cost #integer
        self.machine_move_cost_weight= machine_move_cost #integer
        self.assignment= assignment #assignment

        self.services_processes= None #if defined: list of list of integers
        self.neighborhoods_amount= None #if defined: integer

    def display_resources(self):
        print(len(self.resources))
        for res in self.resources:
            res.display()

    def display_machines(self):
        print(len(self.machines))
        for mach in self.machines:
            mach.display()

    def display_services(self):
        print(len(self.services))
        for ser in self.services:
            ser.display()

    def display_processes(self):
        print(len(self.processes))
        for pro in self.processes:
            pro.display()

    def display_objectives(self):
        print(len(self.objectives))
        for obj in self.objectives:
            obj.display()

    def display_costs(self):
        print(self.process_move_cost_weight,self.service_move_cost_weight,self.machine_move_cost_weight)

    def display_assignment(self):
        self.assignment.display()

    def display(self):
        self.display_assignment()
        self.display_resources()
        self.display_machines()
        self.display_services()
        self.display_processes()
        self.display_objectives()
        self.display_costs()

    def display_amounts(self):
        print(len(self.resources),"resources")
        print(len(self.machines),"machines")
        print(len(self.services),"services")
        print(len(self.processes),"processes")
        print(len(self.objectives),"objectives")

    def get_neighborhoods_amount(self):

        if self.neighborhoods_amount != None:
            return self.neighborhoods_amount

        else:
            neighborhoods_amount= -1
            machines_amount= len(self.machines)
            for mech_index in range(machines_amount):
                mech_neighborhood= self.machines[mech_index].neighborhood
                if mech_neighborhood > neighborhoods_amount:
                    neighborhoods_amount= mech_neighborhood
            self.neighborhoods_amount= neighborhoods_amount + 1
            return neighborhoods_amount + 1

    def get_services_processes(self):

        if self.services_processes != None:
            return self.services_processes

        else:

            services_amount= len(self.services)
            processes_amount= len(self.processes)
            self.services_processes= []
            for i in range(services_amount):
                self.services_processes= self.services_processes + [[]]

            for proc_index in range(processes_amount):
                serv_index= self.processes[proc_index].service
                self.services_processes[serv_index]= self.services_processes[serv_index] + [proc_index]

            return self.services_processes



class resource():
    def __init__(self,transitivity,load_cost):
        self.transitivity= transitivity #bool
        self.load_cost= load_cost #integer

    def display(self):
        print(self.transitivity,self.load_cost)




class machine():
    def __init__(self,neighborhood,location,capacities,safety_capacities,move_costs):
        self.neighborhood= neighborhood #integer
        self.location= location #integer
        self.capacities= capacities #list of integers
        self.safety_capacities= safety_capacities #list of integers
        self.move_costs= move_costs #list of integers

    def display(self):
        print(self.neighborhood,self.location,self.capacities,self.safety_capacities,self.move_costs)



class service():
    def __init__(self,spread,dependencies):
        self.spread= spread #integer
        self.dependencies= dependencies #list of integers

    def display(self):
        print(self.spread,self.dependencies)



class process():
    def __init__(self,service,requirements,move_cost):
        self.service= service #integer
        self.requirements= requirements #list of integers
        self.move_cost= move_cost #integer

    def display(self):
        print(self.service,self.requirements,self.move_cost)



class objective():
    def __init__(self,balance,weight):
        self.balance= balance #list of three integers
        self.weight= weight  #integer

    def display(self):
        print(self.balance,self.balance_cost)



class assignment():
    def __init__(self,assignment_list):
        self.assignment_list= assignment_list #list of integers
        self.lenght= len(assignment_list) #integer
        self.machine_assignment_list= None #if defined: list of list of integers

    def display(self):
        print(self.assignment_list)

    def get_machine_assignment(self,machines_amount):
        if self.machine_assignment_list != None:
            return self.machine_assignment_list
        else:
            machine_assignment_list= []
            for mech_index in range(machines_amount):
                machine_assignment_list= machine_assignment_list + [[]]

            assignment_size= self.lenght
            for proc_index in range(assignment_size):
                mech= self.assignment_list[proc_index]
                machine_assignment_list[mech]= machine_assignment_list[mech] + [proc_index]

            self.machine_assignment_list= machine_assignment_list
            return machine_assignment_list

    def move_process(self,proc_index,mech_index):

        if self.machine_assignment_list != None:
            old_mech_index= self.assignment_list[proc_index]
            self.machine_assignment_list[old_mech_index].remove(proc_index)
            self.machine_assignment_list[mech_index].append(proc_index)

        self.assignment_list[proc_index]= mech_index


class solution():
    def __init__(self,ass,inst):
        self.assignment= ass #assignment
        self.instance= inst #instance
        self.resource_usage_on_machine= [] #list of list of if defined: int
        self.services_on_machine= [] #list of if defined: list of int
        self.services_locations= None #if defined: list of list of int
        self.neighborhoods_services= None #if defined: list of list of int

        machines_amount= len(inst.machines)
        resources_amount= len(inst.resources)

        for res_index in range(resources_amount):
            self.resource_usage_on_machine= self.resource_usage_on_machine + [[None]*machines_amount]
        self.services_on_machine= [None]*machines_amount


    def display(self):
        self.instance.display()
        self.assignment.display()



    def get_resource_usage_on_machine(self,res_index,mech_index):

        if self.resource_usage_on_machine[res_index][mech_index] != None:
            return self.resource_usage_on_machine[res_index][mech_index]

        else:
            instance= self.instance
            ass= self.assignment

            machines_amount= len(instance.machines)
            machine_assignment= ass.get_machine_assignment(machines_amount)
            machine_assignment_instance= instance.assignment.get_machine_assignment(machines_amount)

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
            self.resource_usage_on_machine[res_index][mech_index]= total_usage
            return total_usage



    def get_services_on_machine(self,mech_index):

        if self.services_on_machine[mech_index] != None:
            return self.services_on_machine[mech_index]

        else:
            instance= self.instance
            ass= self.assignment

            servs_on_mech= []
            machines_amount= len(instance.machines)
            machine_assignment= ass.get_machine_assignment(machines_amount)[mech_index]
            assigned_processes_ammount= len(machine_assignment)
            for assigned_proc_index in range(assigned_processes_ammount):
                proc_index= machine_assignment[assigned_proc_index]
                serv= instance.processes[proc_index].service
                servs_on_mech= servs_on_mech + [serv]

            self.services_on_machine[mech_index]= servs_on_mech
            return servs_on_mech



    def get_services_locations(self):

        if self.services_locations != None:
            return self.services_locations

        else:
            instance= self.instance
            ass= self.assignment

            self.services_locations= []
            services_amount= len(instance.services)
            for serv_index in range(services_amount):
                self.services_locations= self.services_locations + [[]]

            processes_amount= ass.lenght
            for proc_index in range(processes_amount):
                proc= instance.processes[proc_index]
                serv_index= proc.service
                mech_index= ass.assignment_list[proc_index]
                mech= instance.machines[mech_index]
                location= mech.location

                if location not in self.services_locations[serv_index]:
                    self.services_locations[serv_index]= self.services_locations[serv_index] + [location]

            return self.services_locations



    def get_neighborhoods_services(self):

        if self.neighborhoods_services != None:
            return self.neighborhoods_services

        else:
            instance= self.instance
            ass= self.assignment

            neighborhoods_amount= self.instance.get_neighborhoods_amount()
            self.neighborhoods_services= []
            for nei in range(neighborhoods_amount):
                self.neighborhoods_services= self.neighborhoods_services + [[]]

            processes_amount= ass.lenght
            for proc_index in range(processes_amount):
                proc= instance.processes[proc_index]
                serv_index= proc.service
                mech_index= ass.assignment_list[proc_index]
                mech= instance.machines[mech_index]
                neighborhood= mech.neighborhood

                if serv_index not in self.neighborhoods_services[neighborhood]:
                    self.neighborhoods_services[neighborhood]= self.neighborhoods_services[neighborhood] + [serv_index]

            return self.neighborhoods_services
