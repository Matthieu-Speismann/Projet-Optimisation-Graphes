import matplotlib.pyplot as plt
import networkx as nx

colors = ['b','g','r','c','m','y','k','w']

def tri_edges(edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(edges, key = lambda x: max(x))

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

        
    
# Tests: 
edges = [(0,1),(0,3),(1,2),(2,4),(2,5),(2,6),(1,3),(1,7),(3,6),(4,7),(5,6),(6,7)]
sorted_edges = tri_edges(edges)
print(sorted_edges)
G = nx.Graph(sorted_edges)
node_colors = greedy_coloring(G)
nx.draw(G, with_labels = True, node_color = node_colors)
plt.show()