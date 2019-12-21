import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy



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
    
    
    
G = nx.read_gpickle("directed_graph.gpickle.gz")
int_func = int(input("What func do you want?\n"))
getFunction(int_func)



#i = int(input("What function do you want to call?\n"))
#getFunction(i)









