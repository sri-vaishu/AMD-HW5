import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import gzip




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
#now we get edges attributes, for each category (time,distance,network)

t_attr = nx.get_edge_attributes(G,'time')
d_attr = nx.get_edge_attributes(G,'dist')
n_attr = nx.get_edge_attributes(G,'net')

#all this variables are dict, as a key there ia a tuple (node1,node2), and the value is the weight of the edge   
        
        
        