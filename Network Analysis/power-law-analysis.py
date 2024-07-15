
import matplotlib.pyplot as plt
import numpy as np
import powerlaw

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

degrees = [val for (node, val) in graph.degree()]

dic = {}

for i in degrees:
    x = degrees.count(i)
    dic[i] = x


log_degrees = [np.log10(degree) for degree in dic.keys()]
log_frequencies = [np.log10(frequency) for frequency in dic.values()] 


plt.figure(figsize=(10,10))
plt.scatter(log_degrees, log_frequencies, color='blue', s=10)
plt.xlabel('Log Degree')
plt.ylabel('Log Frequency')
plt.title('Degree Distribution (Log-Log Scale)')
plt.grid(True)
plt.show()
plt.savefig('./Graph images/Spel graph images/eng_wordgraph_loglog.eps', bbox_inches='tight', format='eps')



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



x = pd.Series(degrees)
f = x.plot.hist(bins=28)
#f.figure.savefig('./Graph images/Spel graph images/german_spel_hist.png', bbox_inches='tight')
plt.xlabel("Spanish degree")
plt.ylabel("Num of Nodes")
plt.savefig('./Graph images/Spel graph images/spanish_wordgraph_histogram.eps', bbox_inches='tight', format='eps')
#plt.xscale('log')
plt.show()



fig, ax = plt.subplots(figsize=(6, 6))
#fig2 = results.plot_ccdf(linewidth = 2, color= 'b',linestyle='--',label='Empirical data') #observed

fig2 = powerlaw.plot_ccdf(degrees, color='b', marker='o', linestyle='None', label='Data', linewidth=1)

#ax.tick_params(axis='x', labelsize=50)
fig2.tick_params(axis='both', which='major', labelsize=20)
fig2.tick_params(axis='both', which='minor', labelsize=20)


results.power_law.plot_ccdf( ax = fig2, color= 'g', label='Power law distribution') #expected
results.lognormal.plot_ccdf( ax = fig2, color= 'r', label = 'Lognormal distribution') 
results.exponential.plot_ccdf( ax = fig2, color= 'c', label = 'Exponential distribution') 

fig2.set_ylabel(r"$p(Degree\geq x)$", fontsize = 20)
fig2.set_xlabel(r"Degree", fontsize = 20)
handles, labels = fig2.get_legend_handles_labels()
#fig2.set_xticks([3000, 4000, 5000, 6000, 7000])

fig2.legend(handles, labels, loc=3, fontsize=8)

fig2.figure.savefig('./Graph images/Spel graph images/french_wordgraph_model.eps', bbox_inches='tight', format='eps')


plt.figure(figsize=(10,8))
results.plot_ccdf(color='r', linestyle='--', label='Power-law fit')
powerlaw.plot_ccdf(degrees, color='b', marker='o', linestyle='None', label='Data', linewidth=1)

plt.legend()
plt.xlabel('Degree (log scale)')
plt.ylabel('Complementary Cumulative Distribution Function (log scale)')
plt.show()


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))

# Plot on the first axis (ax1)
results.plot_ccdf(ax=ax1, color='r', linestyle='--', label='Power-law fit')
powerlaw.plot_ccdf(degrees, color='b', marker='o', linestyle='None', label='Data', linewidth=1)

# Plot on the second axis (ax2)
results.power_law.plot_ccdf(ax=ax2, color='g', label='Power law distribution')

# Add labels, legends, etc. for both axes

plt.show()

p = plt.figure(figsize=(7,5))
plt.xlabel("English Degree")
plt.ylabel("Perc. of nodes")
plt.plot(m,n, lw = 0.55)
plt.scatter(m,n, s = 1.15)



m = list(sorted(dic.keys()))
n = list(dic.values())

p = plt.figure(figsize=(7,5))
plt.xlabel("Spanish Degree")
plt.ylabel("Perc. of nodes")
plt.plot(m,n, lw = 0.55)
plt.scatter(m,n, s = 1.15)

p.savefig('./Graph images/Spel graph images/spanish_spel_%degree.eps',bbox_inches='tight', format='eps' )


