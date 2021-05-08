# Synapse_Mindmap_Generator

![image](https://user-images.githubusercontent.com/35270359/117545901-c6ace500-aff5-11eb-9f20-c9f480847e38.png)

## Link to Video
https://www.youtube.com/watch?v=Y1MUSc4ADNw&t=120s

## Project Inspiration
Our inspiration comes from the ongoing coronavirus and its resulting remote learning and working environment. On zoom, we feel harder to focus, especially when we have to multitask active thinking and note-taking. So we want to address the challenge by having an algorithm taking the notes for us, while we can focus more on understanding the content and speaking our thoughts out. We use various natural language processing techniques to solve the problem. The main challenge is the absence of data and related-projects, so we cannot just have a machine learning model take care of everything. We start by researching on more traditional NLP techniques, and list several potential methods. The logic and relationship extraction is a very challenging part in our project. We tried to use algorithms for knowledge graph extraction, but they frequently miss important information and are not good at handle speech text. Eventually, we use a combination of word2vec-based similarity measures, NLTK wordnet synonyms detection, point-of-speech tagging and word frequency analysis to reach a good performance. We also integrate the NLP pipeline with IBM speech-to-text API and a frontend to process streaming audio and output mind maps.

## Built With
CSS, HTML, IBM, IBM-cloud, JavaScript, Python


## To clean and remove duplicated sentences:

###install spaCy
`pip install spacy`

`python -m spacy download en_core_web_sm`


###call functoion:
`sentence_preprocessing(paragraph)`

input:
`paragraph`: string

`no_rep_sentence_list`: a list of spacy sentences (with stop words, w/o dup sentences/dup words)
