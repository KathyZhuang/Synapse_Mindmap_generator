# Synapse_Mindmap_generator

To clean and remove duplicated sentences:

###install spaCy
`pip install spacy`

`python -m spacy download en_core_web_sm`


###call functoion:
`sentence_preprocessing(paragraph)`

input:
`paragraph`: string

output:
`sentence_no_rep_word_list`: a list of spacy sentences (w/ dup sentences & stop words but w/o dup words)

`sentence_keep`: a list of 0 and 1 (0 for remove, 1 for keep) that keeps track of whether a sentence should be removed. Same length as sentence_no_rep_word_list

`no_rep_sentence_list`: a list of spacy sentences (with stop words, w/o dup sentences/dup words)

`sim_val_list`: records the similarity between two consecutive sentences