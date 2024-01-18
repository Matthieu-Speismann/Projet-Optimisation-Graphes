import random as rd
import networkx as nx
import matplotlib.pyplot as plt
from generationBDD import G, courses, profs, availabilityMatrix
from Coloration_graphes import normalisation, greedy_coloring, trivial_coloring, elem_different, max_couleur

n : int = len(courses)
"""Number of different courses. 
-
"""

index_courses : list[int] = [i for i in range(n)]
"""Transformation of the name of the courses into the list of their indexs
"""

availability_courses : list[list[int]] = [[] for i in range(n)]
"""Binary matrix representing the availability of the courses
-
    list[list[int]]: Lines are courses and columns are the dates.
"""
for classe in range(n):
    for prof in range(len(profs)) :
        if (courses[classe], profs[prof]) in list(G.edges()):
            availability_courses[classe] = list(availabilityMatrix[prof])

real_courses_names : dict = {}
"""Dictionnary with the corresponding names and indexs of the courses
-
"""
for i in range(n):
    real_courses_names[index_courses[i]] = courses[i]

print(real_courses_names)

new_graph = nx.Graph()
new_graph.add_nodes_from(index_courses)
for i in range(n):
    for j in range(n):
        if [path for path in nx.all_simple_paths(G, source=courses[i], target=courses[j], cutoff=2) if len(path) == 3]:
            new_graph.add_edge(index_courses[i], index_courses[j])


# Application des méthodes / Application of the methods :

normalisation(new_graph)
node_colors = greedy_coloring(new_graph, availability_courses, number_rooms = 10)
new_graph = nx.relabel_nodes(new_graph, real_courses_names)


# Génération des label du graphe affiché / Label generation for the printed graphe: 

colorCoursesDict= {}
for node, indexColor in zip(new_graph.nodes, node_colors):
    if indexColor in colorCoursesDict:
        colorCoursesDict[indexColor].append(node)
    else:
        colorCoursesDict[indexColor] = [node]


# Analyse / Analysis :

print("Nombre de couleur: " + str(elem_different(node_colors)))
print("Dernière couleur utilisée: " + str(max_couleur(node_colors)))


# Affichage des graphes / Drawing the graphs: 

plt.figure(2)
nx.draw(new_graph, node_color = node_colors, with_labels = True, node_size=1500)
plt.show()
