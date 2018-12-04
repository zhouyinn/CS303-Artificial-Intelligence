import copy
import time
import math
import random
import argparse
from collections import defaultdict

seed_set = []

class Graph:
    def __init__(self, vertices, edges, edge_weight, adj_list, neighbor):
        self.vertices = vertices
        self.edges = edges
        self.edge_weight = edge_weight
        self.adj_list = adj_list
        self.neighbor = neighbor


def read_seed_set(file_name):
    global seed_set
    with open(file_name) as fp:
        for line in fp:
            seed_set.append(int(line))


def read_social_network_graph(file_name):
    edge_weight, adj_list, neighbor = [[], [], []]
    vertices, edges = [0, 0]

    with open(file_name) as fp:
        for i, line in enumerate(fp):

            line = line.split(" ")
            for e in range(len(line)):
                if e == 2:
                    line[e] = float(line[e])
                else:
                    line[e] = int(line[e])
            
            if i == 0:
                vertices, edges = line
                adj_list = [list() for i in range(vertices)]
                neighbor = [list() for i in range(vertices)]
                edge_weight = [defaultdict() for i in range(vertices)]
            else:
                u,v,w = line
                adj_list[u].append(v)
                neighbor[v].append(u)
                edge_weight[u][v] = w

    return Graph(vertices, edges, edge_weight, adj_list, neighbor)
    

def LT_model(graph: Graph, time_budget):
    curtime = time.time()

    N = 0
    sum = 0
    last_time = 0
    while True:
        star_time = time.time()

        activity_set = copy.deepcopy(seed_set)
        thresholds = [0 for i in range(graph.vertices)]
        isActive = [False for i in range(graph.vertices)]

        # initialize threshold
        for i in range(len(thresholds)):

            rand_num = random.random()
            thresholds[i] = rand_num
            if rand_num == 0:
                activity_set.append(i)

        count = len(activity_set)   

        # initialize isActive      
        for e in activity_set:
            isActive[e] = True
                

        while activity_set:
            new_activity_set = []
            for seed in activity_set:
                for u in graph.adj_list[seed]:
                    if isActive[u] is False:
                        w_total = 0
                        for n in graph.neighbor[u]:
                            if isActive[n] is True:
                                w_total += graph.edge_weight[n][u]
                        if w_total >= thresholds[u]:
                            isActive[u] = True
                            new_activity_set.append(u)
            count += len(new_activity_set)
            activity_set = copy.deepcopy(new_activity_set)
        # print(count)
        N += 1
        sum += count

        last_time = time.time() - star_time
        if last_time + time.time() - curtime > time_budget - 1:
            break  
    print('N: '+str(N))
    return sum / N
    

def IC_model(graph: Graph, time_budget):
    curtime = time.time()

    N = 0
    sum = 0
    last_time = 0
    while True:
        star_time = time.time()

        activity_set = copy.deepcopy(seed_set)
        isActive = [False for i in range(graph.vertices)]

        # initialize isActive      
        for e in activity_set:
            isActive[e] = True
    
        count = len(activity_set)

        while activity_set:
            new_activity_set = []
            for seed in activity_set:
                for u in graph.adj_list[seed]:
                    if isActive[u] is False:
                        rand_num = random.random()
                        if rand_num <= graph.edge_weight[seed][u]:
                            isActive[u] = True
                            new_activity_set.append(u)
            count += len(new_activity_set)
            activity_set = copy.deepcopy(new_activity_set)
        
        N += 1
        sum += count
        last_time = time.time() - star_time
        if last_time + time.time() - curtime > time_budget - 1:
            break  
    print('N: '+str(N))
    return sum / N
        


if __name__ == "__main__":
    curtime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='social_network' ,help='the absolute path of the social network file')
    parser.add_argument('-s', dest='seed_set', help='the absolute path of the seed set file')
    parser.add_argument('-m', dest='diffusion_model', help='only be IC or LT')
    parser.add_argument('-t', dest='time_budget', type=int, help='the seconds that my algorithm can spend on this instance')
    parse_res = parser.parse_args()
    
    read_seed_set(parse_res.seed_set)
    graph = read_social_network_graph(parse_res.social_network)
    if parse_res.diffusion_model == 'IC':
        print(str(IC_model(graph, parse_res.time_budget - (time.time() - curtime))))
    elif parse_res.diffusion_model == 'LT':
        print(str(LT_model(graph, parse_res.time_budget - (time.time() - curtime))))
    
    print(str(time.time() - curtime))
    
    
    