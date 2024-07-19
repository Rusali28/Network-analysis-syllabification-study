import pandas as pd
import networkx as nx
from langdetect import detect
import nltk
from nltk.corpus import words

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

eng_unwgt_spel = readinggraphs("./Spel graphs/enggraph_unwgt.pkl")

#finding number of hermit nodes (isolated nodes with degree 0) for inspection

nodes = eng_unwgt_spel.nodes()
hermits = [node for node in eng_unwgt_spel.nodes() if eng_unwgt_spel.degree[node] == 1]

#Sort the list for ease of understanding
hermits = sorted(hermits)

#The list of hermits is exported to text file
file_path = "hermits.txt"

with open(file_path, "w") as file:
    for item in hermits:
        file.write(item + "\n")

print("List has been saved to", file_path)

#We use two vocabulary set libraries, Langdetect and NLTK to study and analyze the pattern and origin of the hermit nodes

#Using Langdetect
eng_home = []
other_home = []
def is_english(word):
    try:
        return detect(word) == 'en'
    except:
        return False

for word in hermits:
    if is_english(word):
        eng_home.append(word)
        print(word, "is likely English.")
    else:
        other_home.append(word)
        print(word, "is likely from another language.")

len(eng_home)
len(other_home)


#Using NLTK
eng1 = []
other1 = []

nltk.download('words')

english_words = set(words.words())

for word in hermits:
    if word.lower() in english_words:
        print(word, "is likely an English word.")
        eng1.append(word)
    else:
        print(word, "is likely from another language.")
        other1.append(word)

len(eng1), len(other1)
other1 = sorted(other1)

#After average estimations from both the libraries, the set of probable non-english words are exported as lists

file_path = "nltk_non_eng.txt"

with open(file_path, "w") as file:
    for item in other1:
        file.write(item + "\n")

print("List has been saved to", file_path)

other_home = sorted(other_home)

file_path = "langdetect_python_non_eng.txt"

with open(file_path, "w") as file:
    for item in other_home:
        file.write(item + "\n")

print("List has been saved to", file_path)

nltk = set(other1)
langd = set(other_home)
print(sorted(list(langd - nltk)))         #jihad, eisteddfod, bouffant, ebb, jodhpurs

print(langd)        #bouffant, cauldron,delft,ebb (Dutch), zigzag (german), louvred (french), mahjong(chinese), lozenge (spanish, latin, portuguese)

#Here we identify the list of non-english words, and their probable origins. For example, zigzag being a hermit in our networks, is identified to have a non-english origin and it is found upon further study that has probable origins in the German language. 