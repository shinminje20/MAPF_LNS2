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
    # parser.add_argument('--instance', type=str, default=None,
    #                     help='The name of the instance file(s)')
    parser.add_argument('--scens', nargs='+', default=["scen/Berlin_1_256-even-.scen"],
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
    
    

    @timeout(args.time_limit)
    def run_single_iteartion():
        
            
        print("***Import an instance***")
        
        instanceMap, instanceStarts, instanceGoals = loadScen(file, args.num_agents)
        
        # print(file)
        # print(instanceMap, instanceStarts, instanceGoals)
        map_width = len(instanceMap[0])
        map_height = len(instanceMap)


        startTime = timer.time_ns()
        if args.solver == "PPSIPPS":
            print("***Run LNS2 PP with SIPPS***")
            print("running file: ", file)
            paths, num_replan = LNS2PP(numNeighbour, map_width, map_height, instanceMap, instanceStarts, instanceGoals)
           
        elif args.solver == "CBSSIPPS":
            print("***Run LNS2 CBS with SIPPS***")
            print("running file: ", file)
            paths, num_replan = LNS2CBS(numNeighbour, map_width, map_height, instanceMap, instanceStarts, instanceGoals)

        else:
            raise RuntimeError("Unknown solver!")
        endTime = timer.time_ns()
        
        duration = endTime - startTime
        cost = get_sum_of_cost(paths)
        
        return duration, cost, num_replan

    scenario = args.scens

    for instance in scenario:
        filename = instance
        filename = filename.replace("/", "_").replace("-", "_").replace(".scen", "").replace("*", "")
        # filename = filename.replace(".scen", '').replace("*")
        result_file_name = "results/results_" + filename + "_" + args.solver + "_" + "agents" + str(args.num_agents) + "_" + "neighbours" + str(args.num_neighbour) + "_" + "limits" + str(args.time_limit) + "_" + "iter" + str(args.num_iteration) + ".csv"
        # raise 'asdf'
        result_file = open(result_file_name, "w", buffering=1)
        numNeighbour = args.num_neighbour    
        num_iteration = args.num_iteration
        
        files = sorted(glob.glob(instance))

        for file in files:
            
            paths = None
            is_exceeded = False
            durations = []
            costs = []
            result_file.write("Start file: {},\n".format(file))
            num_time_exceeded = 0
            total_replans = 0
            for i in range(num_iteration):
                duration = 0
                cost = 0
                
                try:
                    duration, cost, num_replans = run_single_iteartion()
                    costs.append(cost)
                    durations.append(duration)
                    result_file.write("iteration: {}, cost: {}, duration: {}, num_raplans: {}\n".format(i, cost, duration, num_replans))
                    total_replans += num_replans
                except Exception as e:
                    num_time_exceeded += 1
                    is_exceeded = True
                    result_file.write("iteration: {}, exceeded time Limit!!\n".format(i))
                    print("e: ", e)

            if len(durations) == 0:
                avg_duration = 0
                std_duration = 0
                avg_cost = 0
                success_ratio = 0
                avg_replans = 0
            else:
                avg_duration = mean(durations) if len(durations) > 1 else durations[0]
                std_duration = stdev(durations) if len(durations) > 1 else 0
                avg_cost = mean(costs) if len(costs) > 1 else costs[0]
                success_ratio = (num_iteration - num_time_exceeded) / num_iteration * 100
                avg_replans = total_replans // (num_iteration - num_time_exceeded)
            

            result_file.write("Instance summary: num_iteration:{}, avg_cost: {}, avg_duration: {}, avg_replans: {}, std_duration: {}, success_ratio: {}%\n\n\n".format(num_iteration, avg_cost, avg_duration, avg_replans, std_duration, success_ratio))


        result_file.close()










