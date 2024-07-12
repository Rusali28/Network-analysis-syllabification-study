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

#Final dataframe has two columns - words, syllables
engdata = pd.read_csv("./syll_english_full_spel.txt", sep=" ",error_bad_lines=False)
engdata = engdata.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4'], axis = 1)
engdata = engdata.rename(columns={'a':'words', 'a.1':'syllables'})
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

#Lexical network is constructed for all words 
aoagraph = nx.Graph()

for i in range(len(comlist)):
    aoagraph.add_node(comlist[i], weight = aoadict[comlist[i]])
    
from itertools import combinations
newtry = list(combinations(comlist,2))

#For every two pair of words, we compare the list of syllables to obtain the number of common syllables between each pair of words, and the number is then added to the edge of the network as the weight of the edge
for i,j in newtry:
    count = 0
    list1 = list(dictspell[i])[:]
    list2 = list(dictspell[j])[:]
    for k in list1:
        for m in list2:
            if(k==m):
                count+=1
                i1 = list1.index(k)
                i2 = list2.index(m)
                rand = random.sample(range(1,8000),2)
                list1[i1] = str(rand[0])
                list2[i2] = str(rand[1])
                break
    if(count!=0):
        aoagraph.add_edge(i,j,weight=count)
        print("Edge added between ",i," and ", j, " ----weight: ", count)
    
    
print(aoagraph, len(aoagraph.nodes), len(aoagraph.edges))

import pickle

with open('aoagraph_spel_wgt.pkl','wb') as file:
    pickle.dump(aoagraph, file)

print("DONEEEEEEEE___________")
    