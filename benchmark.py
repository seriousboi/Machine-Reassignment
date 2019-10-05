from structures import *
from parsers import *
from checker import *
import time



def test_instance(instance_name):
    print("instance "+instance_name)
    start= time.time()
    inst= load_instance(instance_name)
    load_time= time.time() - start
    print("load time:",round(load_time,2))
    assignment_checker(inst.assignment,inst,True)
    check_time= time.time() - (start + load_time)
    print("check time:",round(check_time,2))
    print()
    return load_time,check_time



def test_a():
    for i in range(10):
        if i < 5:
            instance_name= "a1_"+str(i+1)
        else:
            instance_name= "a2_"+str(i-4)
        test_instance(instance_name)



def test_b():
    for i in range(10):
        instance_name= "b_"+str(i+1)
        test_instance(instance_name)



def test_all():
    test_a()
    test_b()
