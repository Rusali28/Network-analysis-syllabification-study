
import matplotlib.pyplot as plt
import numpy as np
import powerlaw
import pandas as pd

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

graph = readinggraphs("./Spel graphs/frenchgraph_unwgt.pkl")

#Preparing the network to collect degree distribution data
degrees = [val for (node, val) in graph.degree()]

dic = {}

for i in degrees:
    x = degrees.count(i)
    dic[i] = x


log_degrees = [np.log10(degree) for degree in dic.keys()]
log_frequencies = [np.log10(frequency) for frequency in dic.values()] 

#Based on previous works, log-log plots are constructed to visualize and make intial estimations 
plt.figure(figsize=(10,10))
plt.scatter(log_degrees, log_frequencies, color='blue', s=10)
plt.xlabel('Log Degree')
plt.ylabel('Log Frequency')
plt.title('Degree Distribution (Log-Log Scale)')
plt.grid(True)
plt.show()
plt.savefig('./Graph images/Spel graph images/eng_wordgraph_loglog.eps', bbox_inches='tight', format='eps')


#Computing parameters for power law and lognormal distribution
results = powerlaw.Fit(degrees, discrete=True)

alpha = print(results.power_law.alpha)

xmin = print(results.power_law.xmin)

R, p = results.distribution_compare('power_law', 'lognormal')

x = results.power_law.KS()

synthetic_data = results.power_law.generate_random(len(degrees)) # to perform KS test, fit to power_law with KS test

ks_statistic = results.power_law.KS(data=synthetic_data)

p_value = results.distribution_compare('power_law', 'lognormal',normalized_ratio=True)

y = results.lognormal.KS(degrees)

mu = print(results.lognormal.mu)

sigma = print(results.lognormal.sigma)


#Histogram plots of the degree distribution and node frequency are constructed for all networks and languages
x = pd.Series(degrees)
f = x.plot.hist(bins=28)
#f.figure.savefig('./Graph images/Spel graph images/german_spel_hist.png', bbox_inches='tight')
plt.xlabel("Spanish degree")
plt.ylabel("Num of Nodes")
plt.savefig('./Graph images/Spel graph images/spanish_wordgraph_histogram.eps', bbox_inches='tight', format='eps')
#plt.xscale('log')
plt.show()


#Fitting the empirical degree distribution to our three candidate distributions
fig, ax = plt.subplots(figsize=(6, 6))
fig2 = powerlaw.plot_ccdf(degrees, color='b', marker='o', linestyle='None', label='Data', linewidth=1)

fig2.tick_params(axis='both', which='major', labelsize=20)
fig2.tick_params(axis='both', which='minor', labelsize=20)

results.power_law.plot_ccdf( ax = fig2, color= 'g', label='Power law distribution') 
results.lognormal.plot_ccdf( ax = fig2, color= 'r', label = 'Lognormal distribution') 
results.exponential.plot_ccdf( ax = fig2, color= 'c', label = 'Exponential distribution') 

fig2.set_ylabel(r"$p(Degree\geq x)$", fontsize = 20)
fig2.set_xlabel(r"Degree", fontsize = 20)
handles, labels = fig2.get_legend_handles_labels()
fig2.legend(handles, labels, loc=3, fontsize=8)
fig2.figure.savefig('./Graph images/Spel graph images/french_wordgraph_model.eps', bbox_inches='tight', format='eps')


#Studying the representation of the Complementary Cumulative Distribution Function against the degree distribution of the network
plt.figure(figsize=(10,8))
results.plot_ccdf(color='r', linestyle='--', label='Power-law fit')
powerlaw.plot_ccdf(degrees, color='b', marker='o', linestyle='None', label='Data', linewidth=1)
plt.legend()
plt.xlabel('Degree (log scale)')
plt.ylabel('Complementary Cumulative Distribution Function (log scale)')
plt.show()

#The distribution of degree and node frequency is plotted to study patterns, consistency and anomalies
m = list(sorted(dic.keys()))
n = list(dic.values())

p = plt.figure(figsize=(7,5))
plt.xlabel("English Degree")
plt.ylabel("Perc. of nodes")
plt.plot(m,n, lw = 0.55)
plt.scatter(m,n, s = 1.15)

p = plt.figure(figsize=(7,5))
plt.xlabel("Spanish Degree")
plt.ylabel("Perc. of nodes")
plt.plot(m,n, lw = 0.55)
plt.scatter(m,n, s = 1.15)

p.savefig('./Graph images/Spel graph images/spanish_spel_%degree.eps',bbox_inches='tight', format='eps' )


