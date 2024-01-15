""" 

-
Auteurs: Matthieu SPEISMANN, Théo GUELLA et Guillaume TRAN-RUESCHE
"""

# Modules: 
import matplotlib.pyplot as plt
import networkx as nx

# Variables globales:
dispo_prof: list[list[int]] = [
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1],
            [1, 0, 0, 1, 1]]
"""Matrice binaire représentant les disponibilité des profs. 
-
    list[list[int]]: Profs et donc cours indicées en lignes et créneaux indicées en lignes.
"""

nombre_classe: int = 2
"""Entier représentant le nombre de classe disponible dans l'école.
-
Le nombre de cours ayant lieu sur un même créneau ne peut alors pas être supérieur à ce nombre."""

colors: list[str] = ['b','g','r','y','m','c','k','w']
""" Cette liste permet d'obtenir une couleur (représentée par une chaine de caractères) à partir de son index
    -
"""

colors_dict: dict[str, int] = {}
""" Ce dictionnaire permet d'obtenir l'indice d'une couleur à partir de sa chaine de caractère.
    -
 """
for i in range(len(colors)):
    colors_dict[colors[i]] = i


def normalisation(graph):
    """ Fonction pour normaliser le graph aux fonctions qu'on utilise.
    -
    Modifie le graph en place pour que les nodes soit triés dans son encodage.

    Args:
        graph (Graph)
    """

    nodes = list(graph.nodes)
    edges = list(graph.edges)
    for node in list(graph.nodes()):
        graph.remove_node(node)
    sorted_nodes = sorted(nodes)
    for node in sorted_nodes:
        graph.add_node(node)
    for (node1, node2) in edges:
        graph.add_edge(node1, node2)

    
def trivial_coloring(graph) -> list[str]:
    """Propose une coloration triviale.
    -
    A chaque noeud est associée une couleur différente. 

    Args:
        graph (Graph): Graphe non orienté [Networkx]

    Returns:
        list[str]: Liste des couleurs pour chaque noeuds.
    """

    node_colors: list[str] = []
    for sommet in graph.nodes():
        for index in range(len(colors)):
            # Vérification que la couleur est différente de toutes les autres:
            if colors[index] not in node_colors:
                # Vérification que le prof est disponible:
                try:
                    if dispo_prof[sommet][index] == 1:
                        node_colors.append(colors[index])
                        break
                # Si l'erreur a lieu, cela signifie qu'il n'y a pas assez de couleur (et donc de créneaux) pour avoir une solution acceptable.
                except IndexError:
                    raise ValueError("Pas de solution avec cette méthode de résolution.")
    return node_colors

def nombre_cours_couleur(color: str, node_colors: list[str]) -> int:
    """ """ 
    res = 0
    for elem in node_colors:
        if elem == color:
            res += 1
    return res

def greedy_coloring(graph) -> list[str]:
    """Algoritme glouton de coloration d'un graphe
    -
    Nous allons envisager tous les sommets successivement et attribuer à un sommet la plus petite couleur possible parmi celles déjà utilisées
    (différente de celles de ses voisins s'ils sont déjà colorés) à ce sommet, ou bien une nouvelle couleur si toutes les couleurs 
    sont utilisées par les voisins.

    Args:
        graph (Graph): Graphe non orienté [Networkx]

    Returns:
        list[str]: Liste des couleurs pour chaque noeuds.
    """

    node_colors: list[str] = []
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
                index = colors_dict[color]
                # Vérification de la diponibilité du prof:
                try:
                    if dispo_prof[sommet][index] == 1:
                        # Vérification de la condition sur le nombre de salles de classe:
                        if nombre_cours_couleur(color, node_colors) < nombre_classe:
                            node_colors.append(colors[index])
                            break
                # Si l'erreur a lieu, cela signifie qu'il n'y a pas assez de couleur (et donc de créneaux) pour avoir une solution acceptable.
                except IndexError:
                    raise ValueError("Pas de solution avec cette méthode de résolution.")
    return node_colors

def degree_order(graph):
    """ Retourne les nœuds triés par ordre décroissant de degré
    - 
    
    Args:
        graph (Graphe): Graphe Networkx 

    Returns:
        list[int]: _description_
    """

    return sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)

def improved_greedy_coloring(graph) -> list[str]:
    """Algoritme glouton de coloration d'un graphe
    -
    Similaire à l'algorithme glouton, mais les noeuds sont cette fois parcourus par ordre décroissant de leur arité.

    Args:
        graph (Graph): Graphe non orienté [Networkx]

    Returns:
        list[str]: Liste des couleurs pour chaque noeuds.
    """

    node_colors: list[str] = []
    # Parcours de tous les sommets du graphes:
    nodes = degree_order(graph)
    for sommet in nodes:
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
                index = colors_dict[color]
                # Vérification de la diponibilité du prof:
                try:
                    if dispo_prof[sommet][index] == 1:
                        # Vérification de la condition sur le nombre de salles de classe:
                        if nombre_cours_couleur(color, node_colors) < nombre_classe:
                            node_colors.append(colors[index])
                            break
                # Si l'erreur a lieu, cela signifie qu'il n'y a pas assez de couleur (et donc de créneaux) pour avoir une solution acceptable.
                except IndexError:
                    raise ValueError("Pas de solution avec cette méthode de résolution.")
    return node_colors


if "__main__" == __name__:

    # Tests:
    
    import random as rd

    # edges aléatoire:
    n = len(dispo_prof) - 1
    
    rd_edges = []
    for i in range(15):
        a = rd.randint(0,n)
        b = rd.randint(0,n)
        while a == b:
            b = rd.randint(0,n)
        rd_edges.append((a,b))

    # edges précisé:
    edges = [(0,1), (0,2), (0,4), (1,3), (1,5), (3,6), (5,6), (2, 4), (4,3)]

    # Graphe et application
    G = nx.Graph(rd_edges)

    normalisation(G)
    
    node_colors1 = greedy_coloring(G)
    node_colors2 = improved_greedy_coloring(G)

    plt.figure(1)
    nx.draw(G, node_color = node_colors1, with_labels = True)
    plt.title("Greedy Coloring")
    
    plt.figure(2)
    nx.draw(G, node_color = node_colors2, with_labels = True)
    plt.title("Improved Greedy Coloring")
    
    plt.show()
