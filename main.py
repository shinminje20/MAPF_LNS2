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
from timeout import timeout
from statistics import stdev, mean

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

    parser.add_argument('--num_iteration', type=int, default=2,
                        help='number of times to run solver for each instance')
    
    args = parser.parse_args()
    
    print(args)
    filename = args.instance
    filename = filename.replace("/", "_").replace("-", "_").replace(".scen", "").replace("*", "")
    # filename = filename.replace(".scen", '').replace("*")
    result_file_name = "results/results_" + filename + "_" + args.solver + "_" + args.num_agents + "_" + args.num_neighbour + "_" + args.time_limit + "_" + args.num_iteration + ".csv"
    # raise 'asdf'
    result_file = open(result_file_name, "w", buffering=1)
    timeLimit = args.time_limit #seconds
    numNeighbour = args.num_neighbour    
    num_iteration = args.num_iteration
    num_time_exceeded = 0
    instance_total_avg_duration = 0
    instances = sorted(glob.glob(args.instance))

    @timeout(args.time_limit)
    def run_code():
        
            
        print("***Import an instance***")

        instanceMap, instanceStarts, instanceGoals = loadScen(file, args.num_agents)
        print(file)
        print(instanceMap, instanceStarts, instanceGoals)
        map_width = len(instanceMap[0])
        map_height = len(instanceMap)


        startTime = timer.time_ns()
        if args.solver == "PPSIPPS":
            print("***Run LNS2 PP with SIPPS***")
            print("running file: ", file)
            paths, num_replans = LNS2PP(numNeighbour, map_width, map_height, instanceMap, instanceStarts, instanceGoals, timeLimit)

        elif args.solver == "CBSSIPPS":
            print("***Run LNS2 CBS with SIPPS***")
            print("running file: ", file)
            paths, num_replans = LNS2CBS(numNeighbour, map_width, map_height, instanceMap, instanceStarts, instanceGoals, timeLimit)

        else:
            raise RuntimeError("Unknown solver!")
        endTime = timer.time_ns()
        
        duration = endTime - startTime
        cost = get_sum_of_cost(paths)
        
        return duration, cost, num_replans

    for file in instances:
        
        paths = None
        is_exceeded = False
        durations = []
        costs = []
        for i in range(num_iteration):
            duration = 0
            cost = 0
            
            try:
                duration, cost, num_replans = run_code()
                costs.append(cost)
                durations.append(duration)
            except:
                num_time_exceeded += 1
                is_exceeded = True
                break

        if is_exceeded:
            result_file.write("file: {} exceeded time Limit\n".format(file))
        else:
            avg_duration = mean(durations)
            std_duration = stdev(durations)
            avg_cost = mean(costs)
            
            instance_total_avg_duration += avg_duration
            result_file.write("file: {}, avg_cost: {}, num_iteration:{}, avg_duration: {}, std_duration: {}\n".format(file, avg_cost, num_iteration, avg_duration, std_duration))

    result_file.write("\n\nInstance summary: num_iteration for each case: {}, instance_avg_duration: {}, num_time_exceeded: {}, success_ratio: {}%\n".format(num_iteration, instance_total_avg_duration//(len(instances)-num_time_exceeded), num_time_exceeded, ((len(instances) - num_time_exceeded)/len(instances)) * 100 ))

    result_file.close()










