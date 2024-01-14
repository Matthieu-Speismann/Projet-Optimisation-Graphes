import random as rd
import networkx as nx
import matplotlib.pyplot as plt

parametres = {
    'nbrEleves': 15, #int N: Nombre d'élèves dans l'école
    'nbrCours': 4, #int N: Nombre de cours disponibles
    'duréeCours': 0.2, #float [0,1]: Probabilté avec laquelle un cours dure deux heures au lieu d'une
    'nbrProfs': 2, #int N: Nombre de professeurs dans l'école. nbrProfs < nbrCours. Un prof enseigne forcément un cours mais les cours sont répartis de manière aléatoire
    'probaCoursEleves': 0.3 #float [0,1]: Probabilité de création d'un lien, entre un élève et un cours
}

def lire_prenoms(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]
    
def LireMatieres(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]
    
def LireNoms(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]
    
prenomsEleves = lire_prenoms("prenoms.txt")
nomsProfs = lire_prenoms("noms.txt")
nomsMatieres = LireMatieres("matieres.txt")

eleves = [rd.choice(prenomsEleves) for _ in range(parametres['nbrEleves'])]  
cours = [rd.choice(nomsMatieres) for _ in range(parametres['nbrCours'])]
profs = [rd.choice(nomsProfs).split(" ")[0] for _ in range(parametres['nbrProfs'])]

liensCoursEleve = []
liensCoursProf = []

for eleve in eleves:
    hasCourse = False
    for matiere in cours:
        if rd.random() < parametres['probaCoursEleves']:
            liensCoursEleve.append((eleve, matiere)) #On affecte un élève à un cours avec une probabilité de 'probaCoursEleves'
            hasCourse = True
            print(eleve, matiere)
    if not(hasCourse): #Si l'élève n'a pas été associé à un cours, on lui en associe un au hasard
        liensCoursEleve.append((eleve, rd.choice(cours)))
        print(eleve, liensCoursEleve[-1])

for matiere in cours:
    liensCoursProf.append((matiere, rd.choice(profs)))



#  Création du graphe bipartite
G = nx.Graph()

# Ajout des élèves, cours et profs
G.add_nodes_from(eleves, bipartite=0, label='eleve')
G.add_nodes_from(cours, bipartite=1, label='matiere')
G.add_nodes_from(profs, bipartite=0, label='prof')

# Ajout des arrêtes
G.add_edges_from(liensCoursEleve)
G.add_edges_from(liensCoursProf)

# Positionnement des nœuds
pos = dict()
pos.update((node, (1, index / len(eleves))) for index, node in enumerate(eleves))  # Positionnement des élèves à gauche
pos.update((node, (2, index / len(cours))) for index, node in enumerate(cours))  # Positionnement des cours au centre
pos.update((node, (3, index / len(profs))) for index, node in enumerate(profs))  # Positionnement des profs à droite

# Création de la figure
fig, ax = plt.subplots()
nx.draw(G, pos, ax=ax, with_labels=True, font_color='black', node_color=['#77cad9' if G.nodes[node]['label'] == 'eleve' else '#64d16c' if G.nodes[node]['label'] == 'matiere' else '#f06573' for node in G.nodes], node_size=1000)
plt.show()
