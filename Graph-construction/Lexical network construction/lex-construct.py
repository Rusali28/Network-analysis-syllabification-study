import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import networkx as nx

#%matplotlib inline

#Load specific language data
dutchdata = pd.read_csv("/users/grad/rsaha/Rusali/Data/syll_dutch_full_spel.txt", sep=" ",error_bad_lines=False)


#Clean, analyse and restructure data into a dataframe
dutchdata = dutchdata.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4'], axis = 1)

##Line of code below changes with respect to the language
dutchdata = dutchdata.rename(columns={'F*t*r*e':'words', 'F$t*r*e':'syllables'})


#Final dataframe has two columns - words, syllables
dutchspel = dutchdata[['words','syllables']].copy()


#Extract words list from dataframe
words = list(dutchdata['words'])


#Remove special characters from words list - finalwords will store cleaned, original words
finalwords = []
for i in range(len(words)):
  newword = ""
  for j in words[i]:
    if j!='*':
      newword=newword+j
      #print(newword)
  finalwords.append(newword)


#Extract syllables list from dataframe 
syll = list(dutchdata['syllables'])


#Remove special characters from syll list - finalsyll will store individual lists of all syllables for every word
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
    

#Final dictionary named dictspell is created - each word is the key, corresponding value is list of syllables for the particular word
print(dictspell)

wordlist = list(dictspell.keys())


#Generating graph - unweighted, and adding the words as nodes
dutchgraph = nx.Graph()

for i in range(len(wordlist)):
  dutchgraph.add_node(wordlist[i])

syllist = list(dictspell.values())



#Generating graph - unweighted, adding edges using common syllables
dflst = []
for i in dictspell:
    for j in dictspell:
        
        if(i==j):
            continue
        l = set(dictspell[i])
        m = set(dictspell[j])
        edges = l.intersection(m)
        if(len(edges)!=0):
            dutchgraph.add_edge(i,j)
            print("Match between ",i," and ",j," -- ", len(edges), "\n")
            
print(dutchgraph, len(dutchgraph.nodes), len(dutchgraph.edges))


#Storing entire graph in pickle file
import pickle

with open('dutchgraph_unwgt.pkl','wb') as file:
    pickle.dump(dutchgraph, file)

print("DONEEEEEEEE___________")
