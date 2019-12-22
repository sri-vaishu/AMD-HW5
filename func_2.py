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
    
