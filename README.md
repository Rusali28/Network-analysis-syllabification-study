# Network-analysis-syllabification-study
This project contains the code for the paper 'An Empirical Study of Language Syllabification using Syllabary and
Lexical networks'

Please note: Throughout the contents of the repository, lexical networks have been also referred to as "wordgraphs" and syllabary networks have been alternately referred to as "syllgraphs".

In this work, we consider two parent types of networks:
- **Syllabary networks** : The nodes represent each unique syllable of the language and an edge is generated when two syllable nodes have at least one word in common.
- **Lexical networks** : The nodes represent a word and two words are connected by an edge when they share at least one common syllable

The networks are built across four major languages:
- English
- French
- German
- Spanish

Furthermore, considering Lexical and Syllabary as the parent types, two types of child networks are constructed using datasets based on two domains of each language:

- Spelling
- Pronunciation

## Graph samples
Here is a small representation of the English lexical and syllabary networks. 


<p align="center">
  <img src="Graph%20images/Graph-example/wordgraph-eg.PNG" alt="lexgraph" style="width:50%;">
  <br>
  <b>Figure 1:</b> Example of the English lexical graph
</p>

<p align="center">
  <img src="Graph%20images/Graph-example/syllgraph-eg.PNG" alt="syllgraph" style="width:50%;">
  <br>
  <b>Figure 2:</b> Example of the English syllabary graph
</p>

<!--
## Network Analysis

A detailed network analysis consisting of all major network topology features are calculated and evaluated to study elementary characteristics that define the main types of networks like random networks, small world networks and scale free networks. 

A mathematical evaluation of degree distribution of networks to observe best fit is conducted.
-->
## Dataset Format and Network Construction

Our cleaning, pre-processing and modelling of our dataset results in a dictionary where keys are the words and values are the corresponding list of syllables associated with each word.

<br>
<p align="center">
  <img src="Graph%20images/Data/dict.png" alt="dict" style="width:50%;">
  <br>
  <br>
  <b>Figure 3:</b> Example of the generated dictionary data
</p>
<br>
To generate the lexical and syllabary networks, (by default we consider spelling based data)

```bash
python lex-construct.py (for lexical networks)
```
```bash
python syll-construct.py (for syllabary networks)
```
To generate the lexical and syllabary networks based on pronunciation data,

```bash
python lex-construct-pron.py (for lexical networks)
```
```bash
python syll-construct-pron.py (for syllabary networks)
```

To generate the age of acquisition networks, we filter out words for which age of acquisition (AoA) data is available and subsequently proceed with network construction. 

For the syllabary AoA networks, all words containing a pair of syllables are considered while forming the edges. The word with the minimum age of acquisition value out of them is finally chosen and the AoA value is assigned accordingly.

For generation of AoA networks please use the following:

```bash
python aoa-lexical.py (for lexical networks)
```
```bash
python aoa-syllgraph.py (for syllabary networks)
```
