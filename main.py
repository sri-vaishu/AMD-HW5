import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy



def create_Graph():


    coord = pd.read_csv('../USA-road-d.CAL.co', sep = ',', delimiter = " ",
                      index_col = None, usecols = None, encoding = 'ISO-8859-1')  # we read the input file
    coord.drop(columns=['c','Challenge:','Shortest','Paths'], inplace = True) # drop all the information useless
    coord.rename(columns={"c": "char","9th":"ID","DIMACS":"Longitude","Implementation":"Latitude"},inplace = True)#rename the columns
    coord.drop(coord.index[:6], inplace=True) #the first 6 columns are not information about the node
    
    G = nx.Graph() # create the graph
    # create all the node, with two attributes, latitude and longitute
    for long in coord.iterrows():
        l = list(long[1])
        idx = int(l[0])
        lat = int(l[1])
        long = -int(l[2])
        G.add_node(idx, latitude = lat, longitude = long)
    
    # now inport the time_distance file and create a dataframe
    time = pd.read_csv("../USA-road-t.CAL.gr",sep = ',',skiprows = 7, delimiter=" ",
                       names = ['char','N_1','N_2','time'])
    time.drop(columns=['char'],inplace = True)
    
    
    # now inport the physical_distance  file and create a dataframe
    dist = pd.read_csv("../USA-road-d.CAL.gr",sep = ',',skiprows = 7, delimiter=" ",
                       names = ['char','N_1','N_2','dist'])
    dist.drop(columns=['char'],inplace = True)
    final = dist.merge(time, on = ["N_1","N_2"])
    for idx in final.iterrows():
        l = list(idx[1])
        source = int(l[0])
        dest = int(l[1])
        di = int(l[2])
        ti = int(l[3])
        G.add_edge(source,dest,time = ti, dist = di)
    return G