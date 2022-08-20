import time as timer
import heapq
import random
import copy
from SIPPS2 import *
from Utils2 import *
from prioritizedPlanning import add_constraints_from_path


def detect_collision(path1, path2):
    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.
    for t in range(max(len(path1), len(path2))):
        if get_location(path1, t) == get_location(path2, t):
            #if t >= len(path1) or t >= len(path2):
            #    return {'loc': [get_location(path1, t)], 'timestep': (-1, t)}
            #else:
            #    return {'loc': [get_location(path1, t)], 'timestep': t}
            return {'loc': [get_location(path1, t)], 'timestep': t}
    for t in range(1, max(len(path1), len(path2))):
        if get_location(path1, t) == get_location(path2, t-1) and get_location(path2, t) == get_location(path1, t-1):
            return {'loc': [get_location(path1, t-1), get_location(path2, t-1)], 'timestep': t}
    return None
    


def detect_collisions(paths):
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.
    collisions = []
    for i in range(len(paths)):
        for j in range(i+1, len(paths)):
            temp = detect_collision(paths[i], paths[j])
            if temp != None:
                #if type(temp['timestep']) == type((1,1)):
                    #if temp['loc'] == get_location(paths[i], temp['timestep'][1]):
                    #    collisions.append({'a1': -1, 'a2': j, 'loc': temp['loc'], 'timestep': temp['timestep']})
                    #else:
                    #    collisions.append({'a1': i, 'a2': j, 'loc': temp['loc'], 'timestep': temp['timestep']})
                #else:
                collisions.append({'a1': i, 'a2': j, 'loc': temp['loc'], 'timestep': temp['timestep']})
    return collisions


def standard_splitting(collision):
    ##############################
    # Task 3.2: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the second agent to be at the
    #                            specified location at the specified timestep.
    #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the second agent to traverse the
    #                          specified edge at the specified timestep
    constraints = []
    if len(collision['loc']) == 1:
        constraints.append({'agent': collision['a1'], 'loc': collision['loc'][0], 'timestep': collision['timestep']})
        constraints.append({'agent': collision['a2'], 'loc': collision['loc'][0], 'timestep': collision['timestep']})
    else:
        constraints.append({'agent': collision['a1'], 'loc': (collision['loc'][0], collision['loc'][1]), 'timestep': collision['timestep']})
        constraints.append({'agent': collision['a2'], 'loc': (collision['loc'][1], collision['loc'][0]), 'timestep': collision['timestep']})
    return constraints


def disjoint_splitting(collision):
    ##############################
    # Task 4.1: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the same agent to be at the
    #                            same location at the timestep.
    #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the same agent to traverse the
    #                          specified edge at the specified timestep
    #           Choose the agent randomly
    constraints = []
    if len(collision['loc']) == 1:
        if random.randint(0, 1) >= 0.5:
            constraints.append({'agent': collision['a1'], 'loc': collision['loc'][0], 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a1'], 'loc': collision['loc'][0], 'timestep': collision['timestep']})
        else:
            constraints.append({'agent': collision['a2'], 'loc': collision['loc'], 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a2'], 'loc': collision['loc'], 'timestep': collision['timestep']})
    else:
        if random.randint(0, 1) >= 0.5:
            constraints.append({'agent': collision['a1'], 'loc': (collision['loc'][1], collision['loc'][0]), 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a1'], 'loc': (collision['loc'][1], collision['loc'][0]), 'timestep': collision['timestep']})
        else:
            constraints.append({'agent': collision['a2'], 'loc': (collision['loc'][1], collision['loc'][0]), 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a2'], 'loc': (collision['loc'][1], collision['loc'][0]), 'timestep': collision['timestep']})
    return constraints
    

def paths_violate_constraint(paths, constraint):
    collidingAgents = []
    for i in range(len(paths)):
        for t in range(len(paths[i])):
            if t == constraint['timestep'] and i != constraint['agent'] and paths[i][t] == constraint['loc'][0]:
                collidingAgents.append(i)
                #if len(constraint['loc']) == 2 and paths[i][t] == constraint['loc'][0]:
                #    collidingAgents.append(i)
                #elif: paths[i][t] == constraint['loc'][0]:
                #    collidingAgents.append(i)
    return collidingAgents


class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map, starts, goals, allPaths, neighbourhood):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.allPaths = allPaths
        self.neighbourhood = neighbourhood

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        #print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        #print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint=False):
        self.start_time = timer.time()

        neighbourhood_set = set(self.neighbourhood)
        init_constraints = {} 
        for i in range(len(self.allPaths)):
            if i not in neighbourhood_set:
                add_constraints_from_path(init_constraints, self.allPaths[i])

        init_paths = []
        for i in range(len(self.neighbourhood)):
            init_paths.append(self.allPaths[self.neighbourhood[i]])

        root = {'cost': get_sum_of_cost(init_paths),
                'constraints': [],
                'paths': init_paths,
                'collisions': detect_collisions(init_paths)}

        self.push_node(root)

        while len(self.open_list) > 0:
            currNode = self.pop_node()
            if len(currNode['collisions']) == 0:
                self.print_results(currNode)
                return currNode['paths']
            newConstraints = standard_splitting(currNode['collisions'][0]) #only standard splitting usable with SIPPS
            for con in newConstraints:
                #setting up inherited constraints and paths
                childCons = copy.copy(currNode['constraints']) #copy parent's dictionary references
                childPaths = copy.copy(currNode['paths'])

                #add new constraint
                agent = con['agent']
                childCons.append(con)
                #print(childCons)
                #build constraint table for this node
                hard_constraints = copy.copy(init_constraints)
                for con2 in childCons:
                    if agent == con2['agent']:
                        if con2['loc'] not in hard_constraints:
                            hard_constraints[con2['loc']] = []
                        heapq.heappush(hard_constraints[con2['loc']], con2['timestep'])

                newPath = sipps(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent], hard_constraints, {})
                if newPath != None:
                    childPaths[agent] = newPath
                    childNode = {'cost': get_sum_of_cost(childPaths),
                                'constraints': childCons,
                                'paths': childPaths,
                                'collisions': detect_collisions(childPaths)}
                    self.push_node(childNode)

        raise BaseException('No solutions')
        return None


    def print_results(self, node):
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(node['paths'])))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
