# Synapse_Mindmap_generator

To clean and remove duplicated sentences:

###install spaCy
`pip install spacy`

`python -m spacy download en_core_web_sm`


###call functoion:
`sentence_preprocessing(paragraph)`

input:
`paragraph`: string

`no_rep_sentence_list`: a list of spacy sentences (with stop words, w/o dup sentences/dup words)