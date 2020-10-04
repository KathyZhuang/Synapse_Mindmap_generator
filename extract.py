import spacy
import nltk
nltk.download('wordnet')
# from nltk.corpus import wordnet
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
for word in ['example']:
    syns = wordnet.synsets(word)
    for syn in syns:
        for l in syn.lemmas():
            child_set.append(l.name())

class Node:
    def __init__(self, parentNode, text=None):
        self.parent = parentNode
        self.text = text
        self.children = []
        self.entities = []
        self.seq = False
        if parentNode and (parentNode.seq or parentNode.prev_seq):
            self.prev_seq = True
        else:
            self.prev_seq = False
    
    def save_json(self):
        with open('example_tpo.json', 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        d = {'text': self.text, 'children': [child.to_dict() for child in self.children]}
        return d

def newParallel(node, text, entities=[]):
    parent = node.parent
    parallel = Node(parentNode=parent, text=text)
    parallel.entities = entities
    parent.children.append(parallel)
    return parallel

def newChild(node, text, entities=[]):
    child = Node(parentNode=node, text=text)
    child.entities = entities
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
            print(entities)

    if not node.parent:
        print('detect child', 'None')
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
                    print('parallel seq', token.text)
                    return new_node
                elif i < len(tokens)-3 and len(keyword.split('_')) > 1 and all([keyword.split('_')[j] == tokens[i+j].text for j in range(len(keyword.split('_')))]):
                    new_node = newParallel(node, text, entities) if node.seq else processNode(node.parent, tokens, text)
                    new_node.seq = True
                    print('parallel seq', token.text)
                    return new_node

        for keyword in parallel_set:
            if token.text.lower() == keyword:
                print('parallel', token.text)
                return newParallel(node, text, entities)
            elif i < len(tokens)-3 and len(keyword.split('_')) > 1 and all([keyword.split('_')[j] == tokens[i+j].text for j in range(len(keyword.split('_')))]):
                print('parallel', token.text)
                return newParallel(node, text, entities)
        #if token.text in parallel_set: #[secondly, thirdly, also, then, next, finally, and, but, moreover, another, other]
        #    print('detect parallel')
        #    return newParallel(node, text, entities)
        if i <= 4 and token.text.lower() in one_set: #[one, firstly]
            print('detect child', 'one', token.text)
            new_node = newChild(node, text, entities)
            new_node.seq = True
            return new_node
        if token.text.lower() in child_set: #[one, firstly]
            print('detect child', 'example', token.text)
            new_node = newChild(node, text, entities)
            return new_node
        if i <= 4 and token.text.lower() in ['it', 'he', 'she', 'they', 'this', 'these', 'those', 'that']: #如果有代词
            print('detect child', 'pronoun', token.text)
            return newChild(node, text, entities)
        if token.text.lower() in node.entities:
            print('detect child', 'entity', token.text)
            return newChild(node, text, entities)
        i += 1
    
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
        addNodeGraph(G, child)

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

    sentences = getSentences(text)

    print (text)
    #for sentence in sentences:
    #    triples.append(processSentence(sentence))
    node = Node(parentNode=None, text='Notes')
    root = node
    for sentence in sentences:
        tokens = nlp_model(sentence)
        node = processNode(node, tokens, sentence)
    root.save_json()
    printNodeGraph(root)