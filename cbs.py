import time as timer
import heapq
import random
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost


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
        constraints.append({'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']})
        constraints.append({'agent': collision['a2'], 'loc': collision['loc'], 'timestep': collision['timestep']})
    else:
        constraints.append({'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']})
        constraints.append({'agent': collision['a2'], 'loc': [collision['loc'][1], collision['loc'][0]], 'timestep': collision['timestep']})
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
            constraints.append({'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']})
        else:
            constraints.append({'agent': collision['a2'], 'loc': collision['loc'], 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a2'], 'loc': collision['loc'], 'timestep': collision['timestep']})
    else:
        if random.randint(0, 1) >= 0.5:
            constraints.append({'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']})
        else:
            constraints.append({'agent': collision['a2'], 'loc': [collision['loc'][1], collision['loc'][0]], 'timestep': collision['timestep'], 'positive': True})
            constraints.append({'agent': collision['a2'], 'loc': [collision['loc'][1], collision['loc'][0]], 'timestep': collision['timestep']})
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
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        #print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        #print("Expand node {}".format(id))
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
        self.push_node(root)

        # Task 3.1: Testing
        print(root['collisions'])

        # Task 3.2: Testing
        for collision in root['collisions']:
            print(standard_splitting(collision))

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit

        #starting with root
        # get next node
        # if collisions == None, return node['path']
        # generate new constraints from one of parent node's collisions
        # for each constraint => new node
        #       create new constraint list from parent node with new constraint
        #       generate new path solution using astar agent
        #       if paths none, go on to next child node
        #       detect collisions of new path solution
        #       get_sum_of_cost
        #       add new node to open list

        while len(self.open_list) > 0:
            currNode = self.pop_node()
            #print(currNode, '\n')
            if len(currNode['collisions']) == 0:
                self.print_results(currNode)
                return currNode['paths']
            #newConstraints = standard_splitting(currNode['collisions'][0])
            newConstraints = disjoint_splitting(currNode['collisions'][0])
            for con in newConstraints:
                #setting up inherited constraints and paths
                childCons = []
                for parentCon in currNode['constraints']:
                    childCons.append(parentCon)
                childCons.append(con)
                childPaths = []
                for parentPath in currNode['paths']:
                    childPaths.append(parentPath)

                #computing new paths and collisions
                if 'positive' in con: #positive constraint
                    #detect other colliding agents
                    collidingAgents = paths_violate_constraint(childPaths, con)
                    #replan other agent paths
                    missingPath = 0
                    for agent in collidingAgents:
                        #add new negative constraints
                        if len(con['loc']) == 1:
                            childCons.append({'agent': agent, 'loc': con['loc'], 'timestep': con['timestep']})
                        else:
                            childCons.append({'agent': agent, 'loc': [con['loc'][1], con['loc'][0]], 'timestep': con['timestep']})
                        newPath = a_star(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent], agent, childCons)
                        if newPath == None:
                            missingPath = 1
                            break
                        childPaths[agent] = newPath
                    if missingPath == 0:
                        childNode = {'cost': get_sum_of_cost(childPaths),
                                    'constraints': childCons,
                                    'paths': childPaths,
                                    'collisions': detect_collisions(childPaths)}
                        self.push_node(childNode)

                else :#negative constraint
                    agent = con['agent']
                    newPath = a_star(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent], agent, childCons)
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
