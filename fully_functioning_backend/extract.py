import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import wordnet
import json

nlp_model = spacy.load('en_core_web_sm')
stopwords = set(nlp_model.Defaults.stop_words)
keep_list = ['for', 'to', 'no', 'of']
for word in keep_list:
    stopwords.remove(word)

parallel_set = []
for word in ['also', 'moreover', 'another', 'other']:
    syns = wordnet.synsets(word)
    for syn in syns:
        for l in syn.lemmas():
            parallel_set.append(l.name())
seq_set = []
for word in ['secondly', 'thirdly', 'then', 'next', 'finally']:
    syns = wordnet.synsets(word)
    for syn in syns:
        for l in syn.lemmas():
            seq_set.append(l.name())
one_set = []
for word in ['firstly']:
    syns = wordnet.synsets(word)
    for syn in syns:
        for l in syn.lemmas():
            one_set.append(l.name())
child_set = []
for word in ['example', 'however']:
    syns = wordnet.synsets(word)
    for syn in syns:
        for l in syn.lemmas():
            child_set.append(l.name())

# Code for cleaning text
def split_para_to_sentence(paragraph):
    '''takes in a long paragraph (string), returns a list of string'''
    para = paragraph
    doc = nlp_model(para)
    sentences = list(doc.sents)
    return sentences

def remove_rep_word(sentence):
    '''input: spacy object sentence
    output: spacy object sentence with duplicate words removed'''
    string_sentence = [token.orth_ for token in sentence]
    ulist = []
    [ulist.append(x) for x in string_sentence if x not in ulist]
    return nlp_model(' '.join(ulist))

def remove_stop_punct(sentence):
    '''input: a spacy object sentence
       output: a spacy object sentence'''
    new_sent = []
    [new_sent.append(token.orth_) for token in sentence if not token.is_stop | token.is_punct]
    return nlp_model(' '.join(new_sent))

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
    return no_rep_sentence_list


# Code for knowledge extraction
class Node:
    def __init__(self, parentNode, text=None, entities=[]):
        self.parent = parentNode
        self.depth = parentNode.depth + 1 if parentNode else 0
        self.text = text
        self.children = []
        self.entities = entities
        self.next_is_child = False
        self.seq = False
        if parentNode and (parentNode.seq or parentNode.prev_seq):
            self.prev_seq = True
        else:
            self.prev_seq = False
    
    def save_json(self):
        with open('example.json', 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        d = {'text': self.text, 'children': [child.to_dict() for child in self.children]}
        return d

def newParallel(node, text, entities=[]):
    parent = node.parent
    parallel = Node(parentNode=parent, text=text, entities=entities)
    parent.children.append(parallel)
    return parallel

def newChild(node, text, entities=[]):
    child = Node(parentNode=node, text=text, entities=entities)
    node.children.append(child)
    return child

def common(word):
    return False

def getSentences(text):
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    document = nlp(text)
    return [sent.string.strip() for sent in document.sents]

def processNode(node, tokens, text):
    entities = []
    for token in tokens:
        if any(subs in token.dep_ for subs in ['nsubj', 'dobj', 'pobj']) and 'PRON' not in token.pos_ and 'DET' not in token.pos_:
            entities.append(token.text.lower())
        #print(entities)

    if not node.parent:
        #print('detect child', 'None')
        return newChild(node, text, entities)

    i = 0
    for token in tokens:
        if "punct" in token.dep_:
            continue
        if node.seq or node.prev_seq:
            for keyword in seq_set:
                if token.text.lower() == keyword:
                    new_node = newParallel(node, text, entities) if node.seq else processNode(node.parent, tokens, text)
                    new_node.seq = True
                    #print('parallel seq', token.text)
                    return new_node
                elif i < len(tokens)-3 and len(keyword.split('_')) > 1 and all([keyword.split('_')[j] == tokens[i+j].text for j in range(len(keyword.split('_')))]):
                    new_node = newParallel(node, text, entities) if node.seq else processNode(node.parent, tokens, text)
                    new_node.seq = True
                    #print('parallel seq', token.text)
                    return new_node

        for keyword in parallel_set:
            if token.text.lower() == keyword:
                #print('parallel', token.text)
                return newParallel(node, text, entities)
            elif i < len(tokens)-3 and len(keyword.split('_')) > 1 and all([keyword.split('_')[j] == tokens[i+j].text for j in range(len(keyword.split('_')))]):
                #print('parallel', token.text)
                return newParallel(node, text, entities)
        #if token.text in parallel_set: #[secondly, thirdly, also, then, next, finally, and, but, moreover, another, other]
        #    print('detect parallel')
        #    return newParallel(node, text, entities)
        if i <= 4 and token.text.lower() in one_set: #[one, firstly]
            #print('detect child', 'one', token.text)
            new_node = newChild(node, text, entities)
            new_node.seq = True
            return new_node
        if token.text.lower() in child_set: #[one, firstly]
            #print('detect child', 'example', token.text)
            new_node = newChild(node, text, entities)
            return new_node
        if i <= 7 and token.text.lower() in ['it', 'he', 'she', 'they', 'this', 'these', 'those', 'that']: #如果有代词
            #print('detect child', 'pronoun', token.text)
            return newChild(node, text, entities)
        if token.text.lower() in node.entities:
            #print('detect child', 'entity', token.text)
            return newChild(node, text, entities)
        i += 1

        if node.seq and len(node.entities) <= 1:
            return newChild(node, text, entities)
    
    return processNode(node.parent, tokens, text)
        
def remove_stopwords(sentence):
    tokens = sentence.split(" ")
    tokens_filtered= [word for word in tokens if not word in stopwords]
    return (" ").join(tokens_filtered)

def printNodeGraph(node):
    G = nx.Graph()
    G.add_node(node.text)
    addNodeGraph(G, node)
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9, font_size=9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.savefig('example.jpg')
    plt.show()

def addNodeGraph(G, node):
    for child in node.children:
        G.add_node(remove_stopwords(child.text))
        G.add_edge(remove_stopwords(node.text), remove_stopwords(child.text))
        G.add_node(child.text)
        G.add_edge(node.text, child.text)
        addNodeGraph(G, child)

class Synapse:
    def __init__(self):
        self.root = Node(parentNode=None, text='Notes')
        self.node = self.root
        self.prev_sentence = None
    
    def process(self, sentence):
        if type(sentence) != str:
            return None
        prev2_sentence = self.prev_sentence
        self.prev_sentence = sentence
        if len(prev2_sentence.split(' ')) >= 3 and sentence.split(' ')[0] != prev2_sentence.split(' ')[0]:
            return prev2_sentence
        return None

    def update(self, sentence):
        sentence = self.process(sentence)
        if sentence is None:
            return False
        tokens = nlp_model(sentence)
        self.node = processNode(self.node, tokens, sentence)
        return True

    def display(self):
        self.printNode(self.root, 0)

    def printNode(self, node, indent=0):
        print(" "*indent + node.text + '\n')
        for child in node.children:
            self.printNode(child, indent+4)

    def printlastNode(self):
        print(" "*(4*self.node.depth) + self.node.text + '\n')





if __name__ == "__main__":
    
    text = "Our goal is to help you organize the information you get from all sorts of videos."\
            "So snap, we got your meeting notes and lecture notes organized."\
            "Our basic idea is to turn recordings to mind map."\
            "First of all, we delete redundant and similar sentences."\
            "To do this, we use weighted-average of word2vec vectors to measure the similarity between sentences, and remove the redundant ones."\
            "Then, we want to turn the sentences to knowledge graphs."\
            "We use part-of-speech tagging to extract the subjects, objects and relations from the sentences."\
            "We also use term frequency analysis to filter out unimportant graphs."\
            "Finally, we present the graph as a mind map. "\
            "The mind map can then be edited by the users for adjustment."
    
    text = "So far we have covered biodiversity in the hard wood forest here in the upper peninsula of Michigan from a number of angles."\
"We’ve looked at everything from how biodiversity relates to species stability, to competition for forests resources and more."\
"But now I want to discuss what’s called pedodiversity. Pedodiversity is basically soil diversity."\
"When we analyze pedodiversity within an area, we are measuring how much variability there is in soil properties"\
"and how many different types of soil there are in a particular area."\
"So we look at soil chemistry. For example, how much nitrogen or magnesium there’s in the soil in one spot."\
"And we compare it with the chemistry of the soil a short distance away."\
"Until recently, there hasn’t been a whole lot of attention paid to pedodiversity."\
"But that’s changing rapidly. More and more studies are being done in these fields."

    text = "We are living in an information era, with 2 video conferences and 5 online lectures each day. Now, it’s more crucial than ever for us to overcome this overwhelmed. That’s why we invented Synapse. Snap, We got your video conference notes organized. We normally expect at least 90% of our video conference came out to be useful, which can be stored in the bigger circle representing your memorization. However, multiple situation arises. Thus we want to take care of this process for you, using Natural Language Processing. It works just like your brain, but you don’t need to use any effort. Our idea is to analyze various information embed in your videos, and to organize it as a mind map through Synapse neural network, so it’s logical and presentable. Then, we will hand you the most valuable information as take-home message. However, just like human brain, we make mistakes. That’s when you can edit our mindmap, which will hopefully help us with improving our model using supervised learning in the future. There are 3 steps we use to achieve this goal. First, be selective. We will carefully delete repetitive sentences and words using spaCy and word2vec. Then, we make it more comprehensible. Our model will try to interpret the logic relationships between sentences using information extraction, for a mind map to be finally generated. Finally, we want you to be productive. So we use word frequency and keywords to unpack the valuable pieces like date, to-do-list, and network info, to boost your productivity. Because Synapse is a productivity idea, in the future, we want it to be connected to other productive services you are using. We want you to be able to directly input from your educational videos and conference services. After Synapse skim through it, the mind map can be put in your usual note-taking, collaborating, and calendar tools. So that you can focus more on interacting with people. So next time, when information arises, don’t panic. Synapse will snap, and we will get your video notes organized."

    sentences = getSentences(text)

    synapse = Synapse()
    for sentence in sentences:
        synapse.update(sentence)
        synapse.display()
    # print (text)
    #for sentence in sentences:
    #    triples.append(processSentence(sentence))
    # node = Node(parentNode=None, text='Notes')
    # root = node
    # for sentence in sentences:
    #     tokens = nlp_model(sentence)
    #     node = processNode(node, tokens, sentence)
    # root.save_json()
    # printNodeGraph(root)