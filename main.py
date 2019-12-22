import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import gzip
import folium
from folium.map import *
from folium import plugins
from folium.plugins import MeasureControl
from folium.plugins import FloatImage
from itertools import permutations 

# FUNCTION 1 AND VISUALIZATION

"""
We worked with a graph made by NXGraph library, so before using functions,
we had to set proper data structure

"""



#now we get edges attributes, for each category (time,distance,network)

t_attr = nx.get_edge_attributes(G,'time')
d_attr = nx.get_edge_attributes(G,'dist')
n_attr = nx.get_edge_attributes(G,'net')

                                   ################### FUNCTION #########################

def nodes_in_range(start, max_d, d_type):
    """
    Basic function that gets all the nodes that are within the max_d distance from the start node
    :param start: starting node
    :param max_d: maximum distance allowed
    :return: list of found nodes
    """
    return nodes_in_range_util(start, 0, max_d, max_d, [start], d_type)

def nodes_in_range_util(node, i, max_d, current_d, res,dist_type):
    """
    Recursive helper function for the nodes_in_range function

    :param node: current node
    :param i: current index
    :param max_d: maximum distance
    :param current_d: current 'walkable' distance
    :param res: nodes found
    :return: list of found nodes
    """
    # If the current index is greater than the length of adjacent vertices return the list of found nodes
    if i >= len(list(G.neighbors(node))):
        return res
    # If the current 'walkable' distance is less than 0, increment i and call recursion
    elif current_d <= 0:
        i += 1
        return nodes_in_range_util(node, i, max_d, max_d, res, dist_type)
    # Else we start finding
    
    else:
        neight = list(G.neighbors(node))
        # Get the next node
        next_node = neight[i] #we pick the node
        # Check if we didnt already marked the next node
        if next_node not in res:
            # Get the graph weight
            t1 = (node,next_node) #we try this two node order because library Nx.graph store them in arbitrary way
            t2 = (next_node,node)
            if dist_type=='time':
                try:
                    weight = t_attr[t1]
                except Exception:
                    weight = t_attr[t2]
                    
            elif dist_type=='dist':
                try:
                    weight = d_attr[t1]
                except Exception:
                    weight = d_attr[t2]
                    
            elif dist_type=='net':
                try:
                    weight = n_attr[t1]
                except Exception:
                    weight = n_attr[t2]
            
            # Check if the weight is 'walkable'
            if weight < current_d:
                # Append the node
                res.append(next_node)
                print(res)
                # Call recursion starting from the current node
                i += 1
                return nodes_in_range_util(node, i, max_d, current_d,
                                                nodes_in_range_util(next_node, 0, max_d, current_d - weight, res, dist_type), dist_type)
            else:
                # Call recursion going to the next node
                i += 1
                return nodes_in_range_util(node, i, max_d, current_d, res, dist_type)
        # Increment i if the already marked the next node and proceed
        else:
            i += 1
            return nodes_in_range_util(node, i, max_d, current_d, res, dist_type)


                                            ################# VISUALIZATION #########################
res  = nodes_in_range_util(node, i, max_d, current_d, res,dist_type)

lat =dict(nx.get_node_attributes(G, 'latitude')) #dictionary with all nodes  and their latitude
long = dict(nx.get_node_attributes(G, 'longitude'))

def map(start,res):
    centre = [-long[start]/1000000 , lat[start]/1000000] #centre node
    coord_list = []
    for el in res:
        coord = [-long[el]/1000000,lat[el]/1000000]
        coord_list.append(coord)

    #creating the map

    m = folium.Map(location = centre, zoom_start = 15)

    for coord in coord_list:
        if coord != centre:
            folium.Marker(location = coord, icon=folium.Icon(color = 'red')).add_to(m)

    return m

#FUNCTION 2 AND VISUALIZATION

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import gzip
import folium
from folium.map import *
from folium import plugins
from folium.plugins import MeasureControl
from folium.plugins import FloatImage
from itertools import permutations

"""
We worked with a graph made by NXGraph library, so before using functions,
we had to set proper data structure

"""

#now we get edges attributes, for each category (time,distance,network)

t_attr = nx.get_edge_attributes(G,'time')
d_attr = nx.get_edge_attributes(G,'dist')
n_attr = nx.get_edge_attributes(G,'net')

################### FUNCTION #########################

def min_path(nodes,d_type):
    
    res = [] #list with the result path
    
    s_nodes = sorted(nodes)
    track = []  #track of nodes that are part of the mst
    d = {}
    #we create a dict with every node and their value set as inf, except for the first node(the one that inizialize)
    for node in nodes:
        if node == nodes[0]:
            d [node] = 0
        else:
            d[node] = float("inf") #value is inf
    print(len(d))
            
    if d_type == 'dist':

        #we terminate when in 'track' list we'll have all nodes in input
        #while sorted(track) != s_nodes:
        while len(d) != 0:
            
            m = min(d, key=d.get) #we alway use a node that has not been analized before

            neighbors  = list(G.neighbors(m))
            dist_dict = {}
            for neight_node in neighbors: #we pick all neighbors nodes

                t1 = (m,neight_node) #key1 to get the weight of the edge in attributes dict
                t2 = (neight_node,m) #key2 to get the weight of the edge in attributes dict
                try:
                    weight = d_attr[t1]
                except Exception:
                    weight = d_attr[t2]
                    
                if neight_node not in track: #we check that every neighbors is not yet in tracked nodes
                    dist_dict[neight_node] = weight #we store the weight of all edges from the node we are examining

                #we chekc if we have to upload the value of the node in 'd':
                if neight_node in d.keys():  #just for neighbors node that we have to analyze
                    if d[neight_node ]> weight:
                        d[neight_node ] = weight

            closest = min(dist_dict, key=dist_dict.get) #we get the node with minimum edge
            result = [m,closest]
            result = sorted(result)
            if result not in res:  #we avoid repetition of same edged
                res.append(result) 
            d.pop(m)
                

        return res
    
    if d_type == 'time':

        #we terminate when in 'track' list we'll have all nodes in input
        #while sorted(track) != s_nodes:
        while len(d) != 0:
            m = min(d, key=d.get) #we alway use a node that has not been analized before

            neighbors  = list(G.neighbors(m))
            dist_dict = {}
            for neight_node in neighbors: #we pick all neighbors nodes

                t1 = (m,neight_node) #key1 to get the weight of the edge in attributes dict
                t2 = (neight_node,m) #key2 to get the weight of the edge in attributes dict
                try:
                    weight = t_attr[t1]
                except Exception:
                    weight = t_attr[t2]
                    
                if neight_node not in track: #we check that every neighbors is not yet in tracked nodes
                    dist_dict[neight_node] = weight #we store the weight of all edges from the node we are examining

                #we chekc if we have to upload the value of the node in 'd':
                if neight_node in d.keys():
                    if d[neight_node ]> weight:
                        d[neight_node ] = weight

            closest = min(dist_dict, key=dist_dict.get)
            track.append(closest)
            result = [m,closest]
            result = sorted(result)
            if result not in res:
                res.append(result)
            
            d.pop(m)
                

        return res

    if d_type == 'net':

        #we terminate when in 'track' list we'll have all nodes in input
        #while sorted(track) != s_nodes:
        while len(d) != 0:
            m = min(d, key=d.get) #we alway use a node that has not been analized before

            neighbors  = list(G.neighbors(m))
            dist_dict = {}
            for neight_node in neighbors: #we pick all neighbors nodes

                t1 = (m,neight_node) #key1 to get the weight of the edge in attributes dict
                t2 = (neight_node,m) #key2 to get the weight of the edge in attributes dict
                try:
                    weight = t_attr[t1]
                except Exception:
                    weight = t_attr[t2]
                    
                if neight_node not in track: #we check that every neighbors is not yet in tracked nodes
                    dist_dict[neight_node] = weight #we store the weight of all edges from the node we are examining

                #we chekc if we have to upload the value of the node in 'd':
                if neight_node in d.keys():
                    if d[neight_node ]> weight:
                        d[neight_node ] = weight

            closest = min(dist_dict, key=dist_dict.get)
            track.append(closest)
            result = [m,closest]
            result = sorted(result)
            if result not in res:
                res.append(result)
            
            d.pop(m)
                

        return res

######################### VISUALIZATION ########################à

result = min_path(nodes,d_type)

lat =dict(nx.get_node_attributes(G, 'latitude')) #dictionary with all nodes  and their latitude
long = dict(nx.get_node_attributes(G, 'longitude'))

def map(result):
    nodes = []
    for path in result:
        for n in path:
            nodes.append(n)

    coord_list = []
    for el in nodes:
        coord = [-long[el]/1000000,lat[el]/1000000]
        coord_list.append(coord)

    #creating the map

    m = folium.Map(location = centre, zoom_start = 15)

    for coord in coord_list:
        if coord != centre:
            folium.Marker(location = coord, icon=folium.Icon(color = 'red')).add_to(m)

    folium.PolyLine(nodes, color="red", weight=2.5, opacity=1).add_to(m)

    return m


#########

def create_Graph():
    coord = pd.read_csv('../USA-road-d.CAL.co', sep = ',', delimiter = " ",
                          index_col = None, usecols = None, encoding = 'ISO-8859-1')  # we read the input file
    coord.drop(columns=['c','Challenge:','Shortest','Paths'], inplace = True) # drop all the information useless
    coord.rename(columns={"c": "char","9th":"ID","DIMACS":"Longitude","Implementation":"Latitude"},inplace = True) 
    #rename the columns
    coord.drop(coord.index[:6], inplace=True) #the first 6 columns are not information about the node
    G = nx.DiGraph()
    # create all the node, with two attributes, latitude and longitute
    for long in coord.iterrows():
        l = list(long[1])
        idx = int(l[0])
        lat = int(l[1])/1000000
        long = int(l[2])/1000000
        G.add_node(idx, latitude = long, longitude = lat)
    # now inport the time_distance file and create a dataframe
    time = pd.read_csv("../USA-road-t.CAL.gr",sep = ',',skiprows = 7, delimiter=" ",names = ['char','N_1','N_2','time'])
    time.drop(columns=['char'],inplace = True)
    # now inport the physical_distance  file and create a dataframe
    dist = pd.read_csv("../USA-road-d.CAL.gr",sep = ',',skiprows = 7, delimiter=" ",names = ['char','N_1','N_2','dist'])
    dist.drop(columns=['char'],inplace = True)
    final = dist.merge(time, on = ["N_1","N_2"])
    l = [1 for n in range(4712818)]
    final['netkork']=l
    for idx in final.iterrows():
        l = list(idx[1])
        source = int(l[0])
        dest = int(l[1])
        di = int(l[2])
        ti = int(l[3])
        ni = int(l[4])

        G.add_edge(source,dest,time = ti, dist = di, net=ni)
    return G





def Function(i):
    if i == 1:
        print("functionality 1 called\n")
        Function_1()
    elif i == 2:
        print("Functionality 2 called\n")
        Function_2()
    elif i == 3:
        print("Functionality 3 called\n")
        Function_3()
    elif i ==4:
        print("Functionality 4 called\n")
        Function_4()

def Function_1():
    node_id = int(input("Insert the start node\n"))
    dist_funct = int(input("Insert 1 for the distance function, 2 for the time distance function or 3 for the network distance\n"))
    threshold = int(input("Insert the distance threshold\n"))
    if dist_funct == 1:
        param = 'dist'
    elif dist_funct == 2:
        praram = 'time'
    else:
        param = 'net'
    return func_1.nodes_in_range(G,node_id,threshold,param)

def Function_2():
    print("soon..")

def Function_3():
    node_id = int(input("Insert the start node\n"))
    nodes = list(map(int, input("Insert a list of node (comma separeted) in this way: 'ex. 25,346,456'\n").split(",")))
    dist_funct = int(input("Insert 1 for the distance function, 2 for the time distance function or 3 for the network distance\n"))
    if dist_funct == 1:
        param = 'dist'
    elif dist_funct == 2:
        praram = 'time'
    else:
        param = 'net'
    f3.routes(G, node_id, nodes, param)


def Function_4():
    node_id = int(input("Insert the start node\n"))
    nodes = list(map(int, input("Insert a list of node (comma separeted) in this way: 'ex. 25,346,456'\n").split(",")))
    dist_funct = int(input("Insert 1 for the distance function, 2 for the time distance function or 3 for the network distance\n"))
        if dist_funct == 1:
        param = 'dist'
    elif dist_funct == 2:
        praram = 'time'
    else:
        param = 'net'
    f4.routes(G, node_id, nodes, param)
    
    
    
G = nx.read_gpickle("Final_graph.gpickle.gz")
int_func = int(input("What func do you want to run?\n"))
getFunction(int_func)



#i = int(input("What function do you want to call?\n"))
#getFunction(i)









