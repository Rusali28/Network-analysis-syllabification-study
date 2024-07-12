import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import networkx as nx
import random

#Reading data and pre processing to clean, analyze and restructure data
data = pd.read_excel("./Dataset/AoA_51715_words.xlsx", sheet_name="Sheet1")

newdata = data[['Word','AoA_Kup_lem']].copy()

timelist = list(newdata['AoA_Kup_lem'])
len(timelist), timelist[:10]

#To obtain age of aquisition numbers in months, each AoA value is multiplied by 12
timelist = [i*12 for i in timelist]

aoawordlist = list(newdata['Word'])
aoawordlist[:10], timelist[:10]

aoadict = {}

for i in range(len(aoawordlist)):
    x = aoawordlist[i]
    aoadict[x] = timelist[i]
    
len(aoadict), aoadict

engdata = pd.read_csv("./syll_english_full_spel.txt", sep=" ",error_bad_lines=False)
engdata = engdata.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4'], axis = 1)
engdata = engdata.rename(columns={'a':'words', 'a.1':'syllables'})

#Final dataframe has two columns - words, syllables
engspel = engdata[['words','syllables']].copy()
words = list(engdata['words'])

#Remove special characters from words list - finalwords will store cleaned, original words
finalwords = []
for i in range(len(words)):
  newword = ""
  for j in words[i]:
    if j!='*':
      newword=newword+j
      #print(newword)
  finalwords.append(newword)

syll = list(engdata['syllables'])

#Remove special characters from syll list - finalsyll will store individual lists of all syllables for every word
#Final dictionary named dictspell is created - each word is the key, corresponding value is list of syllables for the particular word
dictspell = {}
finalsyll = []
for i in range(len(syll)):
  finalsyll = []
  newsyll = ""
  for j in syll[i]:
    if(j!='*'):
      if(j=='$'):
        finalsyll.append(newsyll)
        newsyll = ""
      else:
        newsyll = newsyll+j
  finalsyll.append(newsyll)
  dictspell[finalwords[i]] = finalsyll
    
    

m = list(aoadict.keys())
n = list(dictspell.keys())

#comlist is used to extract the list of words from the original created dictionary dictspell, to contain only those words for which age of acquisition data is available
comlist = []
for i in m:
    if n.count(i) != 0:
        comlist.append(i)
        
len(comlist), comlist

from itertools import combinations

#combilist is used to calculate all possible combinations of node pairs among all syllables in the dictionary
combilist = dict()
for i in comlist:
    
    if(len(dictspell[i])==1):
        continue
    l = list(set(combinations(dictspell[i],2)))
    combilist[i] = l
     

print(combilist, "COMBILIST DONE")


#storage will count the frequency of occurrence of every pair of syllables from combilist 
storage = dict()
for i in combilist:
    for j in combilist[i]:
        if j in storage:
              storage[j] += 1
        else:
              storage[j] = 1

for i in combilist:
    print(i, combilist[i])
    
print("STORAGE DONE %%%%%%%%%%%%%%%%", len(storage))

#Syllabary graph for age-of-acquisition data is constructed. The weights of each node pair, obtained from storage dictionary are assigned while constructing the graph
aoa_syllgraph = nx.Graph()

count = 0
for i in storage:
    if(len(i)==1):
        continue
    aoa_syllgraph.add_edge(i[0],i[1], weight = storage[i])
    print("Edge added btw ",i[0]," and ", i[1], " weight - ", storage[i])


print(aoa_syllgraph, len(aoa_syllgraph.nodes), len(aoa_syllgraph.edges))


nodelist = list(aoa_syllgraph.nodes())
nodelist[:10]

comdict = dict()
for i in comlist:
    comdict[i] = dictspell[i]
    
comdict['abacus'], len(comdict), len(nodelist)

newl = []
sylldict = dict()

#Sylldict is the dictionary that stores each individual syllable as key and the corresponding value pair consists of a list of all words in which the syllable has appeared 
#For example, s = sylldict['rig'] will find all the words that have the syllable 'rig' in it
for i in nodelist:
    newl = []
    for j in comdict:
        l = comdict[j]
        if l.count(i) != 0:
            print(i, 'present in list ', newl)
            newl.append(j)
    sylldict[i] = newl
    
nodewgtdict = {}

#After obtaining the dictionary of each syllable and its corresponding set of word occurrences, we iterate through each set of words for a each syllable, and compare the age of acquisition values for every word in the list. The word with the minimum age of acquisition in every list is considered finally.
for j in sylldict:
    
    s = sylldict[j]

    minv = aoadict[s[0]]

    for i in s:
        val = aoadict[i]
        #print(i,val, minv)

        if val<minv:
            minv = val
            #print(minv)
        
    #print(minv, "****************WORD DONE************** FOR",j)   
    nodewgtdict[j] = minv
    
#the minimum AoA value is now accordingly added to every node in the syllabary graph    
nx.set_node_attributes(aoa_syllgraph, values = nodewgtdict, name = 'aoaminvalue') 



#TO BUILD YEARWISE SYLLABARY GRAPHS (syllgraphs) - for each yearwise data, we construct a new network, which is built upon cumulative yearwise data starting from the first year, up till the year being considered in the particular iteration
yeargraph = {}

for i in aoadict:
    if aoadict[i] <= (15*12):
        yeargraph[i] = aoadict[i]
        
        
        
m = list(yeargraph.keys())
n = list(dictspell.keys())

comlist = []
for i in m:
    if n.count(i) != 0:
        comlist.append(i)
        
len(comlist), comlist

from itertools import combinations

combilist = dict()
for i in comlist:
    
    if(len(dictspell[i])==1):
        continue
    l = list(set(combinations(dictspell[i],2)))
    combilist[i] = l
     

print(combilist, "COMBILIST DONE")

storage = dict()
for i in combilist:
    for j in combilist[i]:
        if j in storage:
              storage[j] += 1
        else:
              storage[j] = 1

for i in combilist:
    print(i, combilist[i])
    
print("STORAGE DONE %%%%%%%%%%%%%%%%", len(storage))


year_syllgraph = nx.Graph()

count = 0
for i in storage:
    if(len(i)==1):
        continue
    year_syllgraph.add_edge(i[0],i[1], weight = storage[i])
    print("Edge added btw ",i[0]," and ", i[1], " weight - ", storage[i])


print(year_syllgraph, len(year_syllgraph.nodes), len(year_syllgraph.edges))

yrnodelist = list(year_syllgraph.nodes())
yrnodelist[:10]

newl = []
yrsylldict = dict()

for i in yrnodelist:
    newl = []
    for j in comdict:
        l = comdict[j]
        if l.count(i) != 0:
            print(i, 'present in list ', newl)
            newl.append(j)
    yrsylldict[i] = newl
    
    
yearnodewgtdict = {}

for j in yrsylldict:
    
    s = yrsylldict[j]

    minv = aoadict[s[0]]

    for i in s:
        val = aoadict[i]
        #print(i,val, minv)

        if val<minv:
            minv = val
            #print(minv)
        
    #print(minv, "****************WORD DONE************** FOR",j)   
    yearnodewgtdict[j] = minv
    
    
nx.set_node_attributes(year_syllgraph, values = yearnodewgtdict, name = 'aoaminvalue') 

import pickle

with open('./yearwise syllgraphs/15yearsyllgraph.pkl','wb') as file:
    pickle.dump(year_syllgraph, file)
    
#for reading the networks that are stored as pickle files    
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
