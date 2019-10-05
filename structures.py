


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
        self.assignment= assignment #list of integers

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
        print(self.assignment)

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
    def __init__(self,balance,balance_cost):
        self.balance= balance #list of three integers
        self.balance_cost= balance_cost #integer

    def display(self):
        print(self.balance,self.balance_cost)
