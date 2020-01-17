from tests import *



def main_menu():
    print("Machine Reassignment Optimizer")
    print("you are in the main menu")
    print("type 'cmd' to see all commands")
    print()
    names= ["a1_1","a1_2","a1_3","a1_4","a1_5",
    "a2_1","a2_2","a2_3","a2_4","a2_5",
    "b_1","b_2","b_3","b_4","b_5",
    "b_6","b_7","b_8","b_9","b_10"]

    running= True
    while running:

        command= input()

        if command == "cmd":
            print()
            print("optimize: runs the algorithm on the instance in the given time limit")
            print("benchmarks: tests the speed of basic functions on all instances")
            print("compare: compares the algorithm to his old version based on solutions already found")
            print("quit: quits the application")

        elif command == "quit":
            running= False

        elif command == "optimize":
            print()
            print("input the instance name or 'all' to optimize every instances")
            print("instances names are: a1_1 ... a1_5 a2_1 ... a2_5 b_1 ... b_10")
            print()
            command= input()
            print()

            if command == "all":
                print("input the time limit in seconds or 'none' to run the algorithm until the end")
                print()
                command= input()
                print()
                if command == "none":
                    time_limit= None
                else:
                    time_limit= int(command)
                test_optimization_a(sliding_optimization_2,time_limit)

            elif command in names:
                instance_name= command
                print("input the time limit in seconds or 'none' to run the algorithm until the end")
                print()
                command= input()
                print()
                if command == "none":
                    time_limit= None
                else:
                    time_limit= int(command)
                sliding_optimization_2(time_limit,instance_name)

            else:
                print("unknown name")

        elif command == "benchmarks":
            test_all_speed()

        elif command == "compare":
            compare_optimization_a("solutions//","sliding_1","sliding_2")

        else:
            print("unknown command")
        print()
    return
