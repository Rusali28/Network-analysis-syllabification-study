##AVERAGE CONNECTIVITY

def avg_con_k(filename):
    
    graph = readinggraphs(filename)
    
    num_nodes = len(graph.nodes)
    num_edges = len(graph.edges)
    
    k = (2*num_edges)/num_nodes
    print(k)
    
    return k



##FINDING ALL COMPONENTS OF GRAPH - LARGEST, ISLANDS, HERMITS

def find_all_comps(filename):
    graph = readinggraphs(filename)
    
    l = [graph.subgraph(c) for c in nx.connected_components(graph)]
    
    largest_congraph = l[0] #largest connected component of the graph
    
    ##to find which nodes are present in largest connected component of the graph, use below line of code
    ##largest_set = max(nx.connected_components(eng_unwgt_spel))
    
    #Below for loop is to find number of islands and hermits in the node
    for i in range(len(l)):
        g = l[i]
        if(len(g.nodes) != 1):
            print(len(g.nodes))


##AVERAGE SHORTEST PATH LENGTH

def avg_shortest_path(filename, wgt=None):
    
    #weights are by default None for unweighted graphs, for calculating features for weighted graphs, add the weights list to code
    graph = readinggraphs(filename)
    
    igg = ig.Graph.from_networkx(graph) #convert networkx graph to igraph format
    
    maxnode = igg.vs.select(_degree=igg.maxdegree()) #find largest connected node with maximum degree
    
    trypath = igg.get_all_shortest_paths(maxnode[0],weights = wgt) #get all shortest paths from the maxnode to all nodes in the graph
    
    listofpaths = []            #find the length of each path from the list of paths and calculate average shortest distance
    for i in range(len(trypath)):
        pathl = len(trypath[i])-1
        listofpaths.append(pathl)
    
    total = sum(listofpaths)
    
    vseq = igg.vs
    avg = total/(len(vseq)*(len(vseq)-1))
    
    return avg


##AVERAGE MAXIMUM PATH LENGTH (DIAMETER)

def giant_component(graph):
    """Compute giant component.

    Returns:
        The giant component of `graph` as an `igraph.Graph`.

    """
    vc = graph.components()
    vc_sizes = vc.sizes()
    return vc.subgraph(vc_sizes.index(max(vc_sizes)))


def diameter(filename, wgt=None):
    
    #weights are by default None for unweighted graphs, for calculating features for weighted graphs, add the weights list to code
    graph = readinggraphs(filename)
    
    igg = ig.Graph.from_networkx(graph) #convert networkx graph to igraph format
    
    large_cc = giant_component(igg) #find largest connected component in the graph
    
    ds = large_cc.diameter(directed=False,unconn=False) #calculate diameter for largest connected subgraph

    return ds


##Clustering coefficient

def find_wgtlist(filename):
    
    graph = readinggraphs(filename)
    
    ledge = list(graph.edges)
    
    weightlist = []
    for i in range(len(ledge)):
        x = graph.get_edge_data(ledge[i][0],ledge[i][1])
        w = x['weight']
        weightlist.append(w)

    return weightlist

def clustercoeff(filename):
    
    graph = readinggraphs(filename)
    
    cwgt = find_wgtlist(filename)
    
    igg = ig.Graph.from_networkx(g)

    cc = igg.transitivity_avglocal_undirected(mode = 'zero',weights = cwgt)
    
    return cc


##Avg path length

def avg_path(filename):
    
    graph = readinggraphs(filename)
    
    igg = ig.Graph.from_networkx(graph) #convert networkx graph to igraph format
    
    dist = igg.average_path_length(directed=False,unconn=False)

    return dist
    
    

##Estimating alpha paramter for power law

def power_law(filename):
    
    graph = readinggraphs(filename)
    
    degrees = [val for (node, val) in graph.degree()] ##we pass the a list of degrees of all nodes 
    
    import powerlaw

    results = powerlaw.Fit(degrees)
    
    print(results.power_law.alpha)
    
    print(results.power_law.xmin)
    
    R, p = results.distribution_compare('power_law', 'lognormal')
    print(R,p)
    
    return results

