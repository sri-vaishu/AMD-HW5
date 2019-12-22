import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import time
import datetime
import folium
from folium.map import *
from folium import plugins
from folium.plugins import MeasureControl
from folium.plugins import FloatImage
from itertools import permutations 




def Func_4_time(source,list_n):
    final_path = [source]   # the final path start in the source
    for i in range(len(list_n)): # 
        if(i == 0):        
            initial = source
        else:
            initial = list_n[i-1]
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        while current_node != list_n[i]:
            visited.add(current_node)
            destinations = {}
            l = list(G[current_node])
            for j in l:
                destinations[j] = G[current_node][j]['time']
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = destinations[next_node] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        final_path = final_path + path[1:]
        
    
    return final_path,list_n


def Func_4_dist(source,list_n):
    final_path = [source]   # the final path start in the source
    for i in range(len(list_n)): # 
        if(i == 0):        
            initial = source
        else:
            initial = list_n[i-1]
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        while current_node != list_n[i]:
            visited.add(current_node)
            destinations = {}
            l = list(G[current_node])
            for j in l:
                destinations[j] = G[current_node][j]['dist']
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = destinations[next_node] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        final_path = final_path + path[1:]
        
    
    return final_path,list_n

def Func_4_nn(source,list_n):
    final_path = [source]   # the final path start in the source
    for i in range(len(list_n)): # 
        if(i == 0):        
            initial = source
        else:
            initial = list_n[i-1]
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        while current_node != list_n[i]:
            visited.add(current_node)
            destinations = {}
            l = list(G[current_node])
            for j in l:
                destinations[j] = 1
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = destinations[next_node] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        final_path = final_path + path[1:]
        
    
    return final_path,list_n    


    def Function_4(source,l):
    l = per(l)
    mi = 10000000
    path = l[0]
    for g in l:
        r = Func_4_time_dist(source,g)
        f1 = r[0]
        f2 = r[1]
        if(mi > Conta_peso(r)):
            mi = Conta_peso(r)
            path = r[0]
    

    cord =  (G.node[f1[0]]['latitude'],G.node[f1[0]]['longitude'])
    m = folium.Map(location=cord, zoom_start=11,tiles='Stamen Terrain')
    cluster = folium.plugins.MarkerCluster(name="Previous Crimes").add_to(m)
    for loc in f1:
        long = G.node[loc]['longitude']
        lat = G.node[loc]['latitude']
        loc_cord = [lat,long]
        if loc in f2:
            folium.CircleMarker(location=loc_cord, radius=15,
                    popup='<b>Location: </b>%s'%(loc_cord), line_color='#316cc', color = 'orange',
                    fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)
        else:
            folium.Marker(location=loc_cord, radius=5,
                    popup='<b>Location: </b>%s'%(loc_cord), line_color='#3186cc',
                    fill_color='#000001',fill_opacity=0.7, fill=True).add_to(m)
    return m,f1

    def per(l):
    l1 = []
    final = l[-1]
    perm = permutations(l[:-1])
    for i in perm:
        i = list(i)
        i.append(final)
        l1.append(i)
    return l1