import spacy
nlp = spacy.load('en_core_web_sm')

def split_para_to_sentence(paragraph):
    '''takes in a long paragraph (string), returns a list of string'''
    para = paragraph
    doc = nlp(para)
    sentences = list(doc.sents)
    return sentences

def remove_rep_word(sentence):
    '''input: spacy object sentence
    output: spacy object sentence with duplicate words removed'''
    string_sentence = [token.orth_ for token in sentence]
    ulist = []
    [ulist.append(x) for x in string_sentence if x not in ulist]
    return nlp(' '.join(ulist))

def remove_stop_punct(sentence):
    '''input: a spacy object sentence
       output: a spacy object sentence'''
    new_sent = []
    [new_sent.append(token.orth_) for token in sentence if not token.is_stop | token.is_punct]
    return nlp(' '.join(new_sent))

def remove_rep_sentences(sentence1,sentence2):
    '''input: two spacy object sentences with duplicate words, stop words and punctuations removed
        output: (True, True) meaning that both sentences should be kept or (True, False) meaning that the second
        sentence should be deleted'''
    sim_val = sentence1.similarity(sentence2)
    if sim_val > 0.85:
        return 1,0,sim_val
    else:
        return 1,1,sim_val


def sentence_preprocessing(paragraph):
    '''input: a paragraph (string)
     output:
     sentence_no_rep_word_list: a list of spacy sentences (w/ dup sentences & stop words but w/o dup words)
     sentence_keep: a list of 0 and 1 (0 for remove, 1 for keep) that keeps track of whether a sentence should be
     removed. Same length as sentence_no_rep_word_list
     no_rep_sentence_list: a list of spacy sentences (with stop words, w/o dup sentences/dup words)
     sim_val_list: records the similarity between two consecutive sentences
     '''
    sentence_list = split_para_to_sentence(paragraph)
    sentence_no_rep_word_list, sentence_no_rep_stop_punct_list, no_rep_sentence_list, sim_val_list = [], [], [], []
    sentence_keep = [1] * len(sentence_list)
    cum = 0
    for sentence in sentence_list:
        sentence_no_rep_word_list.append(remove_rep_word(sentence))
        # [spacy sentence,spacy sentence,...,spacy sentence]
        sentence_no_rep_stop_punct_list.append(remove_stop_punct(remove_rep_word(sentence)))
        #  [spacy sentence,spacy sentence,...,spacy sentence]

        if len(sentence_no_rep_stop_punct_list)>1:
            keep_s1, keep_s2,sim_val = remove_rep_sentences(sentence_no_rep_stop_punct_list[cum-1],sentence_no_rep_stop_punct_list[cum])
            sim_val_list.append(sim_val)
            if sentence_keep[cum-1] != 0:
                sentence_keep[cum-1],sentence_keep[cum] = keep_s1, keep_s2
            else:
                sentence_keep[cum - 1], sentence_keep[cum] = sentence_keep[cum - 1], keep_s2
        cum += 1

    for i in range(0,len(sentence_list),1):
        if sentence_keep[i] == 1:
            sentence_keep, no_rep_sentence_list.append(sentence_no_rep_word_list[i])
    return sentence_no_rep_word_list, sentence_keep, no_rep_sentence_list, sim_val_list

paragraph = 'Gus Proto is a Python developer currently working for a London-based Fintech company for a London-based Fintech company.' \
            'Gus Proto is a Python developer currently working for a London-based Fintech company for a London-based Fintech company.' \
            'Gus Proto is a Python developer currently working currently working currently working for a London-based Fintech company for a London-based Fintech company.'\
            'He is he is he is he is interested in learning Natural Language Processing.' \
            'Gus Proto is a Python developer currently working currently working currently working for a London-based Fintech company for a London-based Fintech company.' \
            'He is he is he is he is interested in learning Natural Language Processing.'\
# # stc_list = split_para_to_sentence(paragraph)

sentence_no_rep_word_list, sentence_keep, no_rep_sentence_list, sim_val_list = sentence_preprocessing(paragraph)
print('sentence_keep2', sentence_keep)
print('sentence_no_rep_word_list', sentence_no_rep_word_list)
print('no_rep_sentence_list', no_rep_sentence_list)
