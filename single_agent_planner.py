from sqlite3 import Timestamp
import time as timer
import heapq
import random
from tkinter.messagebox import NO
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost


def detect_collision(path1, path2):
    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.
    # longer path
    maxLen = 0
    if len(path1) > len(path2):
        maxLen = len(path1)
    else:
        maxLen = len(path2)

    # vertext collision
    for timestep in range(maxLen):
        if get_location(path1, timestep) == get_location(path2, timestep):
            return get_location(path1, timestep), timestep

    # edge collision
    for timestep in range(maxLen):
        if get_location(path1, timestep) == get_location(path2, timestep+1):
            if get_location(path1, timestep+1) == get_location(path2, timestep):
                return [get_location(path1, timestep), get_location(path1, timestep+1)], timestep+1

    return (-1, -1), -1  # ex. loc = (1,1), timestep = 1


def detect_collisions(paths):
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.
    collisions = []
    numAgent = len(paths)
    for i in range(numAgent):
        for j in range(i+1, numAgent, 1):
            loc, timestep = detect_collision(paths[i], paths[j])
            if timestep == -1:
                continue
            if timestep != None:
                if isinstance(loc, list) == False:  # vertex
                    collision = {'a1': i, 'a2': j, 'loc': [
                        loc], 'timestep': timestep}
                    collisions.append(collision)
                else:  # edge collision
                    collision1 = {'a1': i, 'a2': j, 'loc': [
                        loc[0], loc[1]], 'timestep': timestep}
                    collisions.append(collision1)

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
    # vertex
    if (len(collision['loc']) == 1):
        constraint1 = {
            'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']}
        constraint2 = {
            'agent': collision['a2'], 'loc': collision['loc'], 'timestep': collision['timestep']}
        constraints.append(constraint1)
        constraints.append(constraint2)

    # edge
    if (len(collision['loc']) == 2):
        constraint = {
            'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']}
        constraint2 = {
            'agent': collision['a2'], 'loc': [collision['loc'][1], collision['loc'][0]], 'timestep': collision['timestep']}
        constraints.append(constraint)
        constraints.append(constraint2)

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

    pass


class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost'], len(
            node['collisions']), self.num_of_generated, node))
        print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint=True):
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()

        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        root = {'cost': 0,
                'constraints': [],
                'paths': [],
                'collisions': []}
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root['constraints'])
            if path is None:
                raise BaseException('No solutions')
            root['paths'].append(path)

        root['cost'] = get_sum_of_cost(root['paths'])
        root['collisions'] = detect_collisions(root['paths'])
        self.push_node(root)  # push to open list

        # Task 3.1: Testing
        # print("collisions")
        # print(root['collisions'])

        # Task 3.2: Testing
        # print("constraints")
        # for collision in root['collisions']:
        #     print(standard_splitting(collision))

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit

        while (len(self.open_list) > 0):
            p = self.pop_node()
            collisions = detect_collisions(p['paths'])
            p['collisions'] = collisions
            if (len(collisions) == 0):
                self.print_results(p)
                print("path")
                print(p['paths'])
                return p['paths']
            collision = collisions[0]
            constraints = standard_splitting(collision)

            for constraint in constraints:
                child = {'cost': 0, 'constraints': [],
                         'paths': [], 'collisions': []}

                if len(constraint['loc']) >= 3:
                    continue

                if isinstance(constraint, dict):
                    child['constraints'].append(constraint)
                for constraintP in p['constraints']:
                    child['constraints'].append(constraintP)

                child['paths'] = p['paths']
                child['collisions'] = detect_collisions(child['paths'])
                child['cost'] = get_sum_of_cost(child['paths'])

                agent = constraint['agent']
                paths = a_star(self.my_map, self.starts[agent], self.goals[agent],
                               self.heuristics[agent], agent, child['constraints'])
                if paths is not None:
                    child['paths'][agent] = paths
                    child['collisions'] = detect_collisions(child['paths'])
                    child['cost'] = get_sum_of_cost(child['paths'])
                    print("!!!!!!!!!!!")
                    print("child = " + str(child))
                    self.push_node(child)

        return BaseException('No solutions')

        # solution return before no high level implimentation
        # self.print_results(root)
        # return root['paths']

    def print_results(self, node):
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(node['paths'])))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
        print(node['paths'])
