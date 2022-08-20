from loadscen import *
from prioritizedPlanning import *
from Utils import *
from LNSUtil import *
import heapq
import argparse
from ReplanCBSSIPPS import LNS2CBS
from ReplanPPSIPPS import LNS2PP
import glob
import time as timer

SOLVER = "PPSIPPS"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')

    parser.add_argument('--solver', type=str, default=SOLVER,
                        help='The solver to use (one of: {CBSSIPPS, PPSIPPS}), defaults to ' + str(SOLVER))

    parser.add_argument('--num_agents', type=int, default=10,
                        help='Number of agents, defaults to 10')

    parser.add_argument('--num_neighbour', type=int, default=5,
                        help='number of neighbourhood, defaults to 5')
    
    parser.add_argument('--time_limit', type=int, default=60,
                        help='time_limits for test, defaults to 1 min(60secs)')
    
    args = parser.parse_args()
    
    print(args)
    filename = args.instance
    filename = filename.replace("/", "_").replace("-", "_").replace(".scen", "").replace("*", "")
    # filename = filename.replace(".scen", '').replace("*")
    result_file_name = "results/results_" + filename + "_" + args.solver + ".csv"
    # raise 'asdf'
    result_file = open(result_file_name, "w", buffering=1)
    
    for file in sorted(glob.glob(args.instance)):
        

        print("***Import an instance***")

        instanceMap, instanceStarts, instanceGoals = loadScen(file, args.num_agents)
        print(file)
        print(instanceMap, instanceStarts, instanceGoals)
        map_width = len(instanceMap[0])
        map_height = len(instanceMap)
        timeLimit = args.time_limit #seconds
        numNeighbour = args.num_neighbour

        startTime = timer.time_ns()
        if args.solver == "PPSIPPS":
            print("***Run LNS2 PP with SIPPS***")
            print("running file: ", file)
            paths = LNS2PP(numNeighbour, map_width, map_height, instanceMap, instanceStarts, instanceGoals, timeLimit)

        elif args.solver == "CBSSIPPS":
            print("***Run LNS2 CBS with SIPPS***")
            print("running file: ", file)
            paths = LNS2CBS(numNeighbour, map_width, map_height, instanceMap, instanceStarts, instanceGoals, timeLimit)
        
        else:
            raise RuntimeError("Unknown solver!")
        endTime = timer.time_ns()
        duration = endTime - startTime

        #print(paths)
        cost = get_sum_of_cost(paths)
        result_file.write("{},{},{}\n".format(file, cost, duration))


    result_file.close()










