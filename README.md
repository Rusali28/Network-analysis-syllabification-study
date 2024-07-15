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

## Network Analysis

A detailed network analysis consisting of all major network topology features are calculated and evaluated to study the complex and small world nature of all the networks. 