import matplotlib.pyplot as plt
import networkx as nx

colors = ['b','g','r','c','m','y','k','w']

def normalisation(graph):
    """ Fonction pour normaliser le graph aux fonctions qu'on utilise.
    -
    Modifie le graph en place pour que les nodes soit triés dans son encodage.
    Args:
        graph (Graph)
    """
    for node in list(graph.nodes()):
        G.remove_node(node)
    sorted_nodes = sorted(list(graph.nodes()))
    for node in sorted_nodes:
        graph.add_node(node)
    for (node1, node2) in edges:
        graph.add_edge(node1, node2)

def greedy_coloring(graph) -> list[str]:
    """Algoritme glouton de coloration d'un graphe
    -
    Nous allons envisager tous les sommets successivement et attribuer 
    à un sommet la plus petite couleur possible parmi celles déjà utilisées
    (différente de celles de ses voisins s'ils sont déjà colorés) 
    à ce sommet, ou bien une nouvelle couleur si toutes les couleurs 
    sont utilisées par les voisins
    
    Args:
        graph (Graph): Graphe non orienté [Networkx]

    Returns:
        list[str]: Liste des couleurs pour chaque noeuds
    """

    node_colors = []
    # Parcours de tous les sommets du graphes:
    for sommet in graph.nodes():
        voisins = list(graph.neighbors(sommet)) # Voisins de ce sommets
        couleurs_voisins = [] 
        # Parcours des voisins du sommet:
        for voisin in voisins:
            try:
                # Ajouter la couleurs du voisins dans une liste
                couleurs_voisins.append(node_colors[voisin])
            except IndexError: 
                pass # Si la couleur n'est pas encore attribuée, ignorer
        # Pour toutes les couleurs définies:
        for color in colors:
            # Si la couleurs n'est pas parmi les voisins:
            if color not in couleurs_voisins:  
                node_colors.append(color) # Attribution de la couleur au sommet 
                break
    return node_colors
    
if "__main__" == __name__:    
    # Tests:

    edges = [(0,3),(1,4),(2,6),(5,3),(0,4),(1,4),(2,7),(2,5)]
    G = nx.Graph(edges)
    normalisation(G)
    
    node_colors = greedy_coloring(G)

    nx.draw(G, node_color = node_colors, with_labels = True)
    plt.show()