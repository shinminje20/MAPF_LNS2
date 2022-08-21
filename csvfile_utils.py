import csv
from os import listdir
from os.path import isfile, join
import statistics
import fileinput
import sys
import glob

def calculate_pstdev():
    file_names = ["Berlin_1_256_even", "Berlin_1_256_random"]


    for file_name in file_names:
        
        files = glob.glob("results/results_scen_"+ file_name + "*")
        print("files: ", files)

        for file in files:
            num_iteration =0
            avg_cost = 0
            avg_duration = 0
            avg_replans = 0
            
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
                temp = lines[-1].split(', ')
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
        
def calculate_map_to_map_pstdev():
    file_names = ["Berlin_1_256_even", "Berlin_1_256_random"]


    for file_name in file_names:
        
        files = glob.glob("results/results_scen_"+ file_name + "*")
        print("files: ", files)

        pstdev_of_instances = []
        total_durations_of_instances = []
        avg_durations_of_instances = []
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
                temp = lines[-1].split(', ')
                avg_duration = temp[2].split(' ')[1]
                avg_durations_of_instances.append(float(avg_duration))
                total_durations_of_instances += total_duration
                pstdev = statistics.pstdev(total_duration)
                print("pstdev: ", pstdev)
            f.close()


            with open(file, "r") as f:
                lines = f.readlines()
                temp = lines[-1].split(', ')
                pstdev = temp[4].split(' ')[1]
                pstdev_of_instances.append(float(pstdev))
                print("pstdev: ", pstdev)
            f.close()
        print("total_durations_of_instances: ", total_durations_of_instances)
        print("pstdev_of_instances: ", pstdev_of_instances)
        print("avg_durations_of_instances: ", avg_durations_of_instances)
        print("===============================================================\n\n")
        with open("results/Map_Summary_" + file_name + ".csv", "w") as f:
            f.write("pstdev_of_instances: {}, pstdev_of_avgs\n".format(statistics.pstdev(total_durations_of_instances), statistics.pstdev(avg_durations_of_instances)))
        f.close()
# calculate_pstdev()
calculate_map_to_map_pstdev()