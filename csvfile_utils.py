import csv
from os import listdir
from os.path import isfile, join
import statistics
import fileinput
import sys
import glob

def calculate_pstdev(file_names):
    


    for file_name in file_names:
        
        files = glob.glob("results/results_scen_"+ file_name + "*")
        print("files: ", files)

        for file in files:
            num_iteration =0
            avg_cost = 0
            avg_duration = 0
            avg_replans = 0
            print("=================== FILE: ====================== ")
            print(file)
            print("=================== ======== ====================== ")
            success_ratio = 0
            with open(file, "r") as f:
                lines = f.readlines()
                total_duration = []
                for line in lines:
                    line = line.split(',')
                    for i in line:
                        if i.startswith(' duration'):
                            d = int(i.split(' ')[2])
                                
                            total_duration.append(d)
                for i in range(len(lines)-1, -1, -1):
                    if lines[i] != "\n":
                        temp = lines[i].split(', ')
                        break
                num_iteration = temp[0].split(':')[2]
                avg_cost = temp[1].split(' ')[1]
                avg_duration = temp[2].split(' ')[1]
                avg_replans = temp[3].split(' ')[1]
                
                success_ratio = temp[-1].split(' ')[1]
                print(temp)
                print(total_duration)
                pstdev = statistics.pstdev(total_duration)
                print("pstdev: ", pstdev)
            f.close()

            a_file = open(file, "r")
            list_of_lines = a_file.readlines()
            list_of_lines[-1] = "Instance_summary: num_iteration: " + num_iteration + ", avg_cost: " + avg_cost + ", avg_duration: " + avg_duration + ", avg_replans: " + avg_replans + ", pstd_duration: " + str(pstdev) + ", success_ratio: " + success_ratio + "\n"
            a_file = open(file, "w")
            a_file.writelines(list_of_lines)
            a_file.close()
        
def calculate_map_to_map_pstdev(file_names):


    for file_name in file_names:
        
        files = glob.glob("results/results_scen_"+ file_name + "*")
        print("files: ", files)

        avg_durations_of_instances = []
        pstdev_over_averages = []

        for file in files:
            
            with open(file, "r") as f:
                lines = f.readlines()
                total_duration = []
                for line in lines:
                    line = line.split(',')
                    for i in line:
                        if i.startswith(' duration'):
                            d = int(i.split(' ')[2])
                                
                            total_duration.append(d)
                for i in range(len(lines)-1, -1, -1):
                    if lines[i] != "\n":
                        temp = lines[i].split(', ')
                        break
                avg_duration = temp[2].split(' ')[1]
                # print(" temp[4].split(' '): ",  temp[4].split(' '))
                pstdev = temp[4].split(' ')[1]
                
                
                avg_durations_of_instances.append(float(avg_duration))
                pstdev_over_averages.append(float(pstdev)/float(avg_duration))
                
            f.close()

        print("avg_durations_of_instances: ", avg_durations_of_instances)
        print("pstdev_over_averages: ", pstdev_over_averages)
        print("===============================================================\n\n")
        with open("MapSummary/" + file_name + ".csv", "w") as f:
            f.write("avg_of_avg_durations: {}, pstdev_of_avgs_durations: {}\n avg_of_ pstdev/avg: {}, pstdev_of_pstdev/avg: {}\n".format(
                statistics.mean(avg_durations_of_instances), 
                statistics.pstdev(avg_durations_of_instances), 
                statistics.mean(pstdev_over_averages), 
                statistics.pstdev(pstdev_over_averages)))
        f.close()

file_names = [ "empty_8_8_even", "maze_32_32_4_even", "maze_32_32_4_random", "empty_8_8_random", "empty_48_48_even", 
"empty_48_48_random", "maze_32_32_2_even", "maze_32_32_2_random", "empty_16_16_even", "empty_16_16_random", "empty_32_32_even", "empty_32_32_random", 
"warehouse_10_20_10_2_1_even", "warehouse_10_20_10_2_1_random", "warehouse_10_20_10_2_2_even", "warehouse_10_20_10_2_2_random", "warehouse_20_40_10_2_1_even", "warehouse_20_40_10_2_2_random", "maze_128_128_10_even" ]

calculate_pstdev(file_names)
calculate_map_to_map_pstdev(file_names)