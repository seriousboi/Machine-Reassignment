from structures import *
from parsers import *
from checker import *
from assesser import *
from benchmark import *



def services_bug():
    for i in range(10):
        print("b"+str(i+1))
        inst= load_instance("b_"+str(i+1))
        true_serv=0
        empty_serv=0
        services_amount= len(inst.services)
        for serv_index in range(services_amount):
            serv= inst.services[serv_index]
            if serv.spread==0 and serv.dependencies==[]:
                empty_serv= empty_serv + 1
            else:
                true_serv= true_serv + 1
        print("total services:",services_amount)
        print("true services:",true_serv)
        print("empty services:",empty_serv)
        print()
