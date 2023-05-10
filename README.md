# Reddit_Music_Discourse

This repository contains the dataset and code files regarding the music sharing patterns with context to depression on Reddit. 

The data directory contains the following files 

`data/songs.tsv` : this file contains the songs used for analysis. For each song, we have the link to the corresponding spotify track and the link to the reddit post where the song was mentioned 

`data/themes_index.tsv` : this file contains the list of manually identified themes and the file numbers of the file which contain the sentences which were identified for that particular theme. 

The directory `data/Sentence_per_theme` contains all the text file, each representing a cluster identified by the topic modelling pipeline and the corresponding sentences belonging to that cluster. 

The code directory contains code snippets used for topic modelling and extracting spotify features. 




