#This code refers to visualization attempts made at studying the networks using networkX. For final visualization, however, Cytoscape software is used.

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from random import sample
from itertools import combinations

plt.rcParams['figure.figsize'] = [20, 10]


def readinggraphs(filename):
    graph = pd.read_pickle(filename)
    print(len(graph.nodes), len(graph.edges))
    
    flag = 0
    for i,j in list(graph.edges):
        print(i," ", j," ------- ",graph.get_edge_data(i,j))
        flag+=1
        if(flag==50):
            break
    
    return graph

enggraph = readinggraphs("./Spel graphs/enggraph_wgt.pkl")

#Selecting a smaller set of nodes for better visualization

from random import sample

# nodelist = list(eng_unwgt.nodes())[:5]
nodelist = sample(list(enggraph.nodes()),15)

print(nodelist)

##Finding all combinations of nodes - this will help in extracting the edges that belong to only selected nodes

from itertools import combinations

comb = list(combinations((nodelist),2))

dummy_graph = nx.Graph()

for i in nodelist:
    dummy_graph.add_node(i)

    
## For each combination in comb list, we will check if a corresponding edge is present in our graph or not, and if yes then add
#that edge to the dummy_graph

for i in comb:
    if enggraph.get_edge_data(i[0],i[1]):
        print("yes",i[0],i[1])
        val = enggraph.get_edge_data(i[0],i[1])
        dummy_graph.add_edge(i[0],i[1], weight = val['weight'])
        
dummy_graph.edges

isolate = list(nx.isolates(dummy_graph))
isolate

for i in range(len(isolate)-3):
    dummy_graph.remove_node(isolate[i])
    
dummy_graph.nodes()
plt.rcParams['figure.figsize'] = [15, 16]
plot = nx.draw_networkx(dummy_graph, with_labels= True, node_color = '#17becf')

plot = nx.draw_circular(dummy_graph, with_labels= True, node_color = '#e377c2')

nx.write_gml(dummy_graph, "testgraph2.gml")
g = nx.read_gml('testgraph.gml')

g.nodes()
isolate = list(nx.isolates(g))

for i in range(len(isolate)-2):
    g.remove_node(isolate[i])
    
g.nodes()