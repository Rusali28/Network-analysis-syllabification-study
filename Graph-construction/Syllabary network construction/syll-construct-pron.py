import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import networkx as nx
from itertools import combinations

#%matplotlib inline

#Load specific language data
spanishdata = pd.read_csv("./Data/syll_spanish_full_pron.txt", sep=" ", error_bad_lines = False)


#Clean, analyse and restructure data into a dataframe
spanishdata = spanishdata.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4'], axis = 1)

##Line of code below changes with respect to the language
spanishdata = spanishdata.rename(columns={'A1b1A1k1O':'words', 'A$b1A$k1O':'syllables'})


#Final dataframe has two columns - words, syllables
spanishspel = spanishdata[['words','syllables']].copy()

spanishspel.describe()

#Check for null entries in the dataset
sns.heatmap(spanishspel.isnull(), yticklabels = False, cbar = False, cmap = 'viridis')


#Extract words list from dataframe
words = list(spanishdata['words'])


#Remove special characters from words list - finalwords will store cleaned, original words
finalwords = []
for i in range(len(words)):
  newword = ""
  for j in words[i]:
    if j!='1':
      newword=newword+j
      #print(newword)
  finalwords.append(newword)


#Extract syllables list from dataframe 
syll = list(spanishdata['syllables'])


#Remove special characters from syll list - finalsyll will store individual lists of all syllables for every word
dictspell = {}
finalsyll = []
for i in range(len(syll)):
  finalsyll = []
  newsyll = ""
  for j in syll[i]:
    if(j!='1'):
      if(j=='$'):
        finalsyll.append(newsyll)
        newsyll = ""
      else:
        newsyll = newsyll+j
  finalsyll.append(newsyll)
  dictspell[finalwords[i]] = finalsyll
    

#Final dictionary named dictspell is created - each word is the key, corresponding value is list of syllables for the particular word
#print(dictspell)

wordlist = list(dictspell.keys())


#Extracting all unique syllables from dictspell values and storing them in a set

syllset = set()
for i in dictspell.values():
  for j in i:
    syllset.add(j)
    
    
#Generating graph - unweighted, and adding the syllables as nodes from syllset
syllgraph_spanish_unwgt = nx.Graph()

# for i in syllset:
#   syllgraph_spanish_unwgt.add_node(i)



#Generating graph - unweighted, adding edges using common syllables

for i in dictspell.values():
  l = list(combinations(i,2))
  for j,k in l:
    syllgraph_spanish_unwgt.add_edge(j,k)
    print("Edge add between ",j," and ", k)
 
            
print(syllgraph_spanish_unwgt, len(syllgraph_spanish_unwgt.nodes), len(syllgraph_spanish_unwgt.edges))


#Storing entire graph in pickle file
import pickle

with open('syllgraph_spanish_unwgt_pron.pkl','wb') as file:
    pickle.dump(syllgraph_spanish_unwgt, file)

print("DONE___________")