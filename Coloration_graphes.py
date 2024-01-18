""" 
Implémentation de méthodes pour appliquer des colorations propres à des graphes avec nos 
contraintes supplémentaires.
-
Implementation of graph coloring methods taking into account our specific constraints.
-
Auteurs / Authors: Matthieu SPEISMANN, Théo GUELLA et Guillaume TRAN-RUESCHE
"""

# Modules: 
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors

# Variables globales / Global variables:

"""Entier représentant le nombre de classe disponible dans l'école.
-
Integer representing the amount of rooms available.
-
Le nombre de cours ayant lieu sur un même créneau ne peut alors pas être supérieur à ce nombre.
In consequences, the number of courses taking place at the same time cannot bea bove that number."""


colors: list[str] = ['blue','green','red','yellow','orange', 'deeppink', 'cyan', 'crimson', 'darkviolet', 'lime',
                     'darkgrey', 'navy', 'lightcoral', 'seagreen', 'mediumturquoise']
""" Cette liste permet d'obtenir une couleur (représentée par une chaine de caractères) à partir de son index

    This list allows to get a color (represented by a string) thanks to its index.
"""


colors_dict: dict[str, int] = {}
""" Ce dictionnaire permet d'obtenir l'indice d'une couleur à partir de sa chaine de caractère.

    This dictionnary allows to get the index of a color thanks to its string. 
 """
# Construction du dictionnaire / Construction of the dictionnary:
for i in range(len(colors)):
    colors_dict[colors[i]] = i


def normalisation(graph):
    """ Fonction pour normaliser le graphe aux fonctions qu'on utilise.
    -
    Function to normalise the graph for the functions we are using.
    - 
    Modifie le graph en place pour que les nodes soit triés dans son encodage / Modify the graph in place in order to sort the nodes.     

    Args:
        graph (Graph): Graphe à normaliser / Graph to normalize. 
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


def trivial_coloring(graph, availability_courses: list[list[int]]) -> list[str]:
    """ Propose une coloration triviale.
    -
    Get a trivial coloration.
    -
    A chaque noeud est associée une couleur différente / To each node is associated a different color

    Args:
        - graph (Graph): Graphe non orienté [Networkx] / Unoriented graph [Networkx]
        - availability_courses: list[list[int]]: Matrice binaire représentant les disponibilités des cours. Cours indicées en lignes et créneaux indicées en lignes /
                                                Binary Matrix representing the courses availability. Courses indexed in ligns and time in columns.

    Returns:
        - list[str]: Liste des couleurs pour chaque noeuds./ List of the color for each node. 
    """

    node_colors: list[str] = []
    for node in graph.nodes():
        for index in range(len(colors)):
            # Vérification que la couleur est différente de toutes les autres:
            # Verification that the color is different form the others:
            if colors[index] not in node_colors:
                # Vérification que le prof est disponible:
                # Verification that the teacher is available:
                try:
                    if availability_courses[node][index] == 1:
                        node_colors.append(colors[index])
                        break
                # Si l'erreur a lieu, cela signifie qu'il n'y a pas assez de couleur (et donc de créneaux) pour avoir une solution acceptable.
                # If the error take place, it means that there is not enough colors (and so of times) to have an acceptable solution. 
                except IndexError:
                    raise ValueError("No available solution with this method.")
    return node_colors

def number_courses_color(color: str, node_colors: list[str]) -> int:
    """Récupère le nombre de cours qui ont déjà cette couleur.
    -
    Get the number of courses which are already on the input color
    -

    Args:
        - color (str): Chaine de caractère qui représente la couleur : string that represents the color. 
        - node_colors (list[str]): Liste des noeuds de couleur actuel / Liste of the node colors at this time.

    Returns:
        - int: Nombre de cours ayant déjà cette couleur / Number of courses which have already this input color.  
    """
    res = 0
    for elem in node_colors:
        if elem == color:
            res += 1
    return res


def greedy_coloring(graph, availability_courses: list[list[int]], number_rooms: int) -> list[str]:
    """Algoritme glouton de coloration d'un graphe
    -
    Graph coloration greedy algorithm
    - 
    En parcourant tous les sommets successivement et attribuer à un sommet la plus petite couleur possible parmi celles déjà utilisées
    (différente de celles de ses voisins s'ils sont déjà colorés) à ce sommet, ou bien une nouvelle couleur si toutes les couleurs 
    sont utilisées par les voisins.
    
    By using every nodes successively and attributing for a node the tinier color possible which is different for all its neighbors
    to its node or a new color if they are all already used by its neighbors.

    Args:
        - graph (Graph): Graphe non orienté [Networkx] / Unoriented graph [Networkx]
        - availability_courses: list[list[int]]: Matrice binaire représentant les disponibilités des cours. Cours indicées en lignes et créneaux indicées en lignes /
                                                Binary Matrix representing the courses availability. Courses indexed in ligns and time in columns.
        

    Returns:
        list[str]: Liste des couleurs pour chaque noeuds.
    """

    node_colors: list[str] = []
    # Parcours de tous les sommets du graphes / Browsing all nodes of the graph:
    for sommet in graph.nodes():
        neighbors = list(graph.neighbors(sommet)) # Voisins de ce sommets / Neighbors of the node:
        neighbors_colors = [] 
        # Parcours des voisins du sommet/ Browsing the neighbors:
        for neighbor in neighbors:
            try:
                # Ajouter la couleurs du voisins dans une liste/ Adding the color of the neighbor to a list: 
                neighbors_colors.append(node_colors[neighbor])
            except IndexError:
                pass # Si la couleur n'est pas encore attribuée, ignorer / If not allready attibuted, pass:
        for color in colors:
            # Si la couleurs n'est pas parmi les voisins / If the color is not in the neighbors: 
            if color not in neighbors_colors:
                index = colors_dict[color]
                # Vérification de la diponibilité du prof / Teacher availability verification: 
                try:
                    if availability_courses[sommet][index] == 1:
                        # Vérification de la condition sur le nombre de salles de classe / Number of rooms availability verification:
                        if number_courses_color(color, node_colors) < number_rooms:
                            node_colors.append(colors[index])
                            break
                        else: pass
                    else: pass
                # Si l'erreur a lieu, cela signifie qu'il n'y a pas assez de couleur (et donc de créneaux) pour avoir une solution acceptable.
                # If the error take place, it means that there is not enough colors (and so times) to construct an available solution:
                except IndexError:
                    raise ValueError("No available solution with this method.")
    return node_colors

def degree_order(graph):
    """ Retourne les nœuds triés par ordre décroissant de degré
    - 
    Returns the nodes sorted by decreasing degree:

    Args:
        graph (Graphe): Graphe Networkx / Graph Networkx

    Returns:
        list[int]: Liste des sommets triées par degeré décroissan / List of the nodes ordered by decreasing degree.
    """

    return sorted(graph.nodes(), key=lambda x: graph.degree[x], reverse=True)

def improved_greedy_coloring(graph, availability_courses: list[list[int]], number_rooms: int) -> list[str]:
    """Algoritme glouton de coloration d'un graphe
    -
    Similaire à l'algorithme glouton, mais les noeuds sont cette fois parcourus par ordre décroissant de leur arité.

    Args:
        - graph (Graph): Graphe non orienté [Networkx] / Unoriented graph [Networkx]
        - availability_courses: list[list[int]]: Matrice binaire représentant les disponibilités des cours. Cours indicées en lignes et créneaux indicées en lignes /
                                                Binary Matrix representing the courses availability. Courses indexed in ligns and time in columns.

    Returns:
        list[str]: Liste des couleurs pour chaque noeuds.
    """

    node_colors: list[str] = []
    nodes = degree_order(graph)
    # Parcours de tous les sommets du graphes / Browsing all nodes of the graph:
    for sommet in graph.nodes():
        neighbors = list(graph.neighbors(sommet)) # Voisins de ce sommets / Neighbors of the node:
        neighbors_colors = [] 
        # Parcours des voisins du sommet/ Browsing the neighbors:
        for neighbor in neighbors:
            try:
                # Ajouter la couleurs du voisins dans une liste/ Adding the color of the neighbor to a list: 
                neighbors_colors.append(node_colors[neighbor])
            except IndexError:
                pass # Si la couleur n'est pas encore attribuée, ignorer / If not allready attibuted, pass:
        for color in colors:
            # Si la couleurs n'est pas parmi les voisins / If the color is not in the neighbors: 
            if color not in neighbors_colors:
                index = colors_dict[color]
                # Vérification de la diponibilité du prof / Teacher availability verification: 
                try:
                    if availability_courses[sommet][index] == 1:
                        # Vérification de la condition sur le nombre de salles de classe / Number of rooms availability verification:
                        if number_courses_color(color, node_colors) < number_rooms:
                            node_colors.append(colors[index])
                            break
                # Si l'erreur a lieu, cela signifie qu'il n'y a pas assez de couleur (et donc de créneaux) pour avoir une solution acceptable.
                # If the error take place, it means that there is not enough colors (and so times) to construct an available solution:
                except IndexError:
                    raise ValueError("No available solution with this method.")
    return node_colors

# Fonctions utiles d'analyse / Useful analysis functions: 

def elem_different(L:list[any]) -> int:
    """Renvoie le nombre d'élément différente dans une liste.
    - 
    Get the number of different elements in a list
    -

    Args:
        L (list[any])

    Returns:
        int: Nombre d'éléments différent trouvé / Number of different elements found.
    """
    res = 0
    unique_elements = []
    for elem in L:
        if elem not in unique_elements:
            res += 1
            unique_elements.append(elem)
    return res

def max_couleur(node_colors: list[str]) -> int:
    """Renvoie l'indice de la dernière couleur utilisée.
    -
    Get the index of the last used color.
    -

    Args:
        node_colors (list[str]): Liste des couleurs pour chaque noeud (en indice) / List of the color for each node (indexed)

    Returns:
        int: Indice de la dernière couleur / Index of the last color.
    """
    node_colors_indexes = []
    for color in node_colors:
        node_colors_indexes.append(colors_dict[color])
    return max (node_colors_indexes)