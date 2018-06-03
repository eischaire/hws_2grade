import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)

model.init_sims(replace=True)

G = nx.Graph()

f = open('wordlist.txt', 'r', encoding='utf-8')
words = f.readlines()
for word in words:
    word = word.strip('\n')
    G.add_node(word)
    if word in model:
        for word2 in words:
            word2 = word2.strip('\n')
            if word2 in model and not word2 == word:
                if model.similarity(word, word2) > 0.5:
                    G.add_edge(word, word2)
centr = []
deg = nx.degree_centrality(G)
nn = 0
print('the most central:')
for nodeid in sorted(deg, key=deg.get, reverse=True):
    if nn <= 5:
        print(nodeid)
        n += 1
rad = {}
for comp in nx.connected_component_subgraphs(G):
    rad[comp] = nx.radius(comp)
clust = nx.average_clustering(G)
print('radiuses: \n')
for comp in rad:
    print(rad[comp])
### Учитывая, как выглядит граф, не вижу смысла подписывать, где чей радиус: очевидно, что в этом случае он ненулевой только в одном месте
print('clustering coefficient: ', clust)
nx.write_gexf(G, 'graph_file.gexf')
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color = 'blue', node_size = 30)
nx.draw_networkx_edges(G, pos, edge_color = 'red')
nx.draw_networkx_labels(G, pos, font_size = 14, font_family = 'Calibri')
plt.axis('off')
plt.show()
